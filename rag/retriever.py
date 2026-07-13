def retrieve_documents(
    vectorstore,
    question,
    k=10
):

    if vectorstore is None:
        return []

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": k}
    )

    docs = retriever.invoke(question)

    return docs