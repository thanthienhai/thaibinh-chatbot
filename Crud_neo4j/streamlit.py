import streamlit as st
import requests
import math

# Adjust API URL as needed
API_URL = "http://localhost:8081"

st.title("Document Management for RAG Preparation")
if 'chunk_page' not in st.session_state:
    st.session_state.chunk_page = 1
# Sidebar actions
action = st.sidebar.selectbox("Action", ["List Files", "Upload File", "View Chunks", "Delete File"])

if action == "Upload File":
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx", "md"])
    if uploaded_file is not None:
        # Send to backend
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        resp = requests.post(f"{API_URL}/files", files=files)
        if resp.status_code == 200:
            st.success(f"File uploaded: {resp.json()['filename']}")
        else:
            st.error(f"Error uploading file: {resp.text}")

elif action == "List Files":
    resp = requests.get(f"{API_URL}/files")
    if resp.status_code == 200:
        files = resp.json()
        if files:
            # Paginate
            page_size = 5
            total = len(files)
            page = st.number_input("Page", min_value=1, value=1, step=1)
            start = (page - 1)*page_size
            end = start+page_size
            for f in files[start:end]:
                st.write(f"**File ID**: {f['file_id']}\n")
            total_pages = math.ceil(total/page_size)
            st.write(f"Page {page} of {total_pages}")
        else:
            st.write("No files found.")
    else:
        st.error("Failed to retrieve files.")

if action == "View Chunks":
    st.header("View Chunks of a File")
    file_id = st.text_input("Enter File ID")
    
    if st.button("View Chunks") and file_id:
        resp = requests.get(f"{API_URL}/files/{file_id}/chunks")
        if resp.status_code == 200:
            chunks = resp.json()
            if chunks:
                # Define pagination parameters
                chunk_page_size = 3
                chunk_total = len(chunks)
                total_chunk_pages = math.ceil(chunk_total / chunk_page_size)
                
                # Display current page
                st.write(f"Page {st.session_state.chunk_page} of {total_chunk_pages}")
                
                # Calculate start and end indices
                chunk_start = (st.session_state.chunk_page - 1) * chunk_page_size
                chunk_end = chunk_start + chunk_page_size
                current_chunks = chunks[chunk_start:chunk_end]
                
                # Display chunks for the current page
                for c in current_chunks:
                    st.subheader(f"Chunk Order: {c['order']}")
                    st.text_area("Chunk Text", c['text'], height=200)
                
                # Navigation buttons
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    if st.button("Previous") and st.session_state.chunk_page > 1:
                        st.session_state.chunk_page -= 1
                with col3:
                    if st.button("Next") and st.session_state.chunk_page < total_chunk_pages:
                        st.session_state.chunk_page += 1
                
                # Optionally, reset to page 1 if file_id changes
                if 'current_file_id' not in st.session_state or st.session_state.current_file_id != file_id:
                    st.session_state.chunk_page = 1
                    st.session_state.current_file_id = file_id
                
            else:
                st.warning("No chunks found for this file.")
        else:
            st.error(f"Error fetching chunks: {resp.text}")

elif action == "Delete File":
    file_id = st.text_input("Enter File ID to delete")
    if st.button("Delete"):
        resp = requests.delete(f"{API_URL}/files/{file_id}")
        if resp.status_code == 200:
            st.success("File deleted successfully.")
        else:
            st.error(resp.text)