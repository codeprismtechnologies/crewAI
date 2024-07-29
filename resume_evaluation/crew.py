import re
import io
import requests
from os import environ
from crewai import Crew
# from PyPDF2 import PdfReader
from pypdf import PdfReader
from dotenv import load_dotenv

from .tasks import ResumeEvaluationTasks
from .agents import ResumeEvaluatorAgents

load_dotenv()

VERBOSE = environ["VERBOSE"]


class ResumeEvaluationCrew:

    def __init__(self, item):
        self.resume_url = item.resume
        self.job_role = item.job_role
        self.required_skills = item.required_skills
    
    def extract_file_id(self, drive_url):
        match = re.search(r'/d/([a-zA-Z0-9_-]+)', drive_url)
        if match:
            return match.group(1)
        else:
            raise ValueError("Invalid Google Drive URL")

    def pdf_to_text(self):
        url = self.resume_url

        file_id = self.extract_file_id(url)
        download_url = f'https://drive.google.com/uc?id={file_id}'
        response = requests.get(download_url)
        text = ""
        if response.status_code == 200:
            pdf_content = io.BytesIO(response.content)
            pdf_reader = PdfReader(pdf_content)
            
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    def evaluate_resume(self):
        agents = ResumeEvaluatorAgents()
        tasks = ResumeEvaluationTasks()
        resume = self.pdf_to_text()

        resume_evaluator_agent = agents.resume_evaluator_agent()
        resume_evaluation_task = tasks.evaluate_resume(
            resume_evaluator_agent, resume, self.job_role, self.required_skills
        )

        crew = Crew(
            agents=[resume_evaluator_agent],
            tasks=[resume_evaluation_task],
            verbose=VERBOSE,
        )

        result = crew.kickoff()
        return result
