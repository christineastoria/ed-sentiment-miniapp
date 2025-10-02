# app.py
import modal
import json
image = (
    modal.Image.debian_slim()
    .pip_install("anthropic", "fastapi[standard]")
)

app = modal.App(name="ed-sentiment-api", image=image)

LABELS = ["harmful", "neutral", "supportive"]
HYPOTHESIS = "This text is {label} regarding eating disorders."


app = modal.App("ed-sentiment-warnings", image=image)

LABELS = ["harmful", "neutral", "supportive"]

SYSTEM_PROMPT = (
    "You are a careful social media assistant scanning for eating-disorder related text. "
    "Return ONLY valid minified JSON with keys: "
    "{label, rationale, recommendation_for_viewer}. "
    f"'label' must be one of {LABELS}. "
    "The 'recommendation_for_viewer' is a very short message (like TikTok's overlays, <15 words). "
    "Keep recommendations supportive and only mildly clinical."
)                                                  
 
def classify_with_claude(text: str):
    import anthropic
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

    resp = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=400,
        temperature=0.2,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": text}],
    )
    print(resp)

    # get plain text from Claude
    out_text = "".join([c.text for c in resp.content if getattr(c, "type", "") == "text"])
    try:
        return json.loads(out_text)
    except Exception:
        return {"label": "neutral", "rationale": "Parse error", "supportive_rewrite": out_text[:200]}

@app.function(secrets=[modal.Secret.from_name("anthropic")])
@modal.fastapi_endpoint(method="POST", docs=True)
def predict_and_recommend(body: dict):
    text = (body or {}).get("text", "")
    return classify_with_claude(text)

# # local entrypoint to blast many requests & show autoscaling
# @app.local_entrypoint()
# def load_test(n: int = 200):
#     texts = ["Thinspo goals; dry fasting this week"] * n
#     # run them in parallel
#     for _ in classify_with_claude.map(texts, order_outputs=False):
#         pass