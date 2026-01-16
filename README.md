# LLM FastAPI Docker

Minimal text-generation API using FastAPI, Hugging Face transformers (`distilgpt2`), and Docker.  
The service exposes:

- `GET /health` for health checks  
- `POST /generate` to generate text from a given prompt (protected by an API key header)

## Features

- FastAPI backend with Pydantic schemas
- Hugging Face `transformers` pipeline for text generation (`distilgpt2`)
- Simple API key authentication via `x-api-key` header
- Dockerized with a multi-stage build for smaller images

## Project Structure

```text
.
├── app
│   ├── __init__.py
│   ├── main.py          # FastAPI app entrypoint
│   ├── routes.py        # /health and /generate routes
│   ├── model_provider.py# LLMProvider using transformers.pipeline
│   ├── auth.py          # verify_token using x-api-key
│   ├── config.py        # settings loaded from env vars
│   └── schemas.py       # PromptRequest, LLMResponse models
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md

## Requirements

Python 3.10

pip

Docker (if you want to run via container)

Main Python dependencies (from requirements.txt) typically include:

fastapi

uvicorn[standard]

transformers

torch

python-dotenv

## Environment Variables

Create a .env file in the project root:


API_KEY=your_dummy_api_key
MODEL_NAME=distilgpt2
MAX_NEW_TOKENS=64
APP_NAME=LLM API
API_KEY: value required in x-api-key header for /generate

MODEL_NAME: Hugging Face model name (default distilgpt2)

MAX_NEW_TOKENS: default max new tokens if not provided in the request

APP_NAME: optional FastAPI title

## Running Locally (without Docker)

Create and activate a virtual environment, install dependencies, then run uvicorn:

pip install -r requirements.txt

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
The API will be available at http://127.0.0.1:8000.

Health Check

curl -X GET "http://127.0.0.1:8000/health"

Expected response:

json
{
  "status": "ok",
  "message": "service is running"
}

Generate Text

curl -X POST "http://127.0.0.1:8000/generate" ^
  -H "Content-Type: application/json" ^
  -H "x-api-key: your_dummy_api_key" ^
  -d "{\"prompt\": \"Explain blockchain in simple terms:\", \"max_new_tokens\": 64}"

Example response:

json
{
  "generated_text": "Explain blockchain in simple terms: ..."
}

Docker Usage
Build Image
From the project root:

docker build -t llm-api .

Run Container
Make sure .env is in the same directory where you run this command:

docker run --rm -p 8000:8000 --env-file .env llm-api
-p 8000:8000: maps container port 8000 to host port 8000

--env-file .env: passes environment variables into the container

--rm: removes container when it stops

Test Inside Docker
With the container running, from the host:

curl -X GET "http://127.0.0.1:8000/health"

curl -X POST "http://127.0.0.1:8000/generate" \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_dummy_api_key" \
  -d '{"prompt": "Explain blockchain in simple terms:", "max_new_tokens": 64}'

## Authentication

The /generate endpoint is protected by a simple API key:

Header: x-api-key

Value: must match API_KEY from .env

If the header is missing or incorrect, the API will return an error.

## Notes

The first call to /generate will download and load distilgpt2 if it is not present yet, which can take some time.

max_new_tokens is an upper limit; the model may generate fewer tokens depending on context and sampling parameters.

This project is intended as a minimal example of serving a small LLM with FastAPI and Docker.