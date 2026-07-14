import streamlit as st
from ui.styles import load_css
from ui.header import render_header
from ui.sidebar import render_sidebar

from ui.session import initialize_session
from ui.uploads import render_upload_section

from ui.chat import (
    render_chat_history,
    process_user_question,
    save_agent_response
)



# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title="AI Data Analyst Agent",
    page_icon="📊",
    layout="wide"
)
load_css()

render_header()


# ==========================================
# Session State
# ==========================================

initialize_session()


# ==========================================
# File Upload Section
# ==========================================

render_upload_section()


# ==========================================
# Get dataframe from session
# ==========================================

df = st.session_state.df


# ==========================================
# Sidebar
# ==========================================

render_sidebar()


# ==========================================
# Render Chat History
# ==========================================

render_chat_history()

# ==========================================
# Chat Input
# ==========================================

question = st.chat_input(
    "Ask anything..."
)


# ==========================================
# User Question
# ==========================================

if question:

    response = None

    with st.chat_message("assistant"):

        with st.spinner("Analyzing..."):

            response = process_user_question(question, df)

    save_agent_response(response, question)

    st.rerun()