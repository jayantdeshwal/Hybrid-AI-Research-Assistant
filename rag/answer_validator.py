from rag.self_rag import (
    check_context_sufficiency,
    critique_answer
)


def validate_answer(
    question,
    answer,
    docs
):
    """
    Returns:
    {
        "context_sufficient": bool,
        "answer_supported": bool
    }
    """

    context_sufficient = (
        check_context_sufficiency(
            question,
            docs
        )
    )

    answer_status = (
        critique_answer(
            question,
            answer,
            docs
        )
    )

    return {
        "context_sufficient": context_sufficient,
        "answer_supported":
            answer_status == "supported"
    }