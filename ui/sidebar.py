import streamlit as st

from utils.data_summary import get_dataset_summary
from utils.llm import RESOLVED_MODEL


def _status(label, on):

    dot_class = "on" if on else "off"

    st.markdown(
        f"""
        <div class="hf-status">
          <span class="hf-status-dot {dot_class}"></span>
          <span>{label}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_sidebar():

    with st.sidebar:

        st.markdown("# 🖥 Workspace")
        st.caption("Current project resources")
        st.divider()

        # =====================================
        # Resource status (pulse dots)
        # =====================================

        st.markdown("### 📊 CSV Dataset")

        if st.session_state.df is not None:

            _status("Dataset loaded", on=True)

            summary = get_dataset_summary(
                st.session_state.df
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Rows", summary["rows"])

            with col2:
                st.metric("Columns", summary["columns"])

        else:
            _status("No CSV uploaded", on=False)

        st.divider()

        # =====================================
        # PDF
        # =====================================

        st.markdown("### 📄 PDF Knowledge")

        if st.session_state.vectorstore is not None:
            _status("Knowledge base indexed", on=True)
        else:
            _status("No PDF uploaded", on=False)

        st.divider()

        # =====================================
        # SQL
        # =====================================

        st.markdown("### 🗄 SQL Engine")

        if st.session_state.sql_connection is not None:
            _status("Database connected", on=True)
        else:
            _status("Database not available", on=False)

        st.divider()

        # =====================================
        # Model badge
        # =====================================

        st.markdown("### 🧠 Model")

        st.markdown(
            f"""
            <div class="hf-model-badge">
              ⚡ Groq · <b>{RESOLVED_MODEL}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "Auto-selected from your Groq account; "
            "override with the GROQ_MODEL env var."
        )

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
        # Reset (with confirmation)
        # =====================================

        st.markdown("### 🧹 Session")

        if st.button(
            "🔄 Reset Workspace",
            use_container_width=True
        ):

            st.session_state.confirm_reset = True

        if st.session_state.get("confirm_reset"):

            st.warning("Erase all uploads and chat history?")

            col_a, col_b = st.columns(2)

            with col_a:

                if st.button(
                    "✅ Confirm",
                    key="hf_reset_confirm",
                    use_container_width=True
                ):

                    for key in (
                        "messages",
                        "last_question",
                        "last_result",
                        "vectorstore",
                        "df",
                        "sql_connection",
                        "pdf_processed",
                        "processed_pdf_files",
                        "processed_csv_files",
                        "confirm_reset",
                    ):
                        st.session_state[key] = (
                            [] if key == "messages" else None
                        )

                    st.rerun()

            with col_b:

                if st.button(
                    "✖ Cancel",
                    key="hf_reset_cancel",
                    use_container_width=True
                ):

                    st.session_state.confirm_reset = False
                    st.rerun()
