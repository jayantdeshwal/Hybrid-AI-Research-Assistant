from agents.query_agent import generate_query
from agents.visualization_agent import generate_chart
from utils.explanation import explain_result
from utils.question_rewriter import rewrite_question
from utils.executor import execute_query


def rewrite_node(state):

    question = state["question"]

    previous_question = state.get(
        "previous_question"
    )

    previous_result = state.get(
        "previous_result"
    )

    if previous_question:

        question = rewrite_question(
            question,
            previous_question,
            previous_result
        )

    state["rewritten_question"] = question

    return state




from agents.query_agent import generate_query


def query_node(state):

    query = generate_query(
        state["rewritten_question"],
        state["df"]
    )

    state["query"] = query

    return state





from utils.executor import execute_query


def execute_node(state):

    result = execute_query(
        state["query"],
        state["df"]
    )

    state["result"] = result

    return state





from utils.explanation import explain_result


def explanation_node(state):

    explanation = explain_result(
        state["rewritten_question"],
        state["result"]
    )

    state["explanation"] = explanation

    return state


from utils.visualizer import (
    needs_visualization,
    detect_chart_type,
    create_chart
)


def visualization_node(state):

    chart = None

    question = state["rewritten_question"]

    result = state["result"]

    if needs_visualization(question):

        chart_type = detect_chart_type(
            question
        )

        try:
            chart = create_chart(
                result,
                chart_type
            )
        except:
            chart = None

    state["chart"] = chart

    return state

from langgraph.graph import (
    StateGraph,
    END
)

from Project1.workflows.state import AgentState

builder = StateGraph(
    AgentState
)

builder.add_node(
    "rewrite",
    rewrite_node
)

builder.add_node(
    "query",
    query_node
)

builder.add_node(
    "execute",
    execute_node
)

builder.add_node(
    "visualize",
    visualization_node
)

builder.add_node(
    "explain",
    explanation_node
)

builder.set_entry_point(
    "rewrite"
)

builder.add_edge(
    "rewrite",
    "query"
)

builder.add_edge(
    "query",
    "execute"
)

builder.add_edge(
    "execute",
    "visualize"
)

builder.add_edge(
    "visualize",
    "explain"
)

builder.add_edge(
    "explain",
    END
)

graph = builder.compile()







