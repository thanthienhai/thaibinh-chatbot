from langchain_community.document_loaders import DirectoryLoader
import os
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from llm.get_llm import get_model_function


generator_llm = LangchainLLMWrapper(get_model_function())
generator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())



os.environ["OPENAI_API_KEY"] = "your-openai-key"
path = "/Users/admin/Working/thaibinh-chatbot/input"
loader = DirectoryLoader(path, glob="**/[!.]*")
docs = loader.load()