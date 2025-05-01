import streamlit as st
from rag.rag_pipeline import RAGEngine
from config import INDEX_DIR, JSON_RAG_TEXT_KEY

class InsuranceRAGApp:
    def __init__(self):
        self.rag = RAGEngine()


    def run(self):
        st.set_page_config(page_title="Insurance RAG Assistant", layout="wide")
        st.title("Страховой RAG-Аналитик")

        query = st.text_input("Введите вопрос по отчёту:")
        if query:
            with st.spinner("🔍 Анализируем..."):
                answer, docs = self.rag.answer_query(query)

            st.markdown("### Ответ:")
            st.write(answer)

            st.markdown("---")
            st.markdown("### 🔎 Использованный контекст:")
            for i, doc in enumerate(docs, 1):
                st.markdown(f"**Фрагмент {i}:**")
                st.code(doc[JSON_RAG_TEXT_KEY], language="markdown")
