from urllib import response
import uuid
import streamlit as st


# ==========================================================
# Header
# ==========================================================

def render_response_header(response):

    route = response.get("route", [])
    source = response.get("source", "Unknown")
    confidence = response.get("confidence")
    reason = response.get("confidence_reason", "")

    st.markdown("#### 🤖 Assistant")

    left, right = st.columns([5, 1])

    with left:

        if route:

            badges = " ".join(
                f":blue-badge[{tool.upper()}]"
                for tool in route
            )

            st.markdown(badges)

        st.caption(f"📚 Source: **{source}**")

    with right:

        if confidence is not None:

            st.metric(
                "Confidence",
                f"{confidence}%"
            )

    if reason:

        st.caption(f"**Reason:** {reason}")

    st.divider()


# ==========================================================
# Text Answer
# ==========================================================

def render_answer(answer):

    with st.container(border=True):

        st.markdown(answer)


# ==========================================================
# Generic Text Response
# ==========================================================

def render_text_response(response):

    render_response_header(response)

    render_answer(response["answer"])


def render_chat_response(response):

    render_text_response(response)


def render_document_response(response):

    render_text_response(response)


def render_web_response(response):

    render_text_response(response)


# ==========================================================
# Data Response
# ==========================================================

def render_data_response(response):

    render_response_header(response)

    if response.get("query"):

        with st.expander(
            "📝 Generated Query",
            expanded=False
        ):

            st.code(
                response["query"],
                language="python"
            )

    st.markdown("### 📊 Analysis Result")

    rows = len(response["data"])

    table_height = min(250, 40 + rows * 35)

    st.dataframe(
        response["data"],
        use_container_width=True,
        height=table_height
    )

    if hasattr(response["data"], "to_csv"):

        csv = response["data"].to_csv(index=False)

        download_key = response.get(
            "download_key",
            str(uuid.uuid4())
        )

        _, col = st.columns([4, 1])

        with col:

            st.download_button(
                "⬇ Download",
                csv,
                file_name="analysis_result.csv",
                mime="text/csv",
                width="stretch",
                key=download_key
            )

    if response.get("chart") is not None:

        st.markdown("### 📈 Visualization")

        fig = response["chart"]

        fig.set_size_inches(9, 4.8)

        fig.tight_layout()

        st.pyplot(
            fig,
            use_container_width=True
        )

    if response.get("explanation"):

        st.info(
            f"💡 **Business Insight**\n\n"
            f"{response['explanation']}"
        )