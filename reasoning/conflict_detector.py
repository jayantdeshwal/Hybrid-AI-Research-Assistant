from utils.llm import llm


def detect_conflicts(
    question,
    ranked_items
):
    """
    Detect whether multiple evidence sources
    contradict each other.
    """

    if len(ranked_items) <= 1:

        return {
            "has_conflict": False,
            "summary": "Only one evidence source."
        }

    evidence_text = ""

    for item in ranked_items:

        evidence = item["evidence"]

        evidence_text += f"""

Source:
{evidence["source"]}

Answer:
{evidence["response"]["answer"]}

"""

    prompt = f"""
You are an evidence verification assistant.

Question:
{question}

Evidence:

{evidence_text}

Determine whether the evidence contains factual conflicts.

Ignore differences in wording.

Only identify real contradictions.

Return exactly in this format:

Conflict:
yes/no

Summary:
<one sentence>
"""

    response = llm.invoke(prompt).content

    has_conflict = "yes" in response.lower()

    return {
        "has_conflict": has_conflict,
        "summary": response
    }