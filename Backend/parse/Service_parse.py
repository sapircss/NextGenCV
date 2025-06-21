from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import fitz  # PyMuPDF
import os
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
import httpx


# UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/uploads")
ENHANCE_URL=os.getenv("ENHANCE_URL", "http://enhance:8002/enhance_resume/")
# ENHANCE_URL = "http://127.0.0.1:8002/enhance_resume/" 

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Resume(BaseModel):
    file_path: str
    
@app.get("/health")
def health_check():
    return {"status": "Service_parse healthy"}






@app.post("/parse_resume/")
async def parse_resume(file: UploadFile = File(...)):
    try:
        # Read file into memory
        contents = await file.read()

        # Open PDF directly from memory buffer
        text = ""
        with fitz.open(stream=contents, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()

        if not text.strip():
            return JSONResponse(content={"message": "No text extracted from the resume."}, status_code=400)

        # Forward extracted text to enhance server
        async with httpx.AsyncClient() as client:
            enhance_response = await client.post(ENHANCE_URL, json={"text": text})

        if enhance_response.status_code != 200:
            return JSONResponse(
                content={
                    "message": "Enhancement failed",
                    "details": enhance_response.text
                },
                status_code=enhance_response.status_code
            )

        enhanced = enhance_response.json().get("enhanced_text", "No content returned.")

        return {
            "message": "Resume parsed and enhanced successfully.",
            "enhanced_text": enhanced
        }

    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)


# @app.post("/parse_resume/")
# async def parse_resume(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         temp_path = os.path.join(UPLOAD_DIR, file.filename)
#         with open(temp_path, "wb") as f:
#             f.write(contents)

#         text = ""
#         with fitz.open(temp_path) as doc:
#             for page in doc:
#                 text += page.get_text()

#         if not text.strip():
#             return JSONResponse(content={"message": "No text extracted from the resume."}, status_code=400)

#         # Forward to enhance server
#         async with httpx.AsyncClient() as client:
#             enhance_response = await client.post(ENHANCE_URL, json={"text": text})

#         if enhance_response.status_code != 200:
#             return JSONResponse(
#                 content={"message": "Enhancement failed", "details": enhance_response.text},
#                 status_code=enhance_response.status_code
#             )

#         enhanced = enhance_response.json().get("enhanced_text", "No content returned.")

#         return {
#             "message": "Resume parsed and enhanced successfully.",
#             "enhanced_text": enhanced
#         }

#     except Exception as e:
#         return JSONResponse(content={"message": str(e)}, status_code=500)
