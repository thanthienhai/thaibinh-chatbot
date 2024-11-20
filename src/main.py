from fastapi import FastAPI
from src.config.settings import settings
from src.api.routes import chat, document

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(chat.router, prefix=settings.API_V1_STR)
app.include_router(document.router, prefix=settings.API_V1_STR)