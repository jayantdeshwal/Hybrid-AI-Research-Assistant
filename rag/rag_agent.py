from utils.llm import llm
from rag.corrective_rag import corrective_retrieval
from rag.reranker import (
    rerank_documents
)


def answer_question(
    vectorstore,
    question
):
    docs, retrieval_status = (
        corrective_retrieval(
            vectorstore,
            question
        )
    )

    print("\n========== Before Reranking ==========")
    print("Number of docs:", len(docs))
    docs = rerank_documents(
    question,
    docs
)
    print("\n========== After Reranking ==========")
    print("Number of docs:", len(docs))

    for i, doc in enumerate(docs):
        print(f"\nRank {i+1}")
        print(doc.page_content[:300])

    if len(docs) == 0:
        return (
        "I could not find relevant information "
        "in the document."
    )

    print("\n========== Retrieved Documents ==========")

    print("Retrieved:", len(docs))

    for i, doc in enumerate(docs):
        print(f"\nChunk {i+1}")
        print(doc.page_content[:500])


    MAX_CHARS = 8000

    context = ""

    for doc in docs:

        if len(context) > MAX_CHARS:
            break

        context += (
            doc.page_content
            + "\n\n"
        )

    prompt = f"""
You are an Evidence Extraction Agent.

Your ONLY job is to extract information from the document
that is useful for answering the user's question.

Rules:

- Never answer using outside knowledge.
- Never compare with the web.
- Never conclude anything.
- Never say "I don't know" unless absolutely no relevant information exists.
- Extract every relevant fact from the document.
- Return a concise factual summary.

Context:
{context}

User Question:
{question}

Relevant Evidence:
"""
    print("\n========== FINAL CONTEXT ==========\n")
    print(context)

    print("\n========== QUESTION ==========\n")
    print(question)

    answer = (
        llm.invoke(prompt)
        .content
    )

    

    return answer