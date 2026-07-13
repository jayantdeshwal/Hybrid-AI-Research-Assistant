from utils.llm import llm


def rewrite_query(question):

    prompt = f"""
Rewrite the question to improve retrieval.

Question:
{question}

Return only the rewritten question.
"""

    return (
        llm.invoke(prompt)
        .content
        .strip()
    )