import os
import base64
import zlib
import json
from typing import List, Dict, Any
import asyncio  # Import asyncio for running async functions

from unstructured_client import UnstructuredClient
from unstructured_client.models import operations, shared
from unstructured.staging.base import elements_from_dicts, elements_to_json
from PIL import Image  # Ensure Pillow is installed for image handling

# Function to extract and decompress orig_elements
def extract_orig_elements(orig_elements: str) -> str:
    decoded_orig_elements = base64.b64decode(orig_elements)
    decompressed_orig_elements = zlib.decompress(decoded_orig_elements)
    return decompressed_orig_elements.decode('utf-8')

# Asynchronous main function
async def main():
    # Define file paths
    input_filepath = "/Users/admin/Working/thaibinh-chatbot/Crud_neo4j/input/02 CT_Chuong trinh cong tac HSV 2024 - 2025.pdf"
    output_filepath = "test.json"
    
    # Initialize the UnstructuredClient with Vietnamese OCR
    client = UnstructuredClient(
        
    )
    
    # Read the input PDF file
    # try:
    #     with open(input_filepath, "rb") as f:
    #         files = shared.Files(
    #             content=f.read(),
    #             file_name=os.path.basename(input_filepath)  # Use basename for file_name
    #         )
    # except FileNotFoundError:
    #     print(f"Input file not found: {input_filepath}")
    #     return
    # except Exception as e:
    #     print(f"Error reading input file: {e}")
    #     return
    
    # # Create a PartitionRequest with desired parameters
    # req = operations.PartitionRequest(
    #     shared.PartitionParameters(
    #         files=files,
    #         strategy=shared.Strategy.HI_RES,
    #         split_pdf_page=True,
    #         split_pdf_allow_failed=True,
    #         split_pdf_concurrency_level=15,
    #         chunking_strategy="basic",
            # new_after_n_chars=200,
            # max_characters=300,
    #         languages=["vie"]
    #     )
    # )

    req = {
        "partition_parameters": {
            "files": {
                "content": open(input_filepath, "rb"),
                "file_name": os.path.basename(input_filepath),
            },
            "strategy": shared.Strategy.OCR_ONLY,
            "languages": ["vie"],
            "split_pdf_page": True,
            "split_pdf_allow_failed": True,
            "split_pdf_concurrency_level": 15
        }
    }
    
    try:
        # Perform asynchronous partitioning
        res = await client.general.partition_async(request=req)
        
        # Initialize a list to hold transposed elements
        orig_elements_dict: List[Dict[str, Any]] = []
    
        for element in res.elements:
            # Check if 'orig_elements' exists in metadata
            if "orig_elements" in element.metadata:
                # Extract and decompress 'orig_elements'
                orig_elements = extract_orig_elements(element.metadata["orig_elements"])
                # Append the transposed data to the list
                orig_elements_dict.append({
                    "element_id": element.element_id,
                    "text": element.text,
                    "orig_elements": json.loads(orig_elements)
                })
        
        # Convert the list to a JSON string with indentation
        orig_elements_json = json.dumps(orig_elements_dict, indent=2)
    
        # Write the JSON data to the output file
        with open(output_filepath, "w") as file:
            file.write(orig_elements_json)
        
        print(f"Successfully wrote output to {output_filepath}")
    
    except Exception as e:
        print(f"An error occurred during partitioning: {e}")
    finally:
        # Close the client to free resources
        await client.aclose()

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main())