import streamlit as st
from utils.data_summary import get_dataset_summary


def render_sidebar():

    with st.sidebar:

        st.markdown("# 🖥 Workspace")
        st.caption("Current project resources")
        st.divider()

        # =====================================
        # CSV
        # =====================================

        st.markdown("### 📊 CSV Dataset")

        if st.session_state.df is not None:

            summary = get_dataset_summary(
                st.session_state.df
            )

            st.success("Dataset Loaded")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Rows",
                    summary["rows"]
                )

            with col2:

                st.metric(
                    "Columns",
                    summary["columns"]
                )

        else:

            st.info("No CSV Uploaded")

        st.divider()

        # =====================================
        # PDF
        # =====================================

        st.markdown("### 📄 PDF Knowledge")

        if st.session_state.vectorstore is not None:

            st.success("Knowledge Base Indexed")

        else:

            st.info("No PDF Uploaded")

        st.divider()

        # =====================================
        # SQL
        # =====================================

        st.markdown("### 🗄 SQL Engine")

        if st.session_state.sql_connection is not None:

            st.success("Database Connected")

        else:

            st.info("Database Not Available")

        st.divider()

        # =====================================
        # Conversation
        # =====================================

        st.markdown("### 💬 Conversation")

        st.metric(
            "Messages",
            len(st.session_state.messages)
        )

        st.divider()

        # =====================================
        # Reset
        # =====================================

        st.markdown("### 🧹 Session")

        if st.button(
            "🔄 Reset Workspace",
            use_container_width=True
        ):

            st.session_state.messages = []
            st.session_state.last_question = None
            st.session_state.last_result = None
            st.session_state.vectorstore = None
            st.session_state.df = None
            st.session_state.sql_connection = None
            st.session_state.pdf_processed = False

            st.rerun()