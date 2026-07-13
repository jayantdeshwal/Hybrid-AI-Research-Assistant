from utils.llm import llm


def grade_retrieval(
    question,
    docs
):
    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = f"""
You are a retrieval evaluator.

Question:
{question}

Retrieved Context:
{context}

Determine whether the retrieved context contains information
that can help answer the question.

Reply with ONLY:

yes

or

no
"""

    response = llm.invoke(
        prompt
    ).content.strip().lower()

    return response == "yes"