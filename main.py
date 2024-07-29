import os
import time
import json
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from interview_crew.crew import InterviewCrew
from interview_crew.models import QuestionModel, AnswerModel
from resume_evaluation.crew import ResumeEvaluationCrew
from resume_evaluation.models import ResumeModel
from utils.logging_details import logging_details

# os.environ["OTEL_SDK_DISABLED"] = "true"

questions_dict = {}
submission_history = {}

app = FastAPI(docs_url="/ai/docs", openapi_url="/ai/openapi.json")

router = APIRouter(prefix="/ai")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

expertise_mapping = {
    "BEGINNER": "Slightly Moderate",
    "INTERMEDIATE": "Medium",
    "EXPERIENCED": "Hard"
}

@router.post("/generate-questions")
def generate_question(item: QuestionModel):
    try:
        session_id = item.session_id
        logging_details("Start of generate_question API", "INFO", session_id)
        logging_details(f"Request payload: {item}", "INFO", session_id)
        start = time.time()
        job_title = item.job_title
        total_questions = item.total_questions
        skills = item.skills
        level = item.expertise
        expertise = expertise_mapping[level]

        if session_id in submission_history:
            last_submission = submission_history[session_id]
        else:
            last_submission = []
            submission_history[session_id] = last_submission

        if session_id in questions_dict:
            questions_asked = questions_dict[session_id]
        else:
            questions_asked = []
            questions_dict[session_id] = questions_asked
        
        logging_details(f"Questions asked: {questions_asked}", "INFO", session_id)
        logging_details(f"Last submission: {last_submission}", "INFO", session_id)
        interview_crew = InterviewCrew(job_title, skills, total_questions, expertise)
        result = interview_crew.ask_question(questions_asked, last_submission)
        
        question = result["question"]
        if "code" in result and result["code"]:
            question += "\n" + result["code"]
        
        questions_asked.append(question)
        if len(last_submission) >= 2:
            last_submission = []
        
        last_submission.append({"role":"system", "content":question})
        submission_history[session_id] = last_submission

        
        logging_details(f'Result: {result}', "INFO", session_id)
        end = time.time()
        logging_details(f"Time consumed: {end-start}", "INFO", session_id)
        return result
    except Exception as e:
        logging_details(e, "ERROR", session_id)
        return {"status_code": 500, "error": "Integration error"}

@router.post("/evaluate-answers")
def evaluate_answer(item: AnswerModel):
    try:
        session_id = item.session_id
        logging_details("Start of evaluate_answer API", "INFO", session_id)
        logging_details(f'Request payload: {item}', "INFO", session_id)
        start = time.time()
        logging_details(f"session id: {session_id}", "INFO", session_id)
        question = item.answer.get("question", "")
        code = item.answer.get("code", "")
        answer = item.answer.get("answer", "")
        if session_id in submission_history:
            messages = submission_history[session_id]
        else:
            submission_history[session_id] = []
            messages = submission_history[session_id]
        interview_crew = InterviewCrew()
        result = interview_crew.evaluate_answer(question, code, answer)
        messages.append({"role": "user", "content": answer})
        logging_details(f'Chat history: {messages}', "INFO", session_id)
        logging_details(f'Result: {result}', "INFO", session_id)
        end = time.time()
        logging_details(f"Time consumed: {end-start}", "INFO", session_id)
        return result
    except Exception as e:
        logging_details(str(e), "ERROR", session_id)
        return {"status_code": 500, "error": "Integration error"}

@router.post("/evaluate-resume")
def evaluate_resume(item: ResumeModel):
    try:
        resume_evaluation_crew = ResumeEvaluationCrew(item)
        result = resume_evaluation_crew.evaluate_resume()
        logging_details("Resume evaluation result", "INFO", "resume_evaluation")
        logging_details(f'Result: {result}', "INFO", "resume_evaluation")
        logging_details(result, "INFO", "resume_evaluation")
        return json.loads(result)
    except Exception as e:
        logging_details(str(e), "ERROR", "resume_evaluation")
        return {"status_code": 500, "error": "Integration error"}

app.include_router(router)