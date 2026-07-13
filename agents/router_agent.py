from utils.llm import llm
import ast

def route_question(
    question,
    has_csv=False,
    has_pdf=False
):

    prompt = f"""
You are an AI planning agent.

Your job is to decide which tools are needed to answer a user's question.

Available tools:

1. csv
Use when:
- analyzing uploaded CSV data
- sales
- profit
- regions
- trends
- dataset columns

2. document
Use when:
- answering questions from uploaded PDFs
- reports
- research papers
- policies

3. sql
Use when:
- user explicitly asks for SQL
- SQL query
- database query
- write SQL
- using SQL

4. web
Use when:
- current events
- latest news
- internet information
- recent trends
- information not present in uploaded files

5. chat
Use when:
- greetings
- coding help
- explanations
- general conversation
- no external information is required

Current Context:

CSV Uploaded:
{has_csv}

PDF Uploaded:
{has_pdf}

Question:
{question}

Priority Rules:

1. Prefer uploaded data over web search whenever possible.

2. Only use web when the uploaded files cannot answer the question completely.

3. If the user explicitly asks for current/latest/recent information, include web.

4. If the user explicitly requests SQL, include sql.

5. If both uploaded files and web are needed, return both tools.

6. Use the minimum number of tools necessary.


Rules:

-Return ONLY a valid Python list.

Examples:

["chat"]

["csv"]

["sql"]

["document"]

["web"]

["csv","web"]

["document","web"]

["csv","sql","web"]

Never explain.

Never use markdown.

Return ONLY the Python list.

Examples:

Question:
Who is the CEO of Microsoft?

Answer:
["web"]

Question:
Explain the uploaded paper.

Answer:
["document"]

Question:
Highest sales region.

Answer:
["csv"]

Question:
Monthly sales trend using SQL.

Answer:
["sql"]

Question:
Compare my sales with industry trends.

Answer:
["csv","web"]

Question:
Compare the uploaded paper with recent research.

Answer:
["document","web"]

Question:
Analyze my sales and explain whether they follow industry trends using SQL.

Answer:
["csv","sql","web"]
"""

    response = (
        llm.invoke(prompt)
        .content
        .strip()
        .lower()
    )



    try:

        tools = ast.literal_eval(response)

        if isinstance(tools, str):
            tools = [tools]

    except Exception:

        tools = ["chat"]



    return[
        tool.lower()
        for tool in tools
]



