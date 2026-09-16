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

    # ----------------------------------------
    # Carry data artifacts from the
    # highest-ranked evidence that has them
    # ----------------------------------------

    best = None

    for item in ranked_evidence:

        response = item["evidence"]["response"]

        if response.get("data") is not None:
            best = response
            break

    return {

        "tool": "chat",

        "success": True,

        "answer": answer,

        "route": route,

        "source": "Hybrid AI",

        "metadata": {
            "sources": sources
        },

        "sources": sources,

        "confidence": confidence["score"],

        "confidence_reason": confidence["reason"],

        "conflict": (
            conflict_report["summary"]
            if conflict_report
            else None
        ),

        "data": best.get("data") if best else None,

        "query": best.get("query") if best else None,

        "chart": best.get("chart") if best else None,

        "explanation": (
            best.get("explanation") if best else None
        )
    }