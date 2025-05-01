import logging
from pathlib import Path
import json

from data_processing.excel_parser import ExcelParser
from data_processing.index_builder import IndexBuilder
from config import DATA_FILE, DOCUMENTS_PATH, INDEX_DIR, EMBED_MODEL_NAME, JSON_RAG_TEXT_KEY

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def documents_exist(documents_path: Path) -> bool:
    return documents_path.exists()


def index_exists(index_path: Path) -> bool:
    return index_path.exists()


def load_documents(documents_path: Path) -> list[dict]:
    with open(documents_path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if JSON_RAG_TEXT_KEY in json.loads(line)]


def extract_documents_from_excel(data_file: str, output_path: Path) -> list[dict]:
    logger.info("Extracting documents from Excel...")
    parser = ExcelParser(data_file)
    docs = parser.parse()
    parser.save_as_jsonl(docs, output_path=output_path)
    return docs


def build_and_save_index(docs: list[dict], dir: Path):
    if not docs:
        logger.error(f"No documents contain the key '{JSON_RAG_TEXT_KEY}'.")
        raise ValueError("No valid documents to index.")

    index_builder = IndexBuilder(EMBED_MODEL_NAME)
    index, embeddings, texts_for_rag = index_builder.build_index(docs)
    index_builder.save_index(index, texts_for_rag, docs, dir)
    logger.info("The index has been built and saved successfully.")


def main():
    documents_path = Path(DOCUMENTS_PATH)
    index_path = Path(INDEX_DIR) / "faiss.index"

    if index_exists(index_path):
        logger.info("The index already exists. Skipping index build.")
        return

    if documents_exist(documents_path):
        logger.info("Loading existing documents...")
        docs = load_documents(documents_path)
    else:
        docs = extract_documents_from_excel(DATA_FILE, documents_path)

    build_and_save_index(docs, Path(INDEX_DIR))


if __name__ == "__main__":
    main()
