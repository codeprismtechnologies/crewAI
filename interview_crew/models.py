from pydantic import BaseModel

class QuestionModel(BaseModel):
    session_id: str
    job_title: str
    total_questions: int
    skills: list
    expertise: str


class AnswerModel(BaseModel):
    session_id: str
    answer: dict
