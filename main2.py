from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Optional
import requests

app = FastAPI()

# -----------------------
# Groq Configuration
# -----------------------
GROQ_API_KEY = "api_gAA"

GROQ_URL = "https://api-pilot-sandbox.aurai.solutions/v1/chat/completions"

MODEL = "Aurai-3.0"


# -----------------------
# Request Model
# -----------------------
class ChatRequest(BaseModel):
    question: str
    instructions: Optional[str] = None


# -----------------------
# Endpoint
# -----------------------
@app.post("/v1/malak-chat")
def malak_chat(
    request: ChatRequest,
    authorization: Optional[str] = Header(default=None)
):

    # Authentication Check
    if authorization != "Malakk":
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
            "role": "system",
            "content": request.instructions or "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "What is Python?"
        },
        {
            "role": "assistant",
            "content": " your answer is Python is a programming language."
        },
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
