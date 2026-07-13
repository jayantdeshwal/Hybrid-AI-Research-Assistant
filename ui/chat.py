import streamlit as st

from agents.main_agent import main_agent

from ui.response_renderer import (
    render_chat_response,
    render_document_response,
    render_web_response,
    render_data_response,
)
import uuid


# =====================================================
# Render Complete Conversation
# =====================================================

def render_chat_history():

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            if message["role"] == "user":

                st.markdown(message["content"])
                continue

            tool = message.get("tool")

            if tool == "chat":

                render_chat_response(message)

            elif tool == "document":

                render_document_response(message)

            elif tool == "web":

                render_web_response(message)

            elif tool in ["csv", "sql"]:

                render_data_response(message)


# =====================================================
# Execute Agent
# =====================================================

def process_user_question(question, df):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # Show it immediately
    with st.chat_message("user"):
        st.markdown(question)

    response = main_agent(
        question=question,
        df=df,
        vectorstore=st.session_state.vectorstore,
        last_question=st.session_state.last_question,
        last_result=st.session_state.last_result,
        sql_connection=st.session_state.sql_connection,
    )

    return response


# =====================================================
# Save Assistant Response
# =====================================================

def save_agent_response(response, question):

    tool = response["tool"]

    if tool in ["csv", "sql"]:

        st.session_state.last_question = question
        st.session_state.last_result = response.get("data")

    message = {
    "role": "assistant",

    "tool": response.get("tool"),

    "success": response.get("success", True),

    "answer": response.get("answer"),

    "query": response.get("query"),

    "data": response.get("data"),

    "chart": response.get("chart"),

    "explanation": response.get("explanation"),

    "route": response.get("route", []),

    "source": response.get("source"),

    "sources": response.get("sources", []),

    "confidence": response.get("confidence"),

    "confidence_reason": response.get("confidence_reason"),

    "metadata": response.get("metadata", {}),
}

    st.session_state.messages.append(message)