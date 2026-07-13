from sql.query_generator import generate_sql
from sql.executor import execute_sql
from sql.validator import validate_sql

from utils.response_schema import create_response


def sql_agent(
    question,
    conn,
    df
):

    if conn is None:

        return create_response(
            tool="sql",
            success=False,
            answer="Please upload a CSV file first.",
            source="SQLite Database"
        )

    columns = df.columns.tolist()

    query = generate_sql(
        question,
        columns
    )

    if not validate_sql(query):

        return create_response(
            tool="sql",
            success=False,
            answer="Unsafe SQL query generated.",
            source="SQLite Database",
            query=query
        )

    try:

        result = execute_sql(
            conn,
            query
        )

    except Exception as e:

        return create_response(
            tool="sql",
            success=False,
            answer=f"SQL execution failed:\n{str(e)}",
            source="SQLite Database",
            query=query
        )

    return create_response(
        tool="sql",
        success=True,
        answer="SQL query executed successfully.",
        data=result,
        query=query,
        chart=None,
        explanation="SQL query executed successfully.",
        source="SQLite Database"
    )