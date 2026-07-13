def build_merge_prompt(
    question,
    evidence
):

    prompt = f"""
You are an expert AI Business Analyst.

You have received information from multiple trusted AI systems.

Each system specializes in a different source of knowledge such as:
- Uploaded documents
- Uploaded datasets
- SQL databases
- Internet search

Your task is to produce ONE final answer for the user.

IMPORTANT RULES:

1. Combine all useful information naturally.
2. Remove duplicated information.
3. If two sources provide complementary information, combine them.
4. If one source cannot answer but another source can, mention that naturally.
5. Never mention internal tool names like "csv", "document", "sql", or "web".
6. Never mention "Agent 1" or "Tool 1".
7. Never invent information.
8. If information is missing, clearly state what is unavailable.
9. Write in professional Markdown.
10. Keep the answer concise but informative.

Use the following structure whenever appropriate:

# Summary

Brief answer.

# Key Findings

- Point 1
- Point 2
- Point 3

# Conclusion

A short concluding paragraph.

----------------------------------------

Available Information:

"""

    for i, item in enumerate(evidence, start=1):

        prompt += f"""

Source {i}

Source Name:
{item["source"]}

Information:
{item["response"]["answer"]}

----------------------------------------
"""

    prompt += f"""

User Question:

{question}

Now produce the final answer.
"""

    return prompt