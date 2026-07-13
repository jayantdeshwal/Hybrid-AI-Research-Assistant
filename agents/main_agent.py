from agents.router_agent import route_question
from agents.hybrid_agent import hybrid_agent


def main_agent(
    question,
    df=None,
    vectorstore=None,
    last_question=None,
    last_result=None,
    sql_connection=None
):

    tools = route_question(
        question,
        has_csv=df is not None,
        has_pdf=vectorstore is not None
    )

    print("Selected Tools:", tools)

    # Remove unavailable tools
    available_tools = {
    "chat",
    "web"
}

    if df is not None:
        available_tools.add("csv")

    if vectorstore is not None:
        available_tools.add("document")

    if sql_connection is not None:
        available_tools.add("sql")

    tools = [
        tool
        for tool in tools
        if tool in available_tools
    ]

    if not tools:
        tools = ["chat"]



    # If nothing remains, use chat
    if len(tools) == 0:
        tools = ["chat"]

    return hybrid_agent(
        question=question,
        tools=tools,
        df=df,
        vectorstore=vectorstore,
        sql_connection=sql_connection,
        last_question=last_question,
        last_result=last_result
    )