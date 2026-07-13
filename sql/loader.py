import sqlite3
import pandas as pd


def create_database(df):

    conn = sqlite3.connect(
        "temp.db",
        check_same_thread=False
    )

    df.to_sql(
        "sales_data",
        conn,
        if_exists="replace",
        index=False
    )

    return conn