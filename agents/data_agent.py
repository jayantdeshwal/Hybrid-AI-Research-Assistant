from utils.query_generator import generate_query
from utils.executor import execute_with_retry
from utils.explanation import explain_result
from utils.visualizer import (
    needs_visualization,
    detect_chart_type,
    create_chart
)
from utils.question_rewriter import rewrite_question
from utils.response_schema import create_response
import pandas as pd


def data_agent(
    question,
    df,
    previous_question=None,
    previous_result=None
):

    # ------------------------------------
    # Memory Rewriting
    # ------------------------------------

    if previous_question:

        question = rewrite_question(
            question,
            previous_question,
            previous_result
        )

        print(
            f"Rewritten Question: {question}"
        )

    if previous_question:

        question = f"""
Previous question:
{previous_question}

Current question:
{question}
"""

    # ------------------------------------
    # Query Generation
    # ------------------------------------

    query = generate_query(
        question,
        df
    )

    # ------------------------------------
    # Execute Query
    # ------------------------------------

    try:
        query, result = execute_with_retry(
            question,
            query,
            df
        )

    except Exception as e:

        return create_response(
            tool="csv",
            success=False,
            answer=f"Failed to execute generated query.\n\n{str(e)}",
            source="CSV DataFrame"
        )

    

    if isinstance(result, pd.Series):
        result = result.to_frame()

    elif not isinstance(result, pd.DataFrame):
        result = pd.DataFrame({"Result": [result]})

    # ------------------------------------
    # Visualization
    # ------------------------------------

    chart = None

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

    # ------------------------------------
    # Business Explanation
    # ------------------------------------

    explanation = explain_result(
        question,
        result
    )

    # ------------------------------------
    # Standard Response
    # ------------------------------------

    return create_response(
        tool="csv",
        success=True,
        answer=explanation,
        data=result,
        query=query,
        chart=chart,
        explanation=explanation,
        source="CSV DataFrame"
    )