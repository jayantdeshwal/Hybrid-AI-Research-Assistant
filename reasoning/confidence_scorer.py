def score_confidence(
    ranked_evidence,
    conflict_report
):
    """
    Compute confidence based on evidence quality
    and agreement between sources.
    """

    if len(ranked_evidence) == 0:

        return {
            "score": 0,
            "level": "Low",
            "reason": [
                "No reliable evidence available."
            ]
        }

    # ---------------------------------------
    # Average evidence score
    # ---------------------------------------

    total_score = sum(
        item["evaluation"]["score"]
        for item in ranked_evidence
    )

    avg_score = (
        total_score /
        len(ranked_evidence)
    )

    confidence = avg_score * 10

    reasons = []

    reasons.append(
        f"Average evidence quality: {avg_score:.1f}/10."
    )

    # ---------------------------------------
    # Source bonus
    # ---------------------------------------

    source_count = len(ranked_evidence)

    if source_count >= 3:

        confidence += 10

        reasons.append(
            "Multiple independent sources were used."
        )

    elif source_count == 2:

        confidence += 5

        reasons.append(
            "Two sources support the answer."
        )

    else:

        reasons.append(
            "Only one source available."
        )

    # ---------------------------------------
    # Conflict penalty
    # ---------------------------------------

    if conflict_report["has_conflict"]:

        confidence -= 20

        reasons.append(
            "Conflicting evidence detected."
        )

    else:

        confidence += 5

        reasons.append(
            "No conflicts detected."
        )

    # ---------------------------------------
    # Clamp score
    # ---------------------------------------

    confidence = max(
        0,
        min(
            int(confidence),
            100
        )
    )

    # ---------------------------------------
    # Confidence level
    # ---------------------------------------

    if confidence >= 85:

        level = "High"

    elif confidence >= 60:

        level = "Medium"

    else:

        level = "Low"

    return {

        "score": confidence,

        "level": level,

        "reason": reasons

    }