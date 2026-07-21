from fastapi import FastAPI, Header, Form, File, UploadFile
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI
import fitz
app = FastAPI()

# -----------------------
# AI Client
# -----------------------
client = OpenAI(
    api_key="api_gAAAAABqV53NXXTPzmZ-4KS2gqrPaRUvT_lgMHDmePjtNPk2JXQBW53cPtkhwBtKyt0a42O2DVQqLKnbp2zy2sIa0qphBhXiK4mEa2tOGmOG_J2Gb3quyU4R6cKrYlrRFuOS0hBVohnE",
    base_url="https://api-pilot-sandbox.aurai.solutions/v1"
)

# -----------------------
# Request Model
# -----------------------
class ChatRequest(BaseModel):
    question: str

# -----------------------
# LLM Function
# -----------------------


def extract_pdf_text(pdf_file):

    pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text

def ask_llm(instructions, question, document):

    prompt = f"""
    
Instructions:
{instructions}


Document:
{document}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="Aurai-3.0",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
# -----------------------
# Endpoint
# -----------------------
@app.post("/v1/malak-chat")
def malak_chat(
    instructions: str = Form(...),
    question: str = Form(...),
    pdf: UploadFile = File(...),
    authorization: Optional[str] = Header(default=None)
):

    if authorization != "Malak":
        return {
            "status": "Error",
            "status_code": 403,
            "error_message": "Invalid authentication credentials",
            "answer": None
        }

    document = extract_pdf_text(pdf.file)

    answer = ask_llm(instructions, question, document)

    return {
        "status": "success",
        "status_code": 200,
        "error_code": 0,
        "error_message": "",
        "answer": answer
    }
