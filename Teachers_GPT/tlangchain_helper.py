from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import streamlit as st
import os
#from keyfile import openai_key
#OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
llm = OpenAI(temperature=0.0)
#llm = OpenAI(temperature=0.0)

def generate_curriculum(level):
    # Chain 1: Level of Curriculum
    prompt_template_curriculum = PromptTemplate(
        input_variables=['level'],
        template="Generate a curriculum outline for grade {level} in US standard elementary schools."
    )
    name_chain = LLMChain(llm=llm, prompt=prompt_template_curriculum, output_key="level_name")
    response = name_chain({'level': level})
    return response


if __name__ == "__main__":
    
    print(generate_curriculum("one"))  # Change "first" to the desired grade level
