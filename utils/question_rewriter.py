from utils.llm import llm


def rewrite_question(
    question,
    previous_question,
    previous_result
):

    prompt = f"""
You are helping a conversational data analyst.

Previous Question:
{previous_question}

Previous Result:
{previous_result}

Current User Question:
{question}

If the current question depends on previous context,
rewrite it into a standalone question.

Otherwise return the original question.

Return only the rewritten question.
"""

    return llm.invoke(prompt).content.strip()