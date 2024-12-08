import getpass
import os
from langchain_unstructured import UnstructuredLoader
import json
import pytesseract


if "UNSTRUCTURED_API_KEY" not in os.environ:
    os.environ["UNSTRUCTURED_API_KEY"] = getpass.getpass("Unstructured API Key:")
os.environ['TESSDATA_PREFIX'] = "/opt/homebrew/share/"

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
file_path = "/Users/admin/Working/thaibinh-chatbot/Crud_neo4j/input/Quyết định ban hành Quy chế nhà giáo trẻ tiêu biêu.docx"
loader_local = UnstructuredLoader(
    file_path=file_path,
    strategy="hi_res",
    ocr_languages=["vie"],
    
)
docs_local = []
for doc in loader_local.lazy_load():
    print(doc)
    docs_local.append(doc)

serializable_docs = [
    {
        "page_content": doc.page_content,
        "metadata": doc.metadata
    }
    for doc in docs_local
]

# Save to JSON file
with open('docs_local2.json', 'w', encoding='utf-8') as file:
    json.dump(serializable_docs, file, ensure_ascii=False, indent=4)
