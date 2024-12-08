# utils.py

import os
import io
from typing import List, Optional
import pdfplumber
from docx import Document
import tempfile
import subprocess
import uuid
import asyncio

def extract_text_from_file(file: bytes, filename: str) -> List[dict]:
    ext = os.path.splitext(filename)[1].lower()
    if ext in [".txt", ".md"]:
        text = file.decode("utf-8", errors="replace")
        return [{"page_number": None, "text": text}]
    elif ext == ".pdf":
        return extract_text_from_pdf(file)
    elif ext == ".docx":
        return asyncio.run(extract_text_from_docx_with_layout(file))
    else:
        # Unsupported or missing dependencies
        # In a real scenario, raise an exception or handle gracefully
        text = file.decode("utf-8", errors="replace")
        return [{"page_number": None, "text": text}]

def extract_text_from_pdf(file: bytes) -> List[dict]:
    with pdfplumber.open(io.BytesIO(file)) as pdf:
        page_texts = []
        for page_idx, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            page_texts.append({"page_number": page_idx, "text": text})
    return page_texts

async def extract_text_from_docx_with_layout(file: bytes) -> List[dict]:
    loop = asyncio.get_event_loop()
    with tempfile.TemporaryDirectory() as tmpdir:
        docx_path = os.path.join(tmpdir, "temp.docx")
        pdf_path = os.path.join(tmpdir, "temp.pdf")
        with open(docx_path, "wb") as f:
            f.write(file)
        
        # Convert .docx to .pdf using LibreOffice (blocking operation)
        await loop.run_in_executor(None, subprocess.run, ["libreoffice", "--headless", "--convert-to", "pdf", docx_path, "--outdir", tmpdir], {"check": True})
        
        # Now extract text using pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            page_texts = []
            for page_idx, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                page_texts.append({"page_number": page_idx, "text": text})
    return page_texts

def chunk_text_with_page_info(page_texts: List[dict], chunk_size: int = 1000, overlap: int = 200) -> List[dict]:
    """
    Given a list of pages with text, chunk the text from each page and preserve page_number.
    Overlapping chunks are created by using an overlap parameter.

    Returns a list of dicts:
    [
      {"chunk_id": "chunk_0", "text": "First 1000 chars...", "order": 0, "page_number": 1},
      {"chunk_id": "chunk_1", "text": "Next 1000 chars...", "order": 1, "page_number": 1},
      ...
    ]
    """
    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk_size to avoid infinite loops.")

    chunks = []
    order = 0
    step = chunk_size - overlap  # How far we move forward for the next chunk start

    for page in page_texts:
        text = page["text"]
        page_number = page["page_number"]

        # Iterate using the step size to create overlapping chunks
        for i in range(0, len(text), step):
            chunk_text = text[i:i+chunk_size]
            if not chunk_text:
                break

            chunk_id = f"chunk_{order}"
            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_text,  # Ensure the key is "text"
                "order": order,
                "page_number": page_number
            })
            order += 1

    return chunks