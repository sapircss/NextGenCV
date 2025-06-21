from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from io import BytesIO
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import markdown2
from xhtml2pdf import pisa

app = FastAPI()

GENERATED_DIR = "./generated"  # make sure this folder exists!

class ResumeContentg(BaseModel):
    text: str  # This will be Markdown text!
    file_path: str = None  # Not needed anymore, but kept if you want it.

@app.post("/generate_pdf/")
async def generate_pdf(content: ResumeContentg):
    try:
        # Create output path
        output_path = os.path.join(GENERATED_DIR, "enhanced_resume.pdf")
        
        # 1. Convert Markdown to HTML
        html_content = markdown2.markdown(content.text)

        # 2. Create PDF from HTML
        with open(output_path, "w+b") as result_file:
            pisa_status = pisa.CreatePDF(
                src=html_content,
                dest=result_file
            )

        if pisa_status.err:
            return {"message": "Error during PDF generation."}

        return FileResponse(output_path, filename="enhanced_resume.pdf", media_type='application/pdf')

    except Exception as e:
        return {"message": f"Error: {str(e)}"}
