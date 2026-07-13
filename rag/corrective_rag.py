from rag.retriever import retrieve_documents
from rag.grader import grade_retrieval
from rag.query_rewriter import rewrite_query


def corrective_retrieval(
    vectorstore,
    question
):

    docs = retrieve_documents(
        vectorstore,
        question
    )

    is_relevant = grade_retrieval(
        question,
        docs
    )

    print(
        "Retrieval Relevant:",
        is_relevant
    )

    if is_relevant:
        return docs, True

    rewritten_question = rewrite_query(
        question
    )

    print(
        "Rewritten Question:",
        rewritten_question
    )

    docs = retrieve_documents(
        vectorstore,
        rewritten_question
    )

    return docs, False