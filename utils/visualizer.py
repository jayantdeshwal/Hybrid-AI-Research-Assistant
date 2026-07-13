import matplotlib.pyplot as plt
import pandas as pd

from utils.llm import llm
from utils.schemas import ChartType


chart_llm = llm.with_structured_output(
    ChartType
)


# =========================
# Should we create a chart?
# =========================

def needs_visualization(question):

    question = question.lower()

    # Don't create charts for these queries
    no_chart_keywords = [
        "first one",
        "first product",
        "show only",
        "only the first",
        "only the top"
    ]

    if any(
        keyword in question
        for keyword in no_chart_keywords
    ):
        return False

    chart_keywords = [
        "chart",
        "graph",
        "plot",
        "trend",
        "visualize",
        "distribution",
        "share",
        "compare",
        "comparison",
        "across",
        "by"
    ]

    return any(
        keyword in question
        for keyword in chart_keywords
    )


# =========================
# Detect chart type
# =========================

def detect_chart_type(question):

    prompt = f"""
You are a data visualization expert.

Choose one:

- bar
- line
- pie
- histogram

Rules:

Trend over time -> line
Distribution -> histogram
Share -> pie
Category comparison -> bar

Question:
{question}
"""

    response = chart_llm.invoke(
        prompt
    )

    return response.chart_type.lower()


# =========================
# Create chart
# =========================

def create_chart(
    result,
    chart_type
):

    # Only DataFrames and Series
    if not isinstance(
        result,
        (pd.DataFrame, pd.Series)
    ):
        return None

    if len(result) == 0:
        return None

    # =====================
    # Handle Series
    # =====================

    if isinstance(result, pd.Series):

        fig, ax = plt.subplots(
            figsize=(10, 5)
        )

        if chart_type == "line":

            ax.plot(
                result.index.astype(str),
                result.values
            )

        elif chart_type == "bar":

            ax.bar(
                result.index.astype(str),
                result.values
            )

        elif chart_type == "histogram":

            ax.hist(
                result.values
            )

        elif chart_type == "pie":

            ax.pie(
                result.values,
                labels=result.index.astype(str),
                autopct="%1.1f%%"
            )

        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

    # =====================
    # Handle DataFrame
    # =====================

    if result.shape[1] < 2:
        return None

    numeric_cols = result.select_dtypes(
        include="number"
    ).columns.tolist()

    if len(numeric_cols) == 0:
        return None

    non_numeric_cols = result.select_dtypes(
        exclude="number"
    ).columns.tolist()

    # x-axis
    if len(non_numeric_cols) > 0:
        x_col = non_numeric_cols[0]
    else:
        x_col = result.columns[0]

    # y-axis
    y_col = numeric_cols[0]

    fig, ax = plt.subplots(
        figsize=(10, 5)
    )

    if chart_type == "line":

        ax.plot(
            result[x_col],
            result[y_col]
        )

    elif chart_type == "bar":

        ax.bar(
            result[x_col].astype(str),
            result[y_col]
        )

    elif chart_type == "histogram":

        ax.hist(
            result[y_col]
        )

    elif chart_type == "pie":

        ax.pie(
            result[y_col],
            labels=result[x_col].astype(str),
            autopct="%1.1f%%"
        )

    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig