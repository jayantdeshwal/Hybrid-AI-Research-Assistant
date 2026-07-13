from langchain_community.tools import DuckDuckGoSearchRun

from utils.llm import llm
from utils.response_schema import create_response


search = DuckDuckGoSearchRun()


def web_agent(question):

    results = search.run(question)

    prompt = f"""
You are a helpful assistant.

Use ONLY the search results below to answer the question.

Question:
{question}

Search Results:
{results}
"""

    answer = llm.invoke(prompt).content

    return create_response(
        tool="web",
        success=True,
        answer=answer,
        source="DuckDuckGo Search",
        metadata={
            "search_results": results
        }
    )