
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
   current_question = current_question_id.get_current_question()
    if current_question is None:
        return "No question to answer."

    answer =session.strip()
    if not answer:
        return "Answer cannot be empty."
    current_question_id.answers[current_question['id']] = answer
    
    return "Answer recorded."


def get_next_question(current_question_id):
   questions = answer.questions
    for question in questions:
        if question['id'] not in current_question_id.answers:
            current_question_id.set_current_question(question)
            return question['text']

    current_question_id.set_current_question(None)
    return None


def generate_final_response(session):
   total_questions = len(answer.questions)
    correct_answers = 0

    for question in answer.questions:
        qid = question['id']
        if qid in current_question_id.answers and current_question_id.answers[qid] == question['correct_answer']:
            correct_answers += 1

    score = (correct_answers / total_questions) * 100
    return f"Quiz completed! Your score is {correct_answers}/{total_questions} ({score}%)."
