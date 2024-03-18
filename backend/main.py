from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fitz  
from openai import OpenAI

from dotenv import load_dotenv
import os


load_dotenv()
client = OpenAI()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



OpenAI.api_key = os.getenv('OPENAI_API_KEY') 


class ChatCompletionResponse(BaseModel):
    result: str



async def extract_text_from_pdf(file: UploadFile) -> str:
    try:
        content = await file.read()
        text = ""
        with fitz.open(stream=content, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {e}")


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


@app.post("/predict", response_model=ChatCompletionResponse)
async def predict(question: str = Form(...), file: UploadFile = File(...)):
    extracted_text = await extract_text_from_pdf(file)
   
    response_text = await query_openai(extracted_text, question)
    return {"result": response_text}
