def update_memory(
    question,
    result,
    session_state
):
    session_state.last_question = question
    session_state.last_result = result