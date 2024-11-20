# Thái Bình - Chatbot

## Cấu trúc thư mục
```bash
thaibinh-chatbot/
├── .env.example
├── README.md
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── embeddings.py
│   │   ├── text_splitter.py
│   │   └── vector_store.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat_service.py
│   │   └── document_service.py
│   └── api/
│       ├── __init__.py
│       ├── deps.py
│       └── routes/
│           ├── __init__.py
│           ├── chat.py
│           └── document.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_chat.py
```