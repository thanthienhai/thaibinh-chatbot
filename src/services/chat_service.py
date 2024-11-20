import anthropic
from src.config.settings import settings
from src.core.vector_store import VectorStoreManager
from src.models.schemas import ChatRequest, ChatResponse

class ChatService:
    def __init__(self, vector_store: VectorStoreManager):
        self.vector_store = vector_store
        self.client = anthropic.Anthropic(
            api_key=settings.ANTHROPIC_API_KEY
        )
    
    async def get_answer(self, chat_request: ChatRequest) -> ChatResponse:
        # Get relevant context
        context = await self.vector_store.similarity_search(chat_request.message)
        
        # Create prompt
        prompt = self._create_prompt(
            query=chat_request.message,
            context=context,
            history=chat_request.history
        )
        
        # Get response from Claude
        response = await self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return ChatResponse(
            answer=response.content,
            context=context
        )
    
    def _create_prompt(self, query: str, context: list, history: Optional[ChatHistory]) -> str:
        prompt = f"""Context: {context}

Query: {query}

Please provide a clear and concise answer based on the given context."""
        return prompt