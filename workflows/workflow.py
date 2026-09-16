from langgraph.graph import (
    StateGraph,
    END
)

from workflows.state import AgentState

from utils.question_rewriter import rewrite_question
from utils.query_generator import generate_query
from utils.executor import execute_query
from utils.explanation import explain_result
from utils.visualizer import (
    needs_visualization,
    detect_chart_type,
    create_chart
)


# ==========================================
# Nodes
# ==========================================

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


def query_node(state):

    query = generate_query(
        state["rewritten_question"],
        state["df"]
    )

    state["query"] = query

    return state


def execute_node(state):

    result = execute_query(
        state["query"],
        state["df"]
    )

    state["result"] = result

    return state


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
        except Exception:
            chart = None

    state["chart"] = chart

    return state


def explanation_node(state):

    explanation = explain_result(
        state["rewritten_question"],
        state["result"]
    )

    state["explanation"] = explanation

    return state


# ==========================================
# Graph
# ==========================================

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
