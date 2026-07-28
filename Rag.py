from fastapi import FastAPI, UploadFile, File, Form, Header
from typing import Optional
from openai import OpenAI
import fitz

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# -----------------------------
# Groq Client
# -----------------------------
client = OpenAI(
    api_key="api_gAAAAABqV53NXXTPzmZ-4KS2gqrPaRUvT_lgMHDmePjtNPk2JXQBW53cPhBVohnE",
    base_url="https://api-pilot-sandbox.aurai.solutions/v1"
)

# -----------------------------
# Embedding Model
# -----------------------------
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------------
# Instructions
# -----------------------------
DEFAULT_INSTRUCTIONS = """
You are a helpful AI assistant.

Rules:

1. Answer ONLY using the provided context.
2. If the answer is not found say:

"The answer is not available in the document."

3. Don't make up information.
"""

# -----------------------------
# Extract PDF
# -----------------------------
def extract_pdf_text(pdf):

    document = fitz.open(
        stream=pdf.read(),
        filetype="pdf"
    )

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text

# -----------------------------
# Chunking
# -----------------------------
def split_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(
            text[i:i+chunk_size]
        )

    return chunks

# -----------------------------
# Embeddings
# -----------------------------
def create_embeddings(chunks):

    return embedding_model.encode(chunks)

# -----------------------------
# Similarity Search
# -----------------------------
def retrieve_context(question, chunks, embeddings):

    question_embedding = embedding_model.encode(
        [question]
    )

    scores = cosine_similarity(
        question_embedding,
        embeddings
    )[0]

    best_index = scores.argmax()

    return chunks[best_index]

# -----------------------------
# Ask Groq
# -----------------------------
def ask_llm(question, context, instructions):

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

Context:

{context}


Question:

{question}

"""
            }

        ]

    )

    return response.choices[0].message.content

# -----------------------------
# Endpoint
# -----------------------------
@app.post("/v1/malak-chat")
def chat(

        question: str = Form(...),

        pdf: UploadFile = File(...),

        instructions: Optional[str] = Form(None),

        authorization: Optional[str] = Header(None)

):

    if authorization != "Malak":

        return {

            "status": "Error",

            "status_code": 403,

            "answer": None

        }

    text = extract_pdf_text(pdf.file)

    chunks = split_text(text)

    embeddings = create_embeddings(chunks)

    context = retrieve_context(
        question,
        chunks,
        embeddings
    )

    final_instructions = (
        instructions
        or DEFAULT_INSTRUCTIONS
    )

    answer = ask_llm(

        question,

        context,

        final_instructions

    )

    return {

        "status": "success",

        "status_code": 200,

        "context_used": context,

        "answer": answer

    }
