"""
Entry point for the Insurance RAG Streamlit application.
"""

import logging
from interface.streamlit_app import InsuranceRAGApp

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    logging.info("Initializing Insurance RAG Application")
    app = InsuranceRAGApp()
    app.run()
