from crewai import Task
from textwrap import dedent


class InterviewTasks:
    def ask_question(self, agent, job_title, skills, question_types, total_questions, expertise, questions_asked, last_submission):
        return Task(
            description=dedent(f"""
                Analyze the job role and generate a single potential interview question based on the instructions below.
                
                1. Job Role: Generate a question for the {job_title} role with {expertise} expertise.
                2. Relevance: Ensure the question is relevant to the role and the provided skills: {skills}.
                3. Question Types: The question should be of {question_types} type. Ensure that each type is represented equally within {total_questions} questions.
                4. Difficulty:
                   - Start with an uncommon, moderately difficult question.
                   - Adjust the difficulty based on the last answer:
                     - If the previous answer was correct or well-structured, increase difficulty of the question.
                     - If the previous answer was incorrect or poorly structured, decrease difficulty of the question.
                5. Unique Questions:
                   - Never repeat questions already asked. Refer {questions_asked} completely to check if a question is already asked.
                   - Avoid theoretical questions.
                   - Ensure questions are different for skills in different categories like programming languages, frameworks, databases, libraries, etc.
                   - Avoid questions which are part of or related to the questions already asked.
                6. Coding Questions:
                   - For CODING type questions:
                     - If the skill is a programming language, provide a tricky and competitive coding question (e.g., questions similar to {expertise} problems as in LeetCode or HackerRank).
                     - If the skill is other than a programming language (e.g., framework, library, database, or others), provide an application-level programming question relevant to the skill.
                   - For ERROR_FIXING and CODE_OPTIMISATION types, include the relevant code snippet or DB query in the "code" field, do not add in "question".
                   - Ensure the generated code in question for ERROR_FIXING contains errors.
                7. Format: Respond strictly in JSON format:
                   {{
                       "question": "question",
                       "code": "Code if any",
                       "type": "type in uppercase",
                       "skill": "skill as same in {skills}",
                       "time": "required time in minutes"
                   }}
                8. Timing: Allocate a minimum of 2 minutes per question.
                9. Note: Never generate any text other than responses in the results. Especially, do not include sentences like "my best complete final answer to the task" or anything similar. Do not include backticks (`) anywhere in the response.

                Job Title: {job_title}
                Skills: {skills}
                Expertise Level: {expertise}
                Question Types: {question_types}
                Last Submission: {last_submission}
                Questions Asked: {questions_asked}
            """),
            agent=agent,
            expected_output='A refined finalized version of relevant interview question'
        )
    

    def evaluate_answer(self, agent, question, answer):
        return Task(
            description=dedent(f"""
                Evaluate and review the answer given for the specific question.
                The task involves analyzing the relevance and correctness of the answer, and then providing a score out of 10 based on these criteria.
                Your final answer must be a detailed evaluation report on the given answer, including the relevance, correctness, and overall quality of the response.
                Provide a score of 0 if no answer is provided or if the answer is irrelevant to the question.
                Strictly respond only with the data in JSON format, not in markdown format. 
                Use this format for the final response:
                    {{
                        "comment":"Evaluation comments",
                        "score":"0-10"
                    }}
                NB: Dont generate any other responses in results.Espescially sentences like -my best complete final answer to the task or anything like ```json```- shouldnt be generated.
                Never include backticks (`) anywhere in the response.
                In 'comment' field,a detailed evaluation report is needed, not the corrected answer or corrected code. So return the detailed evaluation report only in 'comment' field.
                And in 'comment', the evaluation report should be in normal text format in single line. Never generate it in markdown format.
                {self.__tip_section()}

                Question: {question}
                Answer to be evaluated: {answer}
            """),
            agent=agent,
            expected_output='A refined evaluation of the given answer'
        )

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $100!"