import streamlit as st


def initialize_session():

    defaults = {

        "messages": [],
        "last_question": None,
        "last_result": None,

        "vectorstore": None,

        "sql_connection": None,

        "pdf_processed": False,

        "df": None

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value