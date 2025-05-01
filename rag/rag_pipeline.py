from openai import OpenAI
import os
from pathlib import Path
from config import OPENAI_MODEL, TOP_K, JSON_RAG_TEXT_KEY, EMBED_MODEL_NAME, INDEX_DIR
from data_processing.index_builder import IndexBuilder

class RAGEngine:
    """
    A class for generating answers to questions using the Retrieval-Augmented Generation (RAG) approach.

    First finds relevant documents via FAISS, then generates a prompt and sends it to OpenAI GPT.

    Attributes:
    index_store (IndexStore): An object providing access to the FAISS index and related documents.
    embedder (Embedder): An embedding module used to vectorize the query.
    client (OpenAI): An OpenAI client for invoking the GPT model.

    Methods:
    answer_query(query: str) -> tuple[str, list[dict]]:
    Returns the generated GPT answer and the documents used.
    """

    def __init__(self, embed_model_name: str = EMBED_MODEL_NAME):
        self.index_builder = IndexBuilder(embed_model_name)
        self.index_builder.load_index(Path(INDEX_DIR))
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def answer_query(self, query: str) -> tuple[str, list[dict]]:
        query_vec = self.index_builder.embed_texts([query])
        top_docs = self.index_builder.search(query_vec, TOP_K)
        prompt = self._generate_prompt(query, top_docs)

        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "Ты ассистент, который анализирует страховые отчёты."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            return response.choices[0].message.content.strip(), top_docs
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {e}")

    def _generate_prompt(self, query: str, context_docs: list[dict]) -> str:
        """
        Generates a prompt based on the context and user query.

        Args:
        query (str): The original user query.
        context_docs (list[dict]): The list of documents retrieved from the index.

        Returns:
        str: The prompt to pass to the GPT model.
        """

        context = "\n".join([f"[{i+1}] {doc[JSON_RAG_TEXT_KEY]}" for i, doc in enumerate(context_docs)])
        return (
            f"Контекст из страхового отчета:\n{context}\n\n"
            f"На основе этих данных, ответь на вопрос пользователя.\n"
            f"Вопрос: {query}\n"
        )
