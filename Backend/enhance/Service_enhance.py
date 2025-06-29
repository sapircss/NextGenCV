# Service_enhance.py

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import fitz  # PyMuPDF
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import markdown2
from xhtml2pdf import pisa

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = os.getenv("GROQ_URL")




    
class ResumeContent(BaseModel):
    text: str
    

@app.get("/health")
def health_check():
    return {"status": "Service_enhance healthy"}


@app.post("/enhance_resume/")
async def enhance_resume(content: ResumeContent):
    print(GROQ_API_KEY)
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {
    "role": "system",
   "content": (
    "You are a professional and highly experienced resume writer. "
    "Transform the provided resume text into an enhanced, detailed, and compelling resume. "
    "Expand responsibilities with detail, quantify achievements, and use strong action verbs and keywords. "
    "**IMPORTANT:** Absolutely do NOT add any introductions, disclaimers, or phrases like 'Here is', 'Below is', or 'The following'. "
    "Return ONLY the pure rewritten resume content. No preamble, no headings, no extra lines."
    )
},
                {"role": "user", "content": content.text}
            ]
        }
        response = requests.post(GROQ_URL, json=payload, headers=headers)
        response.raise_for_status()

        enhanced_text = response.json()['choices'][0]['message']['content'].strip()
        return {"enhanced_text": enhanced_text}
    
    except Exception as e:
        print(f"Enhancement error: {str(e)}")
        return {"message": f"Enhancement failed: {str(e)}"}
    
    

