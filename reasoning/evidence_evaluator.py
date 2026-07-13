import json

from utils.llm import llm


def evaluate_evidence(
    question,
    evidence
):
    """
    Evaluates whether a piece of evidence is useful
    for answering the user's question.
    """

    answer = evidence["response"]["answer"]

    prompt = f"""
You are an expert AI evaluator.

Your job is NOT to answer the user's question.

Your job is ONLY to evaluate whether the given evidence
is useful for answering the user's question.

Evaluate the evidence using these criteria:

1. Relevance
- Is the evidence related to the user's question?

2. Informativeness
- Does it contain useful information?

3. Specificity
- Is the information specific instead of generic?

4. Completeness
- Does it answer the whole question or only part of it?

5. Trustworthiness
- Does the information appear factual and grounded?

------------------------

User Question:
{question}

Evidence:
{answer}

------------------------

Return ONLY valid JSON in this format:

{{
    "keep": true,
    "score": 8,
    "reason": "Short explanation"
}}

Rules:

- score must be between 1 and 10.
- keep should be true if score >= 6.
- keep should be false if score < 6.
- Return ONLY JSON.
"""

    response = (
        llm.invoke(prompt)
        .content
        .strip()
    )

    try:
        result = json.loads(response)

    except Exception:

        result = {
            "keep": False,
            "score": 5,
            "reason": "Could not parse evaluator output."
        }

    return result