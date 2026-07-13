def rerank_documents(
    question,
    docs,
    top_k=4
):
    """
    Placeholder reranker.

    Later we can replace this with:
    - BGE Reranker
    - Cohere Rerank
    - Cross Encoder

    For now we simply keep the top chunks.
    """

    return docs[:top_k]