import uuid
import streamlit as st

from ui.styles import SOURCE_COLORS
from ui.motion import (
    animate_confidence_meter,
    apply_scroll_reveal,
)


_SOURCE_KEY_ALIASES = {
    "pdf": "document",
}


def _color_for(tool):

    key = _SOURCE_KEY_ALIASES.get(tool, tool)

    return SOURCE_COLORS.get(key, "#6D8CFF")


# ==========================================================
# Header
# ==========================================================

def render_response_header(response):

    route = response.get("route", [])
    source = response.get("source", "Unknown")
    confidence = response.get("confidence")
    reason = response.get("confidence_reason", "")

    # ----------------------------------------
    # Color-code the chat bubble border by
    # the first routed tool (CSS :has)
    # ----------------------------------------

    if route:

        c = _color_for(route[0])

        selector = (
            ".hf-badge[data-c='" + route[0] + "']"
        )

        css = (
            "<style>.stChatMessage:has(" + selector + ") {"
            "border-left: 3px solid " + c + "; }</style>"
        )

        st.markdown(css, unsafe_allow_html=True)

    st.markdown("#### 🤖 Assistant")

    if route:

        badges = " ".join(
            f'<span class="hf-badge" '
            f'data-c="{tool}" '
            f'style="--hf-badge-c:{_color_for(tool)}">'
            f'{tool.upper()}</span>'
            for tool in route
        )

        st.markdown(badges, unsafe_allow_html=True)

    st.caption(f"📚 Source: **{source}**")

    # ----------------------------------------
    # Animated confidence meter
    # ----------------------------------------

    if confidence is not None:

        if confidence >= 85:
            level = "High"
        elif confidence >= 60:
            level = "Medium"
        else:
            level = "Low"

        st.markdown(
            f"""
            <div class="hf-confidence-wrap">
              <span class="hf-confidence-label">
                CONFIDENCE · {level}
              </span>
              <div class="hf-confidence-track">
                <div class="hf-confidence-fill"
                     style="width:{int(confidence)}%">
                </div>
              </div>
              <span class="hf-confidence-value">
                {int(confidence)}%
              </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    if reason:

        if isinstance(reason, (list, tuple)):
            reason = " · ".join(
                str(r) for r in reason if r
            )

        st.markdown(
            f'<p class="hf-reasons">{reason}</p>',
            unsafe_allow_html=True
        )

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

    # ----------------------------------------
    # Animate the meter and reveal data
    # artifacts after render
    # ----------------------------------------

    animate_confidence_meter()

    if response.get("data") is not None:
        apply_scroll_reveal()


def render_chat_response(response):

    render_text_response(response)

    # ----------------------------------------
    # Hybrid answers may carry data artifacts
    # (table / chart / query) from routed tools
    # ----------------------------------------

    if response.get("data") is not None:

        render_data_artifacts(response)


def render_document_response(response):

    render_text_response(response)


def render_web_response(response):

    render_text_response(response)


# ==========================================================
# Data Response
# ==========================================================

def render_data_response(response):

    render_response_header(response)

    animate_confidence_meter()

    # ----------------------------------------
    # Failure / missing-data handling
    # (agent errors have data=None)
    # ----------------------------------------

    if not response.get("success", True) or response.get("data") is None:

        st.error(
            response.get("answer")
            or "Analysis failed — no results available."
        )

        if response.get("query"):

            with st.expander(
                "📝 Generated Query",
                expanded=False
            ):

                st.code(
                    response["query"],
                    language="python"
                )

        return

    render_data_artifacts(response)


# ==========================================================
# Shared Data Artifacts (table / query / chart / insight)
# ==========================================================

def render_data_artifacts(response):

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