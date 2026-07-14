from langchain_community.vectorstores import FAISS

from rag.embeddings import (
    get_embedding_model
)


def create_vectorstore(chunks):

    print("Before get_embedding_model()")

    embeddings = get_embedding_model()

    print("After get_embedding_model()")

    print("Before FAISS")

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    print("After FAISS")

    return vectorstore