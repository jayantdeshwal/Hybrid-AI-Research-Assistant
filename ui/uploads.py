import os
import pandas as pd
import streamlit as st

from rag.loader import load_pdf
from rag.splitter import split_documents
from rag.vectorstore import create_vectorstore

from sql.loader import create_database


def render_csv_upload(file):

    df = pd.read_csv(
        file,
        encoding="windows-1252"
    )

    st.session_state.sql_connection = (
        create_database(df)
    )

    if "Order Date" in df.columns:

        df["Order Date"] = pd.to_datetime(
            df["Order Date"],
            errors="coerce",
            format="mixed"
        )

    if "Ship Date" in df.columns:

        df["Ship Date"] = pd.to_datetime(
            df["Ship Date"],
            errors="coerce",
            format="mixed"
        )

    st.session_state.df = df

    st.success(
        f"✅ {file.name} uploaded successfully "
        f"({df.shape[0]} rows)"
    )


def render_pdf_upload(file):

    if st.session_state.pdf_processed:
        return

    with st.spinner(
        f"Processing {file.name}..."
    ):

        with open("temp.pdf", "wb") as f:

            f.write(file.getbuffer())

        documents = load_pdf("temp.pdf")

        chunks = split_documents(documents)

        st.session_state.vectorstore = (
            create_vectorstore(chunks)
        )

        st.session_state.pdf_processed = True

    st.success(

        f"✅ {file.name} uploaded successfully "

        f"({len(documents)} pages, "

        f"{len(chunks)} chunks)"

    )

    os.remove("temp.pdf")


def render_upload_section():

    st.markdown("## 📂 Upload Knowledge Sources")

    st.info(
    """
Upload your **CSV** and **PDF** files to enable Hybrid AI reasoning.

Supported formats:
- 📊 CSV Dataset
- 📄 PDF Documents
"""
)

    uploaded_files = st.file_uploader(
    "",
    type=["pdf", "csv"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

    if not uploaded_files:
        return

    for file in uploaded_files:

        if file.name.endswith(".pdf"):

            render_pdf_upload(file)

        elif file.name.endswith(".csv"):

            render_csv_upload(file)