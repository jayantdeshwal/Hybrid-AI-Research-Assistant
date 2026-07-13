def rank_evidence(evidence_list):

    ranked = sorted(
        evidence_list,
        key=lambda item: item["evaluation"]["score"],
        reverse=True
    )

    return ranked