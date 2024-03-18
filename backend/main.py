from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fitz  # PyMuPDF for PDFs
import os
from dotenv import load_dotenv
from openai import OpenAI
import docx  # For DOCX files
import pandas as pd  # For CSV files

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize FastAPI and OpenAI client
app = FastAPI()
client = OpenAI(api_key=openai_api_key)

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for the response
class ChatCompletionResponse(BaseModel):
    result: str

# Function to extract text based on file type
async def extract_text(file: UploadFile) -> str:
    content = await file.read()
    if file.filename.endswith('.pdf'):
        return extract_text_from_pdf(content)
    elif file.filename.endswith('.docx'):
        return extract_text_from_docx(content)
    elif file.filename.endswith('.csv') or file.filename.endswith('.txt'):
        return content.decode('utf-8')
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

def extract_text_from_pdf(content: bytes) -> str:
    text = ""
    with fitz.open(stream=content, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(content: bytes) -> str:
    doc = docx.Document(content)
    return "\n".join([para.text for para in doc.paragraphs])

# Query OpenAI with the document and question
async def query_openai(document_text: str, question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[ 
                {"role": "system", "content": "This is a document:"},
                {"role": "system", "content": document_text},
                {"role": "user", "content": question}
                ],
            max_tokens=800
        )
      
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query OpenAI: {e}")


# Endpoint for making predictions
@app.post("/predict", response_model=ChatCompletionResponse)
async def predict(question: str = Form(...), file: UploadFile = File(...)):
    extracted_text = await extract_text(file)
    response_text = await query_openai(extracted_text, question)
    return {"result": response_text}


