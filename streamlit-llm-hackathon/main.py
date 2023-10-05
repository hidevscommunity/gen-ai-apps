from langchain import HuggingFaceHub
import streamlit as st
from langchain import PromptTemplate, LLMChain
import os

os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.secrets['key']

#

def response(question):


    template = """Question: {question}

    Answer: Let's Think"""

    prompt = PromptTemplate(template=template, input_variables=["question"])

    repo_id = "google/flan-t5-xxl"  # See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options
    # repo_id = "gpt2"  # See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options

    llm = HuggingFaceHub(
        repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 200}
    )
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    return llm_chain.run(question)


st.title("LLM Hackathon Challenge")
st.write("Your Anyday Assistant :)")

q = st.text_input("Do you have any question? Just throw it to me.")

if st.button("Generate answer"):
    st.write(f'Answer : :green[{response(q).capitalize()}]')

st.write("Example Questions:")
st.write("1. Who is Joe Biden?")
st.write("2. Where India is located on map?")