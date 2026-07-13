from rag.rag_agent import answer_question
from utils.response_schema import create_response


def document_agent(
    question,
    vectorstore
):

    if vectorstore is None:

        return create_response(
            tool="document",
            success=False,
            answer=(
                "Please upload a PDF first to ask "
                "questions about a document."
            ),
            source="PDF RAG"
        )

    answer = answer_question(
        vectorstore,
        question
    )

    return create_response(
        tool="document",
        success=True,
        answer=answer,
        source="PDF RAG"
    )