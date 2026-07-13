from typing import TypedDict
import pandas as pd


class AgentState(TypedDict):

    question: str

    rewritten_question: str

    query: str

    result: object

    chart: object

    explanation: str

    previous_question: str

    previous_result: object

    df: pd.DataFrame