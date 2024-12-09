import asyncio
import os
import pandas as pd
import ast
import logging

from langchain_community.document_loaders import DirectoryLoader
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from llm.get_llm import get_model_function
from agents.rag_agent import get_agent
from ragas.testset.transforms.extractors.llm_based import NERExtractor
from ragas.testset.transforms.splitters import HeadlineSplitter
from ragas.testset import TestsetGenerator, persona
from ragas.testset.synthesizers.single_hop.specific import SingleHopSpecificQuerySynthesizer
from ragas.testset import TestsetGenerator
from ragas.testset.persona import Persona
from ragas.dataset_schema import EvaluationDataset

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Step 1: Define Transforms
        transforms = [HeadlineSplitter(), NERExtractor()]
        logger.debug("Transforms defined: HeadlineSplitter and NERExtractor.")

        # Step 2: Initialize LLM and Embeddings
        generator_llm = LangchainLLMWrapper(get_model_function())
        generator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())
        logger.debug("LLM and Embeddings wrappers initialized.")

        # Step 3: Load Documents
        path = "/Users/admin/Working/thaibinh-chatbot/input"
        loader = DirectoryLoader(path, glob="**/[!.]*")
        docs = loader.load()
        logger.debug(f"Documents loaded from {path}. Total documents: {len(docs)}")

        # Step 4: Define Personas
        personas = [
                        Persona(
                            name="curious student",
                            role_description="A student who is curious about the world and wants to learn more about different cultures and languages",
                        ),
                    ]
        logger.debug("Personas defined: 'curious student'.")

        # Step 5: Initialize TestsetGenerator
        generator = TestsetGenerator(
            llm=generator_llm, embedding_model=generator_embeddings, persona_list=personas
        )
        logger.debug("TestsetGenerator initialized.")

        # Step 6: Define Synthesizer Distribution
        distribution = [
            (SingleHopSpecificQuerySynthesizer(llm=generator_llm), 1.0),
        ]
        logger.debug("Synthesizer distribution defined.")

        # Step 7: Adapt Prompts for Each Synthesizer
        for synthesizer, weight in distribution:
            # Ensure that 'adapt_prompts' is an async method
            prompts = await synthesizer.adapt_prompts("vietnamese", llm=generator_llm)
            synthesizer.set_prompts(**prompts)
            logger.debug(f"Prompts adapted and set for synthesizer: {synthesizer.__class__.__name__}")

        # Step 8: Generate Testset with Documents and Synthesizers
        dataset = generator.generate_with_langchain_docs(
            docs=docs[:],
            testset_size=20,  # Adjust testset_size as needed
            transforms=transforms,
            query_distribution=distribution,
        )

        eval_dataset = dataset.to_evaluation_dataset()

        logger.debug(f"Testset generated with size: {len(dataset)}")

        # Step 9: Convert Dataset to Pandas DataFrame

        df = eval_dataset.to_pandas()
        logger.debug("Dataset converted to Pandas DataFrame.")

        # Step 10: Save DataFrame to CSV
        output_csv = "save_test4.csv"
        df.to_csv(output_csv, index=False)
        logger.debug(f"DataFrame saved to CSV file: {output_csv}")

    except ValueError as ve:
        logger.error(f"ValueError encountered: {ve}")
    except SyntaxError as se:
        logger.error(f"SyntaxError encountered: {se}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())