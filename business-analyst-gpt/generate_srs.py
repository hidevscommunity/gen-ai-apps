from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'))


def generate_software_requirement_specification_document(urd_content):
    system_message = """Generate a Software Requirements Specification (SRS) document based on the provided User \
Requirements Document (URD). Assume the role of an expert project manager and create a comprehensive SRS document that \
clearly identifies each aspect. Additionally, outline the features, functional requirements, and non-functional \
requirements in detail. You are responsible for choosing the technology stack and technical details not provided by \
the user.

Generate the response in the markdown format

Must generate the title with the topic name
"""

    human_message = """URD:
{urd}
"""

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_message)

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            human_message_prompt
        ]
    )

    chat_model = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo-16k")

    llm_chain = LLMChain(prompt=chat_prompt, llm=chat_model, verbose=True)
    response = llm_chain.run(urd=urd_content)

    return response
