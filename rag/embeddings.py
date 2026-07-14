import os
import time

import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings


# ==========================================
# Configure Hugging Face Authentication
# ==========================================

if "HF_TOKEN" in st.secrets:
    os.environ["HF_TOKEN"] = st.secrets["HF_TOKEN"]
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.secrets["HF_TOKEN"]


# ==========================================
# Cached Embedding Model
# ==========================================

@st.cache_resource
def get_embedding_model():

    print("=" * 60)
    print("Loading HuggingFace Embedding Model...")
    start = time.time()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    end = time.time()

    print(f"Embedding model loaded successfully in {end - start:.2f} seconds")
    print("=" * 60)

    return embeddings