<h2>
  <img src="https://github.com/user-attachments/assets/c11fe6a7-2c34-413b-904a-de914b4945a2" alt="logo" width="30"/>
  NextGenCV
</h2>

-----------

NextGenCV is an AI-powered application designed to parse, enhance, and generate professional, redesigned resumes in one click. It leverages **Groq API (LLaMA 3)** for rewriting, FastAPI microservices for backend orchestration, and a React frontend for a smooth user experience.

---
## Demo

https://youtu.be/Cxaj3XZkgtc


----
## Architecture

<img src="https://github.com/user-attachments/assets/c230ef4e-2e45-4eb2-aeb7-363d9aeebca2" alt="NextGenCVArch" width="500"/>



## 💡 Description

- Upload a resume as a PDF, DOCX, or text file.
- Automatically parse the resume text.
- Enhance the content using advanced AI (Groq LLaMA 3).
- Preview the enhanced resume directly in the web UI.
- Download as a polished PDF ready to share.

---

## ⚙️ Features

- AI-driven resume enhancement (Groq LLaMA 3).
- Clean, user-friendly React interface.
- Downloadable enhanced PDF with professional formatting.
- Microservice architecture using FastAPI (Upload, Parse, Enhance).
- Dockerized services for easy deployment.
- Nginx proxy to unify services and handle routing.

---

## 🧑‍💻 Technologies Used

- **Backend:** FastAPI, Python, PyMuPDF (fitz), httpx, xhtml2pdf, markdown2, ReportLab.
- **Frontend:** React, JavaScript, CSS.
- **AI:** Groq API (LLaMA 3 model).
- **Infrastructure:** Docker, Docker Compose, Nginx.

---

## 🚀 How to Start

### 1️⃣ Clone the repository

```bash
git clone https://github.com/EASS-HIT-PART-A-2025-CLASS-VII/NextGenCV.git
cd NextGenCV
```

---

### 2️⃣ Add your Groq API key

Create an API key at [Groq Console](https://console.groq.com/keys).

Edit `docker-compose.yml`:

```yaml
  environment:
    - GROQ_API_KEY=**YOUR_SECRET_KEY_HERE**
    - GROQ_URL=https://api.groq.com/openai/v1/chat/completions
    - UPLOAD_DIR=/uploads
    - GENERATED_DIR=/generated_pdfs
```

---

### 3️⃣ Build and run with Docker

```bash
docker compose up --build
```

---

### 4️⃣ Access the application

Visit: [http://localhost:80](http://localhost:80)

---

## 🌐 Base URLs

| Service         | URL                      |
|-----------------|--------------------------|
| Frontend (React)| `http://localhost:80`   |
| Upload API      | `http://localhost:80/upload` |
| PDF Generation  | `http://localhost:80/pdf` |
| Health Checks   | `/health` on each service |

---

## 🗂️ Microservices Overview

### Upload Service

- Handles file uploads.
- Validates file size (max 5 MB).
- Forwards to Parse Service.

### Parse Service

- Extracts text from PDF.
- Forwards text to Enhance Service.

### Enhance Service

- Uses Groq LLaMA 3 to rewrite resume text.
- Returns enhanced resume content.

---
## 🗂️ File Structure

```
NextGenCV
├── Backend
│   ├── enhance
│   │   ├── Dockerfile.enhance
│   │   ├── requirements.enhance.txt
│   │   └── Service_enhance.py
│   ├── parse
│   │   ├── Dockerfile.parse
│   │   ├── requirements.parse.txt
│   │   └── Service_parse.py
│   └── upload
│       ├── Dockerfile.upload
│       ├── requirements.upload.txt
│       └── Service_upload.py
├── Frontend
│   └── my-app
│       ├── Dockerfile
│       ├── package.json
│       ├── public
│       └── src
│           ├── App.js
│           ├── NextGenCV.jsx
│           └── ...
├── docker-compose.yml
├── nginx.conf
```

---

## 💬 Example Usage Flow

1. Upload your resume via the web UI.
2. Wait for parsing and enhancement.
3. Preview the enhanced resume on the page.
4. Download the final PDF directly.

---

## 💥 Important Notes

- Use a valid **Groq API key**, otherwise enhancement will fail.
- All microservices communicate internally via Docker network.

---

## 👨‍🏫 Contributors

- Sapir Shenhav

---

## 📄 License

This project is for academic and educational use.




