import os
from langchain_community.vectorstores import Neo4jVector
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from dotenv import load_dotenv
from llm.get_llm import get_embedding_function, get_model_function
from llm.get_graph import get_graph_function

graph = get_graph_function()
embedding_func = get_embedding_function()
model = get_model_function()
neo4j_vector_index = Neo4jVector.from_existing_graph(
    embedding_func,
    graph=graph,
    index_name="chunk_content",
    node_label="Chunk",
    text_node_properties=[
        "content",
    ],
    retrieval_query="""
    RETURN
        node.content, node.prev_chunk, node.next_chunk
    """,
    embedding_node_property="content_embedding",
)

review_template = """Your job is to use product's description to answer questions about
with a product or service. Use the following context to answer questions, 
focusing on details that are on the context but don't make up any information that's not in the context. 
If you don't know an answer based on the context provided, say you don’t know.
{context}

Here is use question:
{question}
"""

review_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["context"], template=review_template)
)

review_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["question"], template="{question}")
)
messages = [review_system_prompt, review_human_prompt]

review_prompt = ChatPromptTemplate(
    input_variables=["context", "question"], messages=messages
)

content_vector_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model='gpt-4o-mini',temperature=0),
    chain_type="stuff",
    retriever=neo4j_vector_index.as_retriever(k=12),
    
)
print("✅✅ Get semantic search step")
content_vector_chain.combine_documents_chain.llm_chain.prompt = review_prompt
