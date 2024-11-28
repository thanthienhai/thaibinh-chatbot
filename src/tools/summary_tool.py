from src.llm.get_llm import get_model_function
from src.llm.get_graph import get_graph_function
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate

qa_generation_template = """You are an assistant that takes the results from
a Neo4j Cypher query and forms a human-readable response. The query results
section contains the results of a Cypher query that was generated based on a
user's natural language question. The provided information is authoritative;
you must always use it to construct your response without any external knowledge
or assumptions. Make the answer sound like a response to the user's question.
Do not return all the properties of the label. Only return few important properties of the label.

Instructions:
1. Schema Adherence: Use only the provided relationship types and properties in the schema. Avoid using any other relationship types or properties that are not specified.
2. Query Limitations: Always limit your answers to a maximum of 10 nodes to maintain concise results.
3. Node Output: Do not return entire nodes or embedding properties. Focus on specific attributes relevant to the user’s question. Remember include link properties when you provide products.
4. Example Usage: Use the examples provided to guide your translations. Structure your queries similarly for consistency and clarity.

Here is example question:

Question: Cho tôi đánh giá của người dùng về sản phẩm: chuột có dây logitech b100 - hàng chính hãng?

Cypher: 

MATCH (p:Product {name: 'Chuột Có Dây Logitech B100 - Hàng Chính Hãng'})
OPTIONAL MATCH (p)<-[:REVIEWED]-(r:Review)
WITH p, r
ORDER BY r.date DESC // Optional: Order reviews, e.g., by date
WITH p, collect({content: r.content, rating: r.rating})[0..10] AS topReviews
RETURN p.specifications p.link AS specifications, topReviews

The user asked the following question:
{question}

A Cypher query was run and generated these results:
{context}

If the provided information is empty, say you don’t know the answer.
Empty information looks like this: []

If the query results are not empty, you must provide an answer.
If the question involves a time duration, assume that any duration in the
query results is measured in days unless otherwise specified.

When names are provided in the query results, such as customer names or
product names, beware of any names that contain punctuation. For instance,
'Acme, Inc.' is a single company name, not multiple companies. Make sure to
format any list of names clearly to avoid ambiguity and to convey full names
accurately.

Never say you lack the right information if data is present in the query results.
Make sure to show all relevant query results if the user asks for details. You
must always assume that any provided query results are relevant to answer the
user's question. Construct your response solely based on the provided query results.

IMPORTANT YOUR ouput must be in Vietnamese
Helpful Answer:
"""

CYPHER_GENERATION_TEMPLATE = """
You are an expert Neo4j Developer specialized in translating user questions into Cypher queries. Your task is to answer questions about products and provide recommendations based on the specified schema.

Instructions:
1. Schema Adherence: Use only the provided relationship types and properties in the schema. Avoid using any other relationship types or properties that are not specified.
2. Query Limitations: Always limit your answers to a maximum of 10 nodes to maintain concise results.
3. Node Output: Do not return entire nodes or embedding properties. Focus on specific attributes relevant to the user’s question.
4. Example Usage: Use the examples provided to guide your translations. Structure your queries similarly for consistency and clarity.

Schema:
{schema}

Question:
{question}

Cypher Query:
"""
model = get_model_function()
graph = get_graph_function()
cypher_prompt = PromptTemplate.from_template(qa_generation_template)
cypher_summary = GraphCypherQAChain.from_llm(
    model,
    graph=graph,
    verbose=True,
    cypher_prompt = cypher_prompt,
    return_intermediate_steps=True,
    exclude_types=["embedding","description_embedding"],
    validate_cypher=True

)
