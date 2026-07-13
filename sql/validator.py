def validate_sql(query):

    dangerous_keywords = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "REPLACE"
    ]

    upper_query = query.upper()

    for keyword in dangerous_keywords:
        if keyword in upper_query:
            return False

    return True