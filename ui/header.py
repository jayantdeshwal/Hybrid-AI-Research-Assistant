import streamlit as st


def render_header():

    st.title("🤖 Hybrid AI Research Assistant")
    st.caption("Intelligent Multi-Agent System for CSV, SQL, PDF and Web Reasoning")

    st.markdown("### 🚀 Supported Knowledge Sources")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.info("📊\n\n**CSV**")

    with col2:
        st.info("🗄️\n\n**SQL**")

    with col3:
        st.info("📄\n\n**PDF**")

    with col4:
        st.info("🌐\n\n**Web**")

    with col5:
        st.info("🧠\n\n**Hybrid**")

    st.divider()