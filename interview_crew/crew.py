import json
import os
from crewai import Crew
from dotenv import load_dotenv

from .agents import InterviewAgents
from .tasks import InterviewTasks

load_dotenv()

VERBOSE = os.environ["VERBOSE"]

class InterviewCrew:

    def __init__(self, job_title=None, skills=None, total_questions=None, expertise=None):
        self.job_title = job_title
        self.skills = skills
        self.total_questions = total_questions
        self.expertise = expertise
        self.question_types = "CODING, ERROR_FIXING, CODE_OPTMISATION"
    
    def ask_question(self, questions_asked, last_submission):
        agents = InterviewAgents()
        tasks = InterviewTasks()

        question_asking_agent = agents.question_asking_agent()
        ask_question_task = tasks.ask_question(
            question_asking_agent,
            self.job_title,
            self.skills,
            self.question_types,
            self.total_questions,
            self.expertise,
            questions_asked,
            last_submission
        )

        crew = Crew(
            agents=[question_asking_agent],
            tasks=[ask_question_task],
        )
        result = crew.kickoff()
        # result = str(crew_output)
        """
        Removes unnecessary literals & characters
        and updates the results into json format
        """
        print('\nquestion generation result:\n---------------\n', result)
        if not result.startswith('{'):
            idx = result.find('{')
            if idx != -1:
                result = result[idx:]
        print('\nUpdated generated question result:\n---------------\n', result)
        return json.loads(result)
    
    def evaluate_answer(self, question,code, answer):
        agents = InterviewAgents()
        tasks = InterviewTasks()
        answer_evaluation_agent = agents.answer_evaluating_agent()
        """
        Add code into question if any
        (for the questions of type ERROR_FIXING,CODE_OPTIMISATION)
        to evaluate the answer
        """
        if code:
            question += '\n' + code
        evaluation_task = tasks.evaluate_answer(
            answer_evaluation_agent,
            question,
            answer
        )

        crew = Crew(
            agents=[answer_evaluation_agent],
            tasks=[evaluation_task],
            verbose=VERBOSE
        )
        result = crew.kickoff()
        # result = str(crew_output)
        """
        Removes unnecessary literals & characters 
        and updates the results into json format
        """
        print('evaluation result:\n---------------\n', result)
        if not result.startswith('{'):
            idx = result.find('{')
            if idx != -1:
                result = result[idx:]

        result = json.loads(result)
        return_res = {}
        return_res['question'] = question
        return_res['answer'] = answer
        for key, value in result.items():
            return_res[key] = value

        return return_res