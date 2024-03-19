# ProtonDatalabs AI developer Assignment - Chatbot application

## Clone the repository

https://github.com/kazutokidigaya/ai-assign.git

## Install dependencies:

In this project you find 2 directories `backend` & `frontend`

for `backend` open a new terminal and paste the following commands:

1.  cd backend
2.  pip install -r requirements.txt
3.  create a .env file 
4.  inside env specify your OpenAI key :  OPENAI_API_KEY="####Your-KEY####"
5.  uvicorn main:app --reload

for `frontend` open a new terminal and paste the following commands:

1.  cd frontend
2.  npm i
4.  npm run start

## Backend dependencies:

we are using

PyMuPDF,python-docx, pandas - extracting text from uploaded file for CSV, Docx,txt & PDF format
openai - model gpt-3.5-turbo for response generation
uvicorn - to run our server locally without the need to reload after doing any change in our code

## frontend dependencies:

we are using

PyMuPDF - extracting text from uploaded pdf
openai - model gpt-3.5-turbo for response generation
uvicorn - to run our server locally without the need to reload after doing any change in our code
