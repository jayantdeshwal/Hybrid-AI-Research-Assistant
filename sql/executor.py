import pandas as pd


def execute_sql(
    conn,
    query
):

    result = pd.read_sql_query(
        query,
        conn
    )

    return result