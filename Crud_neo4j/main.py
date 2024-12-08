# main.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from neo4j_client import Neo4jClient
from utils import extract_text_from_file, chunk_text_with_page_info
import tempfile
import asyncio
import logging
from contextlib import asynccontextmanager
from handle_unstructure_pdf import chunk_text
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    logger.info("Starting up and ensuring Neo4j connection is ready.")
    yield
    # Clean up the ML models and release the resources
    logger.info("Shutting down and closing Neo4j connection.")
    neo4j_client.close()


app = FastAPI(lifespan=lifespan)

# For demo: CORS to allow Streamlit frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the async Neo4jClient
neo4j_client = Neo4jClient()


@app.post("/files")
async def create_file(file: UploadFile = File(...)):
    try:
        # Extract text
        file_bytes = await file.read()
        page_texts = extract_text_from_file(file_bytes, file.filename)
        if not any(pt["text"].strip() for pt in page_texts):
            raise HTTPException(status_code=400, detail="File contains no extractable text")

        # Chunk text with overlap
        chunks = chunk_text(file.filename)

        # Store in Neo4j
        file_id = await neo4j_client.create_file_with_chunks(file.filename, chunks)
        return {"file_id": file_id, "filename": file.filename, "chunk_count": len(chunks)}
    except Exception as e:
        # Log the exception (you can integrate a logging system)
        logger.error(f"Error in create_file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files")
async def list_files():
    try:
        files = await neo4j_client.list_files()
        return files
    except Exception as e:
        logger.error(f"Error in list_files: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/{file_id}/chunks")
async def get_file_chunks(file_id: str):
    try:
        chunks = await neo4j_client.get_chunks_by_file(file_id)
        if not chunks:
            raise HTTPException(status_code=404, detail="File not found")
        return chunks
    except Exception as e:
        logger.error(f"Error in get_file_chunks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/files/{file_id}")
async def delete_file(file_id: str):
    try:
        await neo4j_client.delete_file(file_id)
        return {"message": f"File {file_id} deleted"}
    except Exception as e:
        logger.error(f"Error in delete_file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

# uvicorn main:app --host 0.0.0.0 --port 8081 --reload

# uvicorn main:app --host 0.0.0.0 --port 8081 --reload