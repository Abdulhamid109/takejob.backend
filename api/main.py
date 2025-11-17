from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from io import BytesIO
import pdfplumber

 
app = FastAPI()

 

 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            
    allow_credentials=True,
    allow_methods=["*"],              
    allow_headers=["*"],              
)
 
class Doc_data(BaseModel):
    resume_link:str

class sumar_data(BaseModel):
    text_data:str

 
@app.get('/')
def starter():
        return {'Message':"Backend running fruitfully"}
 
@app.post('/extractresume')
def pdfpipeline(file_path:Doc_data):
  try:
    if file_path.resume_link.endswith('.pdf'):
      response = requests.get(file_path.resume_link)
      response.raise_for_status()  
 
      pdf_file = BytesIO(response.content)
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
                text += page.extract_text() or ""
        return text
  except Exception as e:
      return f"Error: {str(e)}"
  

