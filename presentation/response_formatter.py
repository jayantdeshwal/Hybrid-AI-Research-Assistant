def format_response(
    answer,
    confidence,
    route,
    ranked_evidence,
    conflict_report=None
):

    sources = []

    for item in ranked_evidence:

        source = item["evidence"]["source"]

        if source not in sources:
            sources.append(source)

    return {

        "tool": "chat",

        "success": True,

        "answer": answer,

        "route": route,

        "source": "Hybrid AI",

        "metadata": {
            "sources": sources
        },  

        "confidence": confidence["score"],

        "confidence_reason": confidence["reason"],

        "conflict": (
            conflict_report["summary"]
            if conflict_report
            else None
        ),

        "data": None,

        "query": None,

        "chart": None,

        "explanation": None
    }