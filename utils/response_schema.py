def create_response(
    tool,
    success=True,
    answer=None,
    data=None,
    query=None,
    chart=None,
    explanation=None,
    source=None,
    metadata=None
):
    """
    Standard response format used by every agent.
    """

    return {
        "tool": tool,
        "success": success,
        "answer": answer,
        "data": data,
        "query": query,
        "chart": chart,
        "explanation": explanation,
        "source": source,
        "metadata": metadata or {}
    }