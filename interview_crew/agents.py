from langtrace_python_sdk import langtrace
from crewai import Agent
from langtrace_python_sdk import langtrace
from langchain_community.llms.ollama import Ollama
from dotenv import load_dotenv
import os

load_dotenv()

LANGTRACE_API_KEY = os.environ["LANGTRACE_API_KEY"]
VERBOSE = os.environ["VERBOSE"]
LLAMA_MODEL = os.environ["LLAMA_MODEL"]
BASE_URL = os.environ["BASE_URL"]

langtrace.init(api_key=LANGTRACE_API_KEY)
llm = Ollama(model=LLAMA_MODEL, base_url=BASE_URL)



class InterviewAgents:

    def question_asking_agent(self):
        return Agent(
            role="Interview Question Expert",
            goal="Create effective interview questions to assess interviewee's knowledge, skills, and suitability for the role.",
            backstory="An experienced professional skilled in crafting questions to evaluate candidates across various skills, roles and industries.",
            verbose=VERBOSE,
            llm=llm,
        )
    
    def answer_evaluating_agent(self):
        return Agent(
            role="Answer Evaluation Expert",
            goal="Evalute answer for given question to get best insight about interviewee",
            backstory="An expert in evaluating answers for interview questions.",
            verbose=VERBOSE,
            llm=llm,
        )