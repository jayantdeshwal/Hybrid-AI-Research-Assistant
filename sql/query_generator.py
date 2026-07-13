from utils.llm import llm


def generate_sql(
    question,
    columns
):

    prompt = f"""
You are an expert SQL analyst.

Database engine: SQLite

Table name:
sales_data

Available columns:
{columns}

Rules:
1. Return ONLY SQL.
2. Use only the table sales_data.
3. Use only the provided columns.
4. Do NOT use PostgreSQL functions like:
   - EXTRACT()
   - DATE_TRUNC()
   - ILIKE
5. For dates in SQLite use:
   strftime('%Y', column)
   strftime('%m', column)
   strftime('%Y-%m', column)
6. Always use double quotes around column names that contain spaces.

Examples:

Question:
Monthly sales trend

SQL:
SELECT
    strftime('%Y-%m', "Order Date") AS Month,
    SUM(Sales) AS Total_Sales
FROM sales_data
GROUP BY Month
ORDER BY Month;

Question:
Top 5 products by sales

SQL:
SELECT
    "Product Name",
    SUM(Sales) AS Total_Sales
FROM sales_data
GROUP BY "Product Name"
ORDER BY Total_Sales DESC
LIMIT 5;

Question:
{question}
"""

    sql_query = llm.invoke(prompt).content

    sql_query = (
        sql_query
        .replace("```sql", "")
        .replace("```", "")
        .strip()
    )

    return sql_query