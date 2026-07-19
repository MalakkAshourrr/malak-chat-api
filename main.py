from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


# -----------------------
# Request Model
# -----------------------
class ChatRequest(BaseModel):
    question: str


# -----------------------
# Success Response
# -----------------------
class SuccessResponse(BaseModel):
    status: str
    status_code: int
    error_code: int
    error_message: str
    answer: str


# -----------------------
# Error Response
# -----------------------
class ErrorResponse(BaseModel):
    status: str
    status_code: int
    error_message: str
    answer: Optional[str] = None


# -----------------------
# Endpoint
# -----------------------
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

    # Your AI Logic
    answer = f"You asked: {request.question}"

    return {
        "status": "success",
        "status_code": 200,
        "error_code": 0,
        "error_message": "",
        "answer": answer
    }
