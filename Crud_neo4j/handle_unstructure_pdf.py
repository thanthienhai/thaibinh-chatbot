import getpass
import os
from langchain_unstructured import UnstructuredLoader
import json
import pytesseract


# if "UNSTRUCTURED_API_KEY" not in os.environ:
#     os.environ["UNSTRUCTURED_API_KEY"] = getpass.getpass("Unstructured API Key:")
os.environ['TESSDATA_PREFIX'] = "/opt/homebrew/share/"

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
file_path = "/Users/admin/Working/thaibinh-chatbot/Crud_neo4j/input/02 CT_Chuong trinh cong tac HSV 2024 - 2025.pdf"

def chunk_text(filename):

    # Check if the file is a PDF
    _, file_extension = os.path.splitext(filename)
    if file_extension.lower() != '.pdf':
        raise ValueError("Only PDF files are supported.")
    
    loader_local = UnstructuredLoader(
        file_path=file_path,
        strategy="hi_res",
        languages=["vie"],
        new_after_n_chars=700,
        max_characters=1024,
        overlap=200,
        # split_pdf_page= True,
        # split_pdf_allow_failed= True,
        chunking_strategy="basic",
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


    return serializable_docs

# Save to JSON file
# chunk_docs = chunk_text(file_path)
# with open('docs_local6.json', 'w', encoding='utf-8') as file:
#     json.dump(chunk_docs, file, ensure_ascii=False, indent=4)