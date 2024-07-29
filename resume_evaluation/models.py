from pydantic import BaseModel

class ResumeModel(BaseModel):
    resume: str
    job_role: str
    required_skills: list