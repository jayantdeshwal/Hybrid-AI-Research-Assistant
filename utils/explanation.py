from utils.llm import llm

def explain_result(
    question,
    result
):

    prompt = f"""
You are a business analyst.

Question:
{question}

Result:
{result}

Explain the result.

Do not make assumptions.
Keep it concise.
"""

    return llm.invoke(
        prompt
    ).content