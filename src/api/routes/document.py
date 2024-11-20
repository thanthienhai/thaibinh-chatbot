from fastapi import APIRouter, Depends
from src.models.schemas import Document
from src.services.document_service import DocumentService
from src.api.deps import get_document_service

router = APIRouter()

@router.post("/documents")
async def upload_document(
    document: Document,
    document_service: DocumentService = Depends(get_document_service)
):
    chunks_count = await document_service.process_document(document)
    return {"message": f"Document processed into {chunks_count} chunks"}
