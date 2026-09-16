import os
import pandas as pd
import streamlit as st

from rag.loader import load_pdf
from rag.splitter import split_documents
from rag.vectorstore import create_vectorstore

from sql.loader import create_database
from ui.motion import animate_upload_zone


def render_csv_upload(file):

    # ----------------------------------------
    # Skip re-processing on Streamlit reruns
    # ----------------------------------------

    processed = st.session_state.get(
        "processed_csv_files",
        set()
    )

    if file.name in processed:
        return

    df = load_csv_with_fallback(file)

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

    processed.add(file.name)
    st.session_state.processed_csv_files = processed

    st.success(
        f"✅ {file.name} uploaded successfully "
        f"({df.shape[0]} rows)"
    )


def load_csv_with_fallback(file):

    for encoding in (
        "utf-8",
        "windows-1252",
        "latin-1"
    ):

        try:

            return pd.read_csv(
                file,
                encoding=encoding
            )

        except UnicodeDecodeError:
            file.seek(0)
            continue

    raise ValueError(
        f"Could not decode {file.name} with any "
        "supported encoding."
    )


def render_pdf_upload(file):

    # ----------------------------------------
    # Track processed PDFs by name so every
    # uploaded PDF is indexed exactly once
    # ----------------------------------------

    processed = st.session_state.get(
        "processed_pdf_files",
        set()
    )

    if file.name in processed:
        return

    with st.spinner(
        f"Processing {file.name}..."
    ):

        try:

            with open("temp.pdf", "wb") as f:

                f.write(file.getbuffer())

            documents = load_pdf("temp.pdf")

            chunks = split_documents(documents)

            existing = st.session_state.get(
                "vectorstore"
            )

            if existing is not None:

                # Merge new PDF into the
                # existing knowledge base

                existing.add_documents(chunks)

                st.session_state.vectorstore = (
                    existing
                )

            else:

                st.session_state.vectorstore = (
                    create_vectorstore(chunks)
                )

            processed.add(file.name)
            st.session_state.processed_pdf_files = (
                processed
            )

        finally:

            if os.path.exists("temp.pdf"):
                os.remove("temp.pdf")

    st.success(

        f"✅ {file.name} uploaded successfully "
        f"({len(documents)} pages, "
        f"{len(chunks)} chunks)"
    )


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

    animate_upload_zone()

    if not uploaded_files:
        return

    for file in uploaded_files:

        if file.name.lower().endswith(".pdf"):

            render_pdf_upload(file)

        elif file.name.lower().endswith(".csv"):

            render_csv_upload(file)