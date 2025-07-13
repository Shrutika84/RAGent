from fastapi import APIRouter, UploadFile, File
from typing import List
import shutil
import os
from app.rag import load_and_index_documents
from app.config import settings

router = APIRouter()

@router.post("/")
async def upload_documents(files: List[UploadFile] = File(...)):
    saved_files = []

    # Create directory
    os.makedirs(os.path.dirname(settings.DOC_EMBED_CSV), exist_ok=True)

    for file in files:
        file_path = os.path.join(os.path.dirname(settings.DOC_EMBED_CSV), file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file.filename)

        if file.filename.endswith(".csv"):
            settings.DOC_EMBED_CSV = file_path

    # indexing
    load_and_index_documents()

    return {"message": f"{len(saved_files)} file(s) uploaded and indexed.", "files": saved_files}
