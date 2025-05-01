"""
Configuration for Insurance RAG project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "test.xlsx"
DOCUMENTS_PATH = BASE_DIR / "data" / "documents.jsonl"
INDEX_DIR = BASE_DIR / "data" / "index"

JSON_RAG_TEXT_KEY = 'text'

OPENAI_MODEL = "gpt-3.5-turbo"
EMBED_MODEL_NAME = "intfloat/multilingual-e5-base"
TOP_K = 5
