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
DEFAULT_INSTRUCTIONS = """
You are a helpful AI assistant.

Instructions:
- Answer ONLY using the attached document.
- If the answer is not found in the document, say:
"The answer is not available in the attached document."
"""

def ask_llm(question, document, instructions):

    prompt = f"""
    
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
                "role": "system",
                "content": instructions
            },
            {
                "role": "user",
                "content": f"""
    Document:
    {document}

    Question:
    {question}
    """
            }
        ]
    )

    return response.choices[0].message.content
# -----------------------
# Endpoint
# -----------------------
@app.post("/v1/malak-chat")
def malak_chat(
    instructions: Optional[str] = Form(default=None),
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

    final_instructions = instructions or DEFAULT_INSTRUCTIONS

    answer = ask_llm(
        question,
        document,
        final_instructions
    )

    return {
        "status": "success",
        "status_code": 200,
        "error_code": 0,
        "error_message": "",
        "answer": answer
    }
