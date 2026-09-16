from utils.llm import llm
from utils.response_schema import create_response


def web_agent(question):

    try:
        from langchain_community.tools import (
            DuckDuckGoSearchRun
        )

        search = DuckDuckGoSearchRun()
        results = search.run(question)

    except Exception as e:

        return create_response(
            tool="web",
            success=False,
            answer=(
                "Web search is currently unavailable. "
                f"Error: {str(e)}"
            ),
            source="DuckDuckGo Search"
        )

    prompt = f"""
You are a helpful assistant.

Use ONLY the search results below to answer the question.

Question:
{question}

Search Results:
{results}
"""

    try:

        answer = llm.invoke(prompt).content

    except Exception as e:

        return create_response(
            tool="web",
            success=False,
            answer=(
                "Failed to summarize search results. "
                f"Error: {str(e)}"
            ),
            source="DuckDuckGo Search",
            metadata={
                "search_results": results
            }
        )

    return create_response(
        tool="web",
        success=True,
        answer=answer,
        source="DuckDuckGo Search",
        metadata={
            "search_results": results
        }
    )
