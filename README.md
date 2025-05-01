
---

# RAG System for Excel Document Analysis

---

## Project Structure

```
├── app.py                      # Main application entry point
├── config.py                   # Project configuration
├── data/                       # Raw and indexed data
│   ├── test.xlsx
│   ├── documents.jsonl
│   └── index/
├── data_processing/            # Parsing, embedding, and data preparation
│   ├── excel_parser.py
│   ├── embedder.py
│   └── __init__.py
├── rag/                        # RAG pipeline and index management
│   ├── rag_pipeline.py
│   ├── index_store.py
│   └── __init__.py
├── interface/                  # Streamlit interface
│   ├── streamlit_app.py
│   └── __init__.py
├── scripts/                    # Initialization scripts
│   └── init_index.py
├── test/                       # Unit tests
│   ├── test_excel_parser.py
│   ├── test_embedder.py
│   ├── test_rag_retrieval.py
│   └── ...
└── requirements.txt            # Project dependencies
```

---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

---

## Running the App

```bash
streamlit run app.py
```

After launch, open in your browser:
- http://localhost:8501

---

## Environment Variables

You must set the `OPENAI_API_KEY` environment variable:

```bash
export OPENAI_API_KEY=your_key_here
```

---

## Testing

To run all unit tests:

```bash
pytest test/
```

---

## Dependencies

This project uses:
- FAISS for fast retrieval
- Sentence Transformers for embeddings
- Streamlit for UI
- Pandas and OpenPyXL for working with Excel

---

## Index Initialization

Before the first run, you need to create embeddings and a FAISS index from the Excel file. Run:

```bash
python scripts/init_index.py
```

---

## Debugging Startup Issues

If you encounter an error like:

```
ModuleNotFoundError: No module named 'data_processing'
```

### Make sure that:

You are running the script from the project root **and have set the PYTHONPATH**:

```bash
export PYTHONPATH=.
python scripts/init_index.py --input_path data/test.xlsx --output_dir data/
```

---