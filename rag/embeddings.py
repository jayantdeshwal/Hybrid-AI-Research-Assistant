import os

from dotenv import load_dotenv

# ==========================================
# Configure Gemini API Key
# ==========================================
# Load from .env / environment first, then
# fall back to Streamlit secrets if present.

load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not gemini_key:
        try:
            import streamlit as st

            gemini_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            gemini_key = None

    if gemini_key:
        os.environ["GOOGLE_API_KEY"] = gemini_key


# ==========================================
# Cached Embedding Model
# ==========================================

def get_embedding_model():

    from langchain_google_genai import (
        GoogleGenerativeAIEmbeddings
    )

    if not os.environ.get("GOOGLE_API_KEY"):
        raise RuntimeError(
            "Gemini API key not found. Set GEMINI_API_KEY "
            "in your .env file (or .streamlit/secrets.toml)."
        )

    print("=" * 60)
    print("Loading Gemini Embedding Model...")
    print("=" * 60)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    print("=" * 60)
    print("Gemini Embedding Model Loaded Successfully")
    print("=" * 60)

    return embeddings