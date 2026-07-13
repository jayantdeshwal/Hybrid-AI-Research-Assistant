from utils.llm import llm
from utils.parser import extract_code

def generate_query(question, df):

    columns = df.columns.tolist()

    prompt = f"""
You are a senior pandas expert.

The dataframe name is df.

Available columns:
{columns}

Order Date and Ship Date are datetime columns.

Rules:

1. Understand the business question.

2. Aggregate before ranking.

3. Use groupby when needed.

4. For trends over time use:
pd.Grouper(key='Order Date', freq='ME')

5. If the output will likely be visualized,
prefer using reset_index().

IMPORTANT:
Return ONLY a pandas expression.
No explanation.
No markdown.
No code fences.

Question:
{question}
"""

    response = llm.invoke(prompt)

    return extract_code(
        response.content
    )




def fix_query(
    question,
    query,
    error
):

    prompt = f"""
You are a senior pandas expert.

Question:
{question}

Failed Query:
{query}

Error:
{error}

Fix the query.

Return ONLY the corrected pandas expression.
No explanation.
No markdown.
"""

    response = llm.invoke(prompt)

    return extract_code(
        response.content
    )

