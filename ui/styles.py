"""
Design system for the Hybrid AI Research Assistant.

Pro Max UI kit: dark "midnight" theme (default) + light theme,
CSS-variable driven, with glassmorphism cards, gradient accents,
source-color-coded chat borders, confidence meter, status dots
and full responsiveness.
"""

import streamlit as st


# ==========================================
# Theme state
# ==========================================

def get_theme():

    return st.session_state.get("theme", "dark")


def toggle_theme():

    st.session_state.theme = (
        "light" if get_theme() == "dark" else "dark"
    )


# ==========================================
# Palettes
# ==========================================

_PALETTES = {
    "dark": {
        "bg": "#0B1220",
        "bg-glow-1": "rgba(109,140,255,0.16)",
        "bg-glow-2": "rgba(34,211,238,0.10)",
        "surface": "rgba(17,26,46,0.82)",
        "surface-solid": "#111A2E",
        "surface-2": "#16213A",
        "border": "rgba(255,255,255,0.09)",
        "border-strong": "rgba(255,255,255,0.16)",
        "text": "#E7ECF5",
        "muted": "#93A1B8",
        "accent": "#6D8CFF",
        "accent-2": "#22D3EE",
        "accent-soft": "rgba(109,140,255,0.14)",
        "shadow": "0 10px 34px rgba(0,0,0,0.42)",
        "shadow-hover": "0 16px 44px rgba(0,0,0,0.55)",
        "scroll-track": "#101A30",
        "scroll-thumb": "#2A3A5C",
        "input-bg": "rgba(13,21,38,0.9)",
    },
    "light": {
        "bg": "#F6F8FC",
        "bg-glow-1": "rgba(37,99,235,0.08)",
        "bg-glow-2": "rgba(8,145,178,0.06)",
        "surface": "rgba(255,255,255,0.88)",
        "surface-solid": "#FFFFFF",
        "surface-2": "#EEF3FA",
        "border": "#E4E9F2",
        "border-strong": "#CBD5E4",
        "text": "#0F172A",
        "muted": "#5B6B83",
        "accent": "#2563EB",
        "accent-2": "#0891B2",
        "accent-soft": "rgba(37,99,235,0.08)",
        "shadow": "0 8px 28px rgba(15,23,42,0.08)",
        "shadow-hover": "0 14px 38px rgba(15,23,42,0.14)",
        "scroll-track": "#EEF2F9",
        "scroll-thumb": "#C3CDE0",
        "input-bg": "#FFFFFF",
    },
}

# Per-source identity colors (chat borders, badges, dots)

SOURCE_COLORS = {
    "csv": "#60A5FA",
    "sql": "#FBBF24",
    "document": "#A78BFA",
    "web": "#34D399",
    "chat": "#94A3B8",
    "hybrid": "#F472B6",
}


def _css(p):
    """Build the full stylesheet from a palette."""

    src_vars = " ".join(
        f'--hf-{name}: {color};'
        for name, color in SOURCE_COLORS.items()
    )

    return f"""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {{
        --hf-bg: {p["bg"]};
        --hf-bg-glow-1: {p["bg-glow-1"]};
        --hf-bg-glow-2: {p["bg-glow-2"]};
        --hf-surface: {p["surface"]};
        --hf-surface-solid: {p["surface-solid"]};
        --hf-surface-2: {p["surface-2"]};
        --hf-border: {p["border"]};
        --hf-border-strong: {p["border-strong"]};
        --hf-text: {p["text"]};
        --hf-muted: {p["muted"]};
        --hf-accent: {p["accent"]};
        --hf-accent-2: {p["accent-2"]};
        --hf-accent-soft: {p["accent-soft"]};
        --hf-shadow: {p["shadow"]};
        --hf-shadow-hover: {p["shadow-hover"]};
        --hf-input-bg: {p["input-bg"]};
        --hf-gradient: linear-gradient(120deg, {p["accent"]}, {p["accent-2"]}, #A78BFA);
        {src_vars}
    }}

    /* ===========================
       Base
    =========================== */

    html, body, [class*="css"], .stApp,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li {{
        font-family: 'Inter', sans-serif;
        font-feature-settings: "tnum" 1;
    }}

    /* Global text color - covers old and new
       Streamlit class systems (1.64+) */

    .stApp,
    .stApp *:not(svg):not(path):not(a) {{
        color: var(--hf-text);
    }}

    code, pre, code * {{
        color: var(--hf-accent-2);
    }}

    .stApp {{
        background:
            radial-gradient(1100px 480px at 15% -8%, var(--hf-bg-glow-1), transparent 60%),
            radial-gradient(900px 420px at 90% -12%, var(--hf-bg-glow-2), transparent 55%),
            var(--hf-bg);
    }}

    .main .block-container {{
        max-width: 1200px;
        padding-top: 1.6rem;
        padding-bottom: 3rem;
    }}

    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header {{ visibility: hidden; }}

    ::selection {{
        background: var(--hf-accent);
        color: #fff;
    }}

    /* ===========================
       Hero / Header
    =========================== */

    .hf-hero {{
        padding: .4rem 0 .2rem 0;
    }}

    .hf-title {{
        font-size: 2.35rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        line-height: 1.15;
        background: var(--hf-gradient);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }}

    .hf-subtitle {{
        color: var(--hf-muted);
        font-size: 1.02rem;
        margin-top: .45rem;
    }}

    .hf-chip-row {{
        display: flex;
        flex-wrap: wrap;
        gap: .6rem;
        margin: 1.05rem 0 .4rem 0;
    }}

    .hf-chip {{
        display: inline-flex;
        align-items: center;
        gap: .45rem;
        padding: .42rem .95rem;
        border-radius: 999px;
        font-size: .86rem;
        font-weight: 600;
        color: var(--hf-text);
        background: var(--hf-surface);
        border: 1px solid var(--hf-border-strong);
        box-shadow: var(--hf-shadow);
        backdrop-filter: blur(10px);
        transition: transform .25s ease, box-shadow .25s ease,
                    border-color .25s ease;
    }}

    .hf-chip:hover {{
        transform: translateY(-3px);
        border-color: var(--hf-chip-c, var(--hf-accent));
        box-shadow: 0 8px 26px color-mix(
            in srgb, var(--hf-chip-c, var(--hf-accent)) 32%, transparent
        );
    }}

    .hf-chip .hf-chip-dot {{
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: var(--hf-chip-c, var(--hf-accent));
        box-shadow: 0 0 10px var(--hf-chip-c, var(--hf-accent));
    }}

    /* ===========================
       Sidebar (glass)
    =========================== */

    section[data-testid="stSidebar"] {{
        background: var(--hf-surface);
        backdrop-filter: blur(18px);
        border-right: 1px solid var(--hf-border);
        box-shadow: 6px 0 34px rgba(0,0,0,0.18);
    }}

    section[data-testid="stSidebar"] .block-container {{
        padding-top: 1.4rem;
    }}

    /* Status dots */

    .hf-status {{
        display: flex;
        align-items: center;
        gap: .55rem;
        padding: .5rem .75rem;
        border-radius: 12px;
        border: 1px solid var(--hf-border);
        background: var(--hf-surface-2);
        margin-bottom: .45rem;
        font-size: .88rem;
        font-weight: 500;
    }}

    .hf-status-dot {{
        width: 9px;
        height: 9px;
        border-radius: 50%;
        flex-shrink: 0;
    }}

    .hf-status-dot.on {{
        background: #34D399;
        animation: hfPulse 2.2s ease-out infinite;
    }}

    .hf-status-dot.off {{
        background: var(--hf-muted);
        opacity: .55;
    }}

    @keyframes hfPulse {{
        0%   {{ box-shadow: 0 0 0 0 rgba(52,211,153,0.55); }}
        70%  {{ box-shadow: 0 0 0 9px rgba(52,211,153,0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(52,211,153,0); }}
    }}

    .hf-model-badge {{
        font-size: .78rem;
        color: var(--hf-muted);
        border: 1px dashed var(--hf-border-strong);
        border-radius: 10px;
        padding: .45rem .7rem;
        margin-top: .35rem;
        word-break: break-all;
    }}

    /* ===========================
       Metrics
    =========================== */

    div[data-testid="stMetric"],
    div[data-testid="metric-container"] {{
        background: var(--hf-surface);
        border: 1px solid var(--hf-border);
        border-radius: 16px;
        padding: 14px 16px;
        box-shadow: var(--hf-shadow);
        backdrop-filter: blur(10px);
        transition: transform .25s ease, box-shadow .25s ease;
    }}

    div[data-testid="stMetric"]:hover,
    div[data-testid="metric-container"]:hover {{
        transform: translateY(-3px);
        box-shadow: var(--hf-shadow-hover);
    }}

    /* ===========================
       Chat messages
    =========================== */

    .stChatMessage {{
        border-radius: 18px;
        padding: 16px 18px;
        margin-bottom: 16px;
        border: 1px solid var(--hf-border);
        background: var(--hf-surface);
        backdrop-filter: blur(12px);
        transition: transform .25s ease, box-shadow .25s ease,
                    border-color .25s ease;
        box-shadow: var(--hf-shadow);
    }}

    .stChatMessage:hover {{
        transform: translateY(-2px);
        box-shadow: var(--hf-shadow-hover);
    }}

    /* Source-color-coded left border, set per message */

    .hf-msg {{
        border-left: 3px solid var(--hf-msg-c, var(--hf-accent));
    }}

    /* ===========================
       Agent badges
    =========================== */

    .hf-badge {{
        display: inline-block;
        padding: .22rem .7rem;
        margin-right: .4rem;
        border-radius: 999px;
        font-size: .72rem;
        font-weight: 700;
        letter-spacing: .06em;
        text-transform: uppercase;
        color: var(--hf-text);
        background: color-mix(
            in srgb, var(--hf-badge-c, var(--hf-accent)) 18%, transparent
        );
        border: 1px solid color-mix(
            in srgb, var(--hf-badge-c, var(--hf-accent)) 45%, transparent
        );
    }}

    /* ===========================
       Confidence meter
    =========================== */

    .hf-confidence-wrap {{
        display: flex;
        align-items: center;
        gap: .7rem;
        margin: .3rem 0 .15rem 0;
    }}

    .hf-confidence-label {{
        font-size: .78rem;
        font-weight: 600;
        color: var(--hf-muted);
        white-space: nowrap;
    }}

    .hf-confidence-track {{
        flex: 1;
        height: 8px;
        border-radius: 999px;
        background: var(--hf-surface-2);
        border: 1px solid var(--hf-border);
        overflow: hidden;
    }}

    .hf-confidence-fill {{
        height: 100%;
        width: 0%;
        border-radius: 999px;
        background: var(--hf-gradient);
        transform-origin: left;
        box-shadow: 0 0 12px
            color-mix(in srgb, var(--hf-accent) 55%, transparent);
    }}

    .hf-confidence-value {{
        font-size: .8rem;
        font-weight: 700;
        min-width: 42px;
        text-align: right;
    }}

    .hf-reasons {{
        font-size: .8rem;
        color: var(--hf-muted);
        margin: .25rem 0 0 0;
    }}

    /* ===========================
       Inputs & buttons
    =========================== */

    .stChatInput, div[data-testid="stChatInput"] {{
        border-radius: 14px;
    }}

    div[data-testid="stChatInput"] textarea,
    .stTextInput input {{
        background: var(--hf-input-bg) !important;
        color: var(--hf-text) !important;
        border: 1px solid var(--hf-border-strong) !important;
        border-radius: 14px !important;
    }}

    div[data-testid="stChatInput"] textarea::placeholder,
    .stTextInput input::placeholder {{
        color: var(--hf-muted) !important;
    }}

    .stButton > button {{
        width: 100%;
        border-radius: 12px;
        border: 1px solid var(--hf-border-strong);
        background: var(--hf-surface-2);
        color: var(--hf-text);
        font-weight: 600;
        padding: .6rem;
        transition: transform .25s ease, box-shadow .25s ease,
                    border-color .25s ease;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        border-color: var(--hf-accent);
        box-shadow: 0 8px 22px var(--hf-accent-soft);
        color: var(--hf-text);
    }}

    div[data-testid="stDownloadButton"] > button {{
        width: 100%;
        border-radius: 12px;
        border: 1px solid color-mix(in srgb, var(--hf-accent) 55%, transparent);
        background: var(--hf-accent-soft);
        color: var(--hf-text);
        font-weight: 600;
        transition: transform .25s ease, box-shadow .25s ease;
    }}

    div[data-testid="stDownloadButton"] > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 22px var(--hf-accent-soft);
        color: var(--hf-text);
    }}

    /* ===========================
       File uploader
    =========================== */

    div[data-testid="stFileUploaderDropzone"] {{
        border: 1.5px dashed var(--hf-border-strong);
        border-radius: 18px;
        padding: 18px;
        background: var(--hf-surface-2);
        transition: border-color .25s ease, box-shadow .25s ease;
    }}

    div[data-testid="stFileUploaderDropzone"]:hover {{
        border-color: var(--hf-accent);
        box-shadow: 0 0 0 4px var(--hf-accent-soft);
    }}

    div[data-testid="stFileUploaderDropzone"] *,
    div[data-testid="stFileUploader"] * {{
        color: var(--hf-text);
    }}

    /* ===========================
       Expanders / code / tables
    =========================== */

    details {{
        border-radius: 14px;
        border: 1px solid var(--hf-border);
        background: var(--hf-surface-2);
        margin-bottom: 12px;
    }}

    summary {{
        font-weight: 600;
        padding: 6px;
        color: var(--hf-text);
    }}

    pre {{
        border-radius: 14px;
        border: 1px solid var(--hf-border);
        background: var(--hf-input-bg);
    }}

    div[data-testid="stDataFrame"] {{
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid var(--hf-border);
        box-shadow: var(--hf-shadow);
    }}

    /* ===========================
       Alerts
    =========================== */

    div[data-testid="stAlert"] {{
        border-radius: 14px;
        border: 1px solid var(--hf-border);
        backdrop-filter: blur(8px);
    }}

    /* ===========================
       Spinner
    =========================== */

    div[data-testid="stSpinner"], .stSpinner {{
        color: var(--hf-muted);
        font-weight: 500;
    }}

    /* ===========================
       Theme toggle
    =========================== */

    .hf-theme-toggle > button {{
        border-radius: 999px;
        font-size: .9rem;
        padding: .45rem;
    }}

    /* ===========================
       Scrollbar
    =========================== */

    ::-webkit-scrollbar {{ width: 10px; }}
    ::-webkit-scrollbar-track {{ background: var(--hf-bg); }}
    ::-webkit-scrollbar-thumb {{
        background: var(--hf-scroll-thumb, #2A3A5C);
        border-radius: 20px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--hf-accent);
    }}

    /* ===========================
       Mobile
    =========================== */

    @media (max-width: 640px) {{
        .main .block-container {{ padding-top: 1rem; }}
        .hf-title {{ font-size: 1.7rem; }}
        .hf-chip {{ font-size: .78rem; padding: .34rem .7rem; }}
        .stChatMessage {{ padding: 12px 13px; border-radius: 14px; }}
    }}

    </style>
    """


def load_css():
    """Render the active theme's stylesheet."""

    st.markdown(
        _css(_PALETTES[get_theme()]),
        unsafe_allow_html=True
    )
