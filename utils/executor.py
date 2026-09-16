import pandas as pd
import numpy as np
from datetime import datetime
from utils.query_generator import fix_query


def execute_query(query,df):

    try:

        return eval(
            query,
            {
                "__builtins__": __builtins__,
                "df": df,
                "pd": pd,
                "np": np,
                "datetime": datetime
            }
        )

    except Exception as e:

        return str(e)
    

def execute_with_retry(question, query, df):

    result = execute_query(query, df)

    if not isinstance(result, str):
        return query, result

    print("Error:")
    print(result)

    fixed_query = fix_query(
        question,
        query,
        result
    )

    print("\nFixed Query:")
    print(fixed_query)

    result = execute_query(fixed_query, df)

    # Retry succeeded
    if not isinstance(result, str):
        return fixed_query, result

    # Retry also failed
    raise Exception(result)