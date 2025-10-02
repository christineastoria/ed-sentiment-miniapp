# ED Sentiment Warning API

This project is a mini-app built on [Modal](https://modal.com/) that uses [Anthropic’s Claude](https://docs.anthropic.com/) to detect and flag potentially harmful eating-disorder–related captions (e.g. TikTok, Reels, or other social posts).  
It builds upon my more extensive college research on semi supervised transfer learning for eating disorder sentiment analysis:  [Transfer Learning for Eating Disorder Sentiment Analysis]([https://docs.anthropic.com/](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1224/reports/custom_116620290.pdf)) 
The endpoint returns short, supportive warnings similar to the overlays you might see on TikTok, designed to protect viewers and encourage recovery-minded messaging.

## Features

- Claude-powered classification  
  Uses Anthropic’s Claude 3 Haiku to classify captions as `harmful`, `neutral`, or `supportive`.

- Short supportive warnings  
  Returns a very short viewer-facing message (≤15 words), like TikTok’s “This content may promote eating disorders.”

- Autoscaling on Modal  
  Deployed as a Modal web function with automatic scaling. Bursty traffic (hundreds of requests) spins up new containers, then scales back down.

- Swagger API docs  
  Comes with an auto-generated `/docs` page for quick testing in the browser.

## Tech Stack

- [Modal](https://modal.com/) — serverless infra for Python, autoscaling functions  
- [Anthropic Claude 3 Haiku](https://docs.anthropic.com/) — LLM inference  
- [FastAPI](https://fastapi.tiangolo.com/) — powering the endpoint & docs  

## Usage

### 1. Deploy the app
```bash
modal deploy app.py
```

This creates a web endpoint at a URL like:

```
https://christineastoria--ed-sentiment-warnings-predict-and-recommend.modal.run/
```

### 2. Send a request with curl
```bash
curl -X POST "https://christineastoria--ed-sentiment-warnings-predict-and-recommend.modal.run/"   -H "Content-Type: application/json"   -d '{"text": "How to not feel like a whale today"}'
```

### 3. Example response
```json
{
  "label": "harmful",
  "rationale": "The caption expresses negative body image.",
  "recommendation_for_viewer": "This content may promote eating disorders"
}
```

### 4. Interactive docs
Visit:
```
https://christineastoria--ed-sentiment-warnings-predict-and-recommend.modal.run/docs
```
to test via Swagger UI.

## Load Testing and Autoscaling

To simulate burst traffic, you can send multiple requests:

```bash
export URL="https://christineastoria--ed-sentiment-warnings-predict-and-recommend.modal.run/"
export BODY='{"text":"I feel like a whale today"}'

seq 1 200 | xargs -I{} -P 20 curl -s -X POST "$URL"   -H "Content-Type: application/json"   -d "$BODY" >/dev/null
```

Watch Modal’s dashboard to see containers spin up and scale back down automatically.

## Project Structure
```
functions/ed_sentiment_analysis/app.py     # Modal app definition + Claude integration
README.me  # Project overview and usage
```

## Future Work
- Frontend demo page (instead of Swagger JSON)  
- More nuanced labels (e.g. `triggering`, `educational`, `recovery-focused`)  
- Support for batch analysis of captions  
- Add observability (logging, metrics dashboards)

## Why This Project
This project demonstrates how AI infra (Modal) and safe-by-design LLMs (Claude) can be combined to solve a real, sensitive problem: harmful eating disorder content online.  
Instead of a toy demo, it focuses on responsible AI use, short warnings, and developer experience.
