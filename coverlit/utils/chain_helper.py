from langchain.chat_models import ChatOpenAI
from langchain.prompts import  PromptTemplate
from langchain.chains import LLMChain


async def async_generate(chain, arg_dict):
    response = await chain.arun(arg_dict)
    return response


def get_chain(template, llm_model="gpt-3.5-turbo-16k", temperature=0.1):
    prompt = PromptTemplate.from_template(template)
    llm = ChatOpenAI(temperature=temperature, model=llm_model)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    return chain