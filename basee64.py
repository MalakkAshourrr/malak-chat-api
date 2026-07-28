from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    api_key="api_gAAAAABqV53NXXTPzmZ-4KS2gqrPaRUvT_lgMHDmePjtNPk2JXQBW53cPtkhwBtKyt0a42O2DVQqLKnbp2zy2sIa0qphBhXiK4mEa2tOGmOG_J2Gb3quyU4R6cKrYlrRFuOS0hBVohnE",
    base_url="https://api-pilot-sandbox.aurai.solutions/v1"
)

DEFAULT_INSTRUCTIONS = """
You are a helpful AI assistant.

Instructions:
- Answer ONLY using the attached PDF.
- If the answer is not found in the PDF, say:
"The answer is not available in the attached document."
"""

class ChatRequest(BaseModel):
    question: str
    pdf_base64: str
    instructions: Optional[str] = None


@app.post("/v1/malak-chat")
def malak_chat(
    request: ChatRequest,
    authorization: Optional[str] = Header(default=None)
):

    if authorization != "Malak":
        return {
            "status": "Error",
            "status_code": 403,
            "error_message": "Invalid authentication credentials",
            "answer": None
        }

    instructions = request.instructions or DEFAULT_INSTRUCTIONS

    response = client.chat.completions.create(
        model="Aurai-3.0",
        messages=[
            {
                "role": "system",
                "content": instructions
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "file",
                        "file": {
                            "filename": "document.pdf",
                            "file_data": f"data:application/pdf;base64,{request.pdf_base64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": request.question
                    }
                ]
            }
        ]
    )

    return {
        "status": "success",
        "status_code": 200,
        "answer": response.choices[0].message.content
    }
