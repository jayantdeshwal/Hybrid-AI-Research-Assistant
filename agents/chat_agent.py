from utils.llm import llm
from utils.response_schema import create_response


def chat_agent(question):

    answer = llm.invoke(question).content

    return create_response(
        tool="chat",
        success=True,
        answer=answer,
        source="LLM Knowledge"
    )