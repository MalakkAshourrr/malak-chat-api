from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

app = FastAPI()

loader = PyMuPDFLoader(r"C:\Users\user\Downloads\test.pdf")

documents = loader.load()
splitter = RecursiveCharacterTextSplitter(

    chunk_size=500,

    chunk_overlap=100

)

docs = splitter.split_documents(documents)
embedding = HuggingFaceEmbeddings(

    model_name="sentence-transformers/all-MiniLM-L6-v2"

)
db = FAISS.from_documents(

    docs,

    embedding

)
retriever = db.as_retriever(

    search_kwargs={

        "k":3

    }

)
llm = ChatOpenAI(

    model="Aurai-3.0",

    api_key="apiVohnE",

    base_url="https://api-pilot-sandbox.aurai.solutions/v1"

)
template = """

You are an AI assistant.

Use ONLY the context below.

Do NOT use your own knowledge.

If the answer cannot be found in the context, reply exactly:

"The answer is not available in the document."

Context:

{context}

Question:

{question}

Answer:

"""
prompt = PromptTemplate(

    template=template,

    input_variables=[

        "context",

        "question"

    ]

)
qa = RetrievalQA.from_chain_type(

    llm=llm,

    retriever=retriever,

    chain_type="stuff",

    chain_type_kwargs={

        "prompt":prompt

    }

)
class Question(BaseModel):

    question:str
    
@app.post("/ask")

def ask(data:Question):

    answer = qa.invoke(

        {

            "query":data.question

        }

    )

    return answer
