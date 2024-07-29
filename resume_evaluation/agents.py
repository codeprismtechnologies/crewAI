from crewai import Agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from os import environ

load_dotenv()

VERBOSE = environ["VERBOSE"]
GPT_MODEL = environ["GPT_MODEL"]

llm = ChatOpenAI(model=GPT_MODEL, temperature=0)


class ResumeEvaluatorAgents:

    def resume_evaluator_agent(self):
        return Agent(
            role="An expert resume evaluator",
            goal="Analyze a resume and provide a score based on skills relevant to the desired role",
            backstory="I can help you assess resumes by identifying skills mentioned and comparing them to the requirements of a specific role.",
            verbose=VERBOSE,
            llm=llm,
        )
