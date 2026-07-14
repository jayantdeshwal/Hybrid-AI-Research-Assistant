import time
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings

@st.cache_resource
def get_embedding_model():

    print("Embedding loading started")

    start = time.time()

    model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print(f"Embedding loaded in {time.time()-start:.2f} seconds")

    return model