from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'))


def generate_user_requirement_document(answers):
    system_message = """Given the information by the user, generate a User Requirement Document (URD). The URD should \
have a clear problem statement, goals, objectives to accomplish, features, and a conclusion paragraph. Reproduce the \
features part as it is in the response

Generate the features response in the following format:
Feature Name:
Feature Prerequisites:
Feature Description:

Sub-feature Name:
Sub-feature Prerequisites:
Sub-feature Description:

# Generate the response document in the markdown format 

Must generate the title with the topic name
"""

    human_message = """
Problem: {answer1}
Platform: {platform}
Goal: {answer2}
Features: {answer3}
Users: {answer4}
"""

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_message)

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            human_message_prompt
        ]
    )

    chat_model = ChatOpenAI(temperature=0.6, model="gpt-3.5-turbo-16k")

    llm_chain = LLMChain(prompt=chat_prompt, llm=chat_model, verbose=True)
    response = llm_chain.run(
        answer1=answers["answer1"],
        platform=answers["platform"],
        answer2=answers["answer2"],
        answer3=answers["answer3"],
        answer4=answers["answer4"],
    )

    return response
