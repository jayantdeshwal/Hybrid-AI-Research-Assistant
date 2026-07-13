import re

def extract_code(response):

    match = re.search(
        r"```(?:python)?\n(.*?)```",
        response,
        re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return response.strip()