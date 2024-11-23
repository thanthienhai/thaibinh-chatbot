from src.core.chunking import TextSplitterManager
from src.core.vector_store import VectorStoreManager
from src.models.schemas import Document

class DocumentService:
    def __init__(
        self,
        text_splitter: TextSplitterManager,
        vector_store: VectorStoreManager
    ):
        self.text_splitter = text_splitter
        self.vector_store = vector_store
    
    async def process_document(self, document: Document):
        # Split document into chunks
        chunks = self.text_splitter.split_text(document.content)
        
        # Store in vector store
        await self.vector_store.init_store(chunks)
        
        return len(chunks)