from utils.llm import llm
import json


def build_reasoning_plan(
    question,
    evidence,
    conflict_result
):

    prompt = f"""
You are the reasoning engine of an AI research assistant.

Do NOT answer the user's question.

Your task is to analyze the collected evidence and create a reasoning plan.

Question:
{question}

Evidence:
{evidence}

Conflict Analysis:
{conflict_result}

Identify:

1. Question Type
2. Common Information
3. Unique Information from each source
4. Missing Information
5. Recommended answer structure

Return ONLY valid JSON.

Example:

{{
    "question_type":"comparison",
    "common_points":[
        "...",
        "..."
    ],
    "unique_points":{{
        "document":[
            "...",
            "..."
        ],
        "web":[
            "...",
            "..."
        ]
    }},
    "missing_information":"",
    "recommended_structure":[
        "Introduction",
        "Similarities",
        "Differences",
        "Conclusion"
    ]
}}
"""

    response = llm.invoke(prompt).content.strip()

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    try:
        return json.loads(response)

    except Exception:

        print("\nReflection JSON Parsing Failed\n")
        print(response)

        return {
            "question_type":"general",
            "common_points":[],
            "unique_points":{},
            "missing_information":"",
            "recommended_structure":[]
        }