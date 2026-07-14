import os

import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# ==========================================
# Configure Gemini API Key
# ==========================================

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GEMINI_API_KEY"]


# ==========================================
# Cached Embedding Model
# ==========================================

@st.cache_resource
def get_embedding_model():

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