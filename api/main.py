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
def pdfpipeline(file_path: Doc_data):
    try:
        if not file_path.resume_link.endswith('.pdf'):
            return {"error": "Invalid file format. Only PDF files are supported."}
        
        response = requests.get(file_path.resume_link, timeout=30)
        response.raise_for_status()
        
        pdf_file = BytesIO(response.content)
        with pdfplumber.open(pdf_file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            if not text.strip():
                return {"error": "No text found in PDF"}
            
            return {"data":text.strip()}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to download PDF: {str(e)}"}
    except Exception as e:
        return {"error": f"Error processing PDF: {str(e)}"}