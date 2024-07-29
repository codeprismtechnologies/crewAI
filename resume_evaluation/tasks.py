from crewai import Task
from textwrap import dedent


class ResumeEvaluationTasks:

    def evaluate_resume(self, agent, resume, job_role, required_skills):
        return Task(
            description=dedent(f"""
                Evaluate the resume and understand the skills and abilities of the candidate.
                Analyse the resume for relevance, correctness, and quality.
                The task involves analyzing the relevance and correctness of the resume,and then providing a score out of 10 based on these criteria.
                Check the word count, repeated words, and spelling errors in the resume.
                The score should reflect the overall quality of the resume and also the skills matchness for the desired role.
                The comment should include a brief explanation of the quality, correctness, relevance of the resume and also whether the user is a good fit for the role or not.
                Your final answer must be a detailed evaluation report on the given resume,including the relevance, correctness, and overall quality of the response.
                Respond only with the data in JSON format. 
                Use this format for the final response:
                    {{
                        "job_role":"job_role",
                        "matched_skills":"matched skills",
                        "missing_skills":"unmatched skills"
                        "comment":"Brief evaluation of the resume",
                        "score":"0-10"
                    }}
                NB: Dont generate any other responses in results.Espescially sentences like -my best complete final answer to the task or anything like ```json```- shouldnt be generated.
                    
                Job role: {job_role}
                Resume: {resume}
                Required skills: {required_skills}
            """),
            agent=agent,
            expected_output="An accurate and refined evaluation of the provided resume",
        )

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $100!"
