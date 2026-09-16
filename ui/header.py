import streamlit as st

from ui.styles import SOURCE_COLORS, get_theme, toggle_theme


_SOURCES = [
    ("csv", "📊", "CSV"),
    ("sql", "🗄️", "SQL"),
    ("document", "📄", "PDF"),
    ("web", "🌐", "Web"),
    ("hybrid", "🧠", "Hybrid"),
]


def render_header():

    # ------------------------------------
    # Theme toggle (top right)
    # ------------------------------------

    col_title, col_toggle = st.columns([12, 1])

    with col_toggle:

        st.markdown(
            '<div class="hf-theme-toggle">',
            unsafe_allow_html=True
        )

        icon = "☀️" if get_theme() == "dark" else "🌙"

        if st.button(
            icon,
            key="hf_theme_toggle",
            use_container_width=True,
            help="Switch theme"
        ):
            toggle_theme()
            st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # ------------------------------------
    # Hero title
    # ------------------------------------

    st.markdown(
        """
        <div class="hf-hero">
            <h1 class="hf-title">
                🤖 Hybrid AI Research Assistant
            </h1>
            <p class="hf-subtitle">
                Intelligent multi-agent system for CSV, SQL,
                PDF and Web reasoning
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------
    # Capability chips (color-coded)
    # ------------------------------------

    chips = "".join(
        f'<span class="hf-chip" '
        f'style="--hf-chip-c:{SOURCE_COLORS[key]}">'
        f'<span class="hf-chip-dot"></span>'
        f'{emoji} {label}</span>'
        for key, emoji, label in _SOURCES
    )

    st.markdown(
        f'<div class="hf-chip-row">{chips}</div>',
        unsafe_allow_html=True
    )

    st.divider()
