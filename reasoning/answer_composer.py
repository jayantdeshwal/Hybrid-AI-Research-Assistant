from utils.llm import llm
import json

def compose_answer(
    question,
    reasoning_plan,
    ranked_evidence,
    conflict_summary=None
):
    evidence_text = ""

    for item in ranked_evidence:

        evidence_text += f"""

    Source:
    {item["source"]}

    Answer:
    {item["response"]["answer"]}

    """
        
    reasoning_text = json.dumps(
    reasoning_plan,
    indent=2
)
    

    prompt = f"""
You are a senior AI analyst.

A separate reasoning system has already analyzed all evidence.

Your task is ONLY to write the final answer.

Do NOT perform new reasoning.

Use the reasoning plan below.

======================================

Question

{question}

======================================

Reasoning Plan

{reasoning_text}

======================================

Conflict Summary

{conflict_summary}

======================================

Evidence

{evidence_text}

======================================

Instructions

1. Follow the recommended structure.

2. Begin with a direct answer.

3. Explain common findings first.

4. Then explain unique findings.

5. Mention missing information if any.

6. Never invent facts.

7. Never repeat the same information.

8. Produce a professional report.

9. Use markdown headings.

10. Finish with a concise conclusion.

11. Never omit important information from the reasoning plan, even if another source appears more detailed.
Final Answer:
"""
    
    answer = llm.invoke(prompt).content

    return answer


        