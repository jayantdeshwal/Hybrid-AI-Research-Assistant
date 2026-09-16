from utils.llm import llm


def check_context_sufficiency(
    question,
    docs
):
    """
    Returns True when the retrieved context
    contains enough information to answer
    the question.
    """

    if not docs:
        return False

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = f"""
You are a retrieval quality inspector.

Question:
{question}

Retrieved Context:
{context}

Determine whether the retrieved context
contains enough information to fully
answer the question.

Reply with ONLY:

yes

or

no
"""

    response = llm.invoke(
        prompt
    ).content.strip().lower()

    return response.startswith("yes")


def critique_answer(
    question,
    answer,
    docs
):
    """
    Returns "supported" when the answer is
    grounded in the provided documents,
    otherwise "unsupported".
    """

    if not docs:
        return "unsupported"

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = f"""
You are a strict answer verifier.

Question:
{question}

Answer:
{answer}

Retrieved Context:
{context}

Is the answer fully supported by the
retrieved context?

Reply with ONLY one word:

supported

or

unsupported
"""

    response = llm.invoke(
        prompt
    ).content.strip().lower()

    if "unsupported" in response:
        return "unsupported"

    if "supported" in response:
        return "supported"

    return "unsupported"
