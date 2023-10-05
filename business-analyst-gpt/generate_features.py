from langchain.chat_models import ChatOpenAI
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'))


def generate_features_list(features):
    system_message = """Given a list of features, generate an updated feature list with expanded features which \
includes all the features that are prerequisites, dependencies, or interlinks of the given features."""

    human_message = """Features:
{features}
"""

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_message)

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            human_message_prompt
        ]
    )

    chat_model = ChatOpenAI(temperature=0.6, model="gpt-3.5-turbo")

    llm_chain = LLMChain(prompt=chat_prompt, llm=chat_model, verbose=True)
    response = llm_chain.run(
        features=features
    )

    print(response)

    return response


def generate_features_description(problem, features):
    system_message = """Elaborate on the given FEATURES and sub-features for a URD related to the given problem. Write prerequisites and descriptions, for \
each feature and sub-feature. Make sure you cover all the FEATURES """

    human_message = """Problem: {problem}

% START OF FEATURES 
{features}
% END OF FEATURES

Here is an example output format:

1. Feature 1:
    Pre-requisites: ...
    Description: ...

1.1 Sub-feature 1
    Pre-requisites: ...
    Description: ...
1.2 Sub-feature 2
    Pre-requisites: ...
    Description: ...
1.3 Sub-feature 3
        Pre-requisites: ...
    Description: ...
"""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_message)

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            human_message_prompt
        ]
    )

    chat_model = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo")

    llm_chain = LLMChain(prompt=chat_prompt, llm=chat_model, verbose=True)
    response = llm_chain.run(
        problem=problem,
        features=features
    )

    print(response)

    return response
