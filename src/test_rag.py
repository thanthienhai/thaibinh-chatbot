from ragas import EvaluationDataset
import pandas as pd

from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness, SemanticSimilarity
from ragas import evaluate

from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from llm.get_llm import get_eval_model_function, get_embedding_function
from agents.rag_agent import chat_agent
import ast



df = pd.read_csv("save_test2.csv")

# c
def convert_to_list(s):
    try:
        # Remove surrounding quotes if present
        if isinstance(s, str):
            s = s.strip()
            if s.startswith('"') and s.endswith('"'):
                s = s[1:-1]
            elif s.startswith("'") and s.endswith("'"):
                s = s[1:-1]
        return ast.literal_eval(s) if isinstance(s, str) else s
    except (ValueError, SyntaxError) as e:
        print(f"Error parsing string to list: {s}\n{e}")
        return []  # Return an empty list or handle as needed
    
df['retrieved_contexts'] = df['retrieved_contexts'].apply(convert_to_list)

testset= EvaluationDataset.from_pandas(df)

print(testset.features())

print(testset.get_sample_type())
evaluator_llm = LangchainLLMWrapper(chat_agent)
evaluator_embeddings = LangchainEmbeddingsWrapper(get_embedding_function())

metrics = [
    LLMContextRecall(llm=evaluator_llm), 
    FactualCorrectness(llm=evaluator_llm), 
    Faithfulness(llm=evaluator_llm),
    SemanticSimilarity(embeddings=evaluator_embeddings)
]
results = evaluate(dataset=testset, metrics=metrics)

df = results.to_pandas()
df.to_csv