from fastapi import APIRouter, UploadFile, File
from typing import List
import shutil
import os
from app.rag import load_and_index_documents
from app.config import settings

router = APIRouter()
ALLOWED_EXTENSIONS = {".csv", ".txt", ".pdf", ".json"}

@router.post("/")
async def upload_documents(files: List[UploadFile] = File(...)):
    saved_files = []

    # Create directory
    os.makedirs(os.path.dirname(settings.DOC_EMBED_CSV), exist_ok=True)

    for file in files:
        ext = os.path.splitext(file.filename)[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return {"error": f"Unsupported file type: {ext}. Allowed types are: {', '.join(ALLOWED_EXTENSIONS)}"}

        file_path = os.path.join(os.path.dirname(settings.DOC_EMBED_CSV), file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file.filename)

        if file.filename.endswith(".csv"):
            settings.DOC_EMBED_CSV = file_path

    # indexing
    load_and_index_documents()

    return {"message": f"{len(saved_files)} file(s) uploaded and indexed.", "files": saved_files}
