from reasoning.evidence_ranker import rank_evidence
from reasoning.conflict_detector import detect_conflicts
from agents.chat_agent import chat_agent
from agents.data_agent import data_agent
from agents.document_agent import document_agent
from agents.sql_agent import sql_agent
from agents.web_agent import web_agent
from reasoning.answer_composer import compose_answer
from utils.llm import llm
from reasoning.evidence_evaluator import evaluate_evidence
from reasoning.reflection import build_reasoning_plan
from reasoning.confidence_scorer import score_confidence
from presentation.response_formatter import format_response



TOOL_REGISTRY = {
    "chat": chat_agent,
    "csv": data_agent,
    "document": document_agent,
    "sql": sql_agent,
    "web": web_agent,
}

def execute_tool(
    tool,
    question,
    df=None,
    vectorstore=None,
    sql_connection=None,
    last_question=None,
    last_result=None
):
    agent = TOOL_REGISTRY[tool]

    if tool == "chat":

        return agent(question)
    
    if tool == "web":

        return agent(question)
    
    if tool == "document":

        return agent(
        question,
        vectorstore
    )

    if tool == "csv":

        return agent(
        question,
        df,
        last_question,
        last_result
    )

    if tool == "sql":

        return agent(
        question,
        sql_connection,
        df
    )


def hybrid_agent(
    question,
    tools,
    df=None,
    vectorstore=None,
    sql_connection=None,
    last_question=None,
    last_result=None
):
    
    evidence = []
    filtered_evidence = []


    for tool in tools:

        print(f"\n========== Executing: {tool} ==========")

        try:

            response = execute_tool(
            tool=tool,
            question=question,
            df=df,
            vectorstore=vectorstore,
            sql_connection=sql_connection,
            last_question=last_question,
            last_result=last_result
        )

            print("Response:")
            print(response)

            evidence.append(
            {
                "tool": tool,
                "source": response.get("source", "Unknown"),
                "response": response
            }
        )

        except Exception as e:

            print(f"ERROR while executing {tool}:")
            print(e)


    print("\n========== Evaluating Evidence ==========")

    for item in evidence:

        evaluation = evaluate_evidence(
            question,
            item
        )

        print(
            item["tool"],
            evaluation
        )

        if evaluation["keep"]:

            filtered_evidence.append(
            {
            "evidence": item,
            "evaluation": evaluation
            }
        )

            
    if len(filtered_evidence) == 0:

        filtered_evidence = [
        {
            "evidence": item,
            "evaluation": {
                "score": 0,
                "reason": "Fallback",
                "keep": True
            }
        }
        for item in evidence
    ]

    if len(filtered_evidence) == 1:
        single_response = {
        **filtered_evidence[0]["evidence"]["response"],
        "route": tools,
        "source": filtered_evidence[0]["evidence"]["source"],
    }

        return single_response
    



    
    ranked_evidence = rank_evidence(filtered_evidence)
    print("\n========== Ranked Evidence ==========")

    for item in ranked_evidence:

        print(
        f"{item['evidence']['tool']} "
        f"-> Score: {item['evaluation']['score']}"
    )
        


    conflict_report = detect_conflicts(
        question,
        ranked_evidence
)

    print("\n========== Conflict Detection ==========")
    print(conflict_report)

    confidence = score_confidence(
    ranked_evidence,
    conflict_report
)

    print("\n========== Confidence ==========")
    print(confidence)  


    reasoning_plan = build_reasoning_plan(
        question=question,
        evidence=ranked_evidence,
        conflict_result=conflict_report
    )
    print("\n========== Reasoning Plan ==========")
    print(reasoning_plan)
    
    composer_evidence = [
    item["evidence"]
    for item in ranked_evidence
]


    final_answer = compose_answer(
    question=question,
    reasoning_plan=reasoning_plan,
    ranked_evidence=composer_evidence,
    conflict_summary=conflict_report["summary"]
)
    
    
    return format_response(
    answer=final_answer,
    confidence=confidence,
    route=tools,
    ranked_evidence=ranked_evidence,
    conflict_report=conflict_report
)