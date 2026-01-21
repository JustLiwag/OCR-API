from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import subprocess, uuid, os

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/ocr/pdf")
async def ocr_pdf(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    input_pdf = f"{UPLOAD_DIR}/{job_id}.pdf"
    output_pdf = f"{OUTPUT_DIR}/{job_id}_ocr.pdf"

    with open(input_pdf, "wb") as f:
        f.write(await file.read())

    subprocess.run([
        "ocrmypdf",
        "--deskew",
        "--rotate-pages",
        "--clean",
        input_pdf,
        output_pdf
    ], check=True)

    return {
        "job_id": job_id,
        "download_url": f"/ocr/result/{job_id}"
    }

@app.get("/ocr/result/{job_id}")
def download(job_id: str):
    path = f"{OUTPUT_DIR}/{job_id}_ocr.pdf"
    return FileResponse(path, media_type="application/pdf")
