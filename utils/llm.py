import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

if not os.getenv("GROQ_API_KEY"):

    # Streamlit Cloud stores keys in
    # st.secrets - fall back to it.

    try:

        import streamlit as st

        os.environ["GROQ_API_KEY"] = (
            st.secrets["GROQ_API_KEY"]
        )

    except Exception:
        pass

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# ==========================================
# Groq model selection
# ==========================================
# Preference order: GROQ_MODEL env var, then
# the best Groq-hosted open models. If the
# configured model ever gets deprecated,
# fall back automatically so the app keeps
# working. Groq-only: uses GROQ_API_KEY.
# ==========================================

PREFERRED_MODELS = [
    "openai/gpt-oss-120b",
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-20b",
    "groq/compound",
]


def _resolve_model():

    requested = os.getenv("GROQ_MODEL")

    if requested:
        return requested

    try:

        from groq import Groq

        client = Groq(
            timeout=8,
            max_retries=0
        )

        available = [
            m.id
            for m in client.models.list().data
        ]

    except Exception:

        # Can't check right now (offline, key
        # problem, etc.) - let init_chat_model
        # surface any real error.

        return PREFERRED_MODELS[0]

    for model in PREFERRED_MODELS:

        if model in available:
            return model

    # Nothing preferred is offered - use the
    # first non-audio, non-guard model Groq
    # has so the app still works.

    skip = (
        "whisper",
        "orpheus",
        "prompt-guard",
        "safeguard"
    )

    for model in available:

        if not any(s in model for s in skip):
            return model

    return PREFERRED_MODELS[0]


RESOLVED_MODEL = _resolve_model()

llm = init_chat_model(
    model=RESOLVED_MODEL,
    model_provider="groq"
)