# Service_upload.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
import os, shutil, httpx
import httpx
from reportlab.pdfgen import canvas
from io import BytesIO
from xhtml2pdf import pisa
import markdown2


app = FastAPI()
# router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# limit to 5mb
MAX_FILE_SIZE_MB = 5  
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# FORWARD_URL = "http://127.0.0.1:8001/parse_resume/"


FORWARD_URL = os.getenv("FORWARD_URL", "http://parse:8001/parse_resume/")  # default fallback
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/uploads")


if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
    
@app.get("/health")
def health_check():
    return {"status": "Service_upload healthy"}


@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    try:
        # Read file content into memory
        contents = await file.read()

        if len(contents) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Limit is {MAX_FILE_SIZE_MB} MB."
            )

        # Forward the file 
        files = {
            'file': (file.filename, contents, file.content_type)
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(FORWARD_URL, files=files)

        # Try to parse the forwarded response as JSON
        try:
            forward_data = response.json()
        except Exception:
            forward_data = {
                "error": "Invalid JSON response from forward target",
                "raw_response": response.text
            }

        return JSONResponse(
            content={
                "message": "File forwarded successfully",
                "forward_response": forward_data
            },
            status_code=response.status_code
        )

    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

class ResumeContent(BaseModel):
    text: str  

@app.post("/pdf")
async def generate_pdf(content: ResumeContent):
    try:
        # Convert markdown to HTML
        html_content = markdown2.markdown(content.text)

        # Generate PDF in memory
        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(src=html_content, dest=pdf_buffer)

        if pisa_status.err:
            return {"message": "Error during PDF generation."}

        pdf_buffer.seek(0)
        return Response(
            content=pdf_buffer.getvalue(),
            media_type="application/pdf",
            headers={
                "Content-Disposition": 'inline; filename="enhanced_resume.pdf"'
            }
        )
    except Exception as e:
        return {"message": f"Error: {str(e)}"}