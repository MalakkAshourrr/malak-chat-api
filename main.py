from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Optional
import requests

app = FastAPI()

GROQ_API_KEY = "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"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

MODEL = "openai/gpt-oss-120b"

class ChatRequest(BaseModel):
    question: str


@app.post("/v1/malak-chat")
def malak_chat(
    request: ChatRequest,
    authorization: Optional[str] = Header(default=None)
):

    # Authentication Check
    if authorization != "Malak":
        return {
            "status": "Error",
            "status_code": 403,
            "error_message": "Invalid authentication credentials",
            "answer": None
        }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": request.question
            }
        ]
    }

    response = requests.post(
        GROQ_URL,
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        return {
            "status": "Error",
            "status_code": response.status_code,
            "error_message": response.text,
            "answer": None
        }

    data = response.json()

    answer = data["choices"][0]["message"]["content"]

    return {
        "status": "success",
        "status_code": 200,
        "error_code": 0,
        "error_message": "",
        "answer": answer
    }
