from langchain.text_splitter import RecursiveCharacterTextSplitter

class TextSplitterManager:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def split_text(self, text: str) -> list[str]:
        return self.splitter.split_text(text)