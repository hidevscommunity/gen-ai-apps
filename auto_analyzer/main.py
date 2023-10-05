import os
import json

import pandas as pd
import streamlit as st

from langchain import LLMChain
from langchain.llms import OpenAIChat
from langchain.utilities import SQLDatabase
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain_experimental.sql import SQLDatabaseChain


def generate_question_list(header, description):
    """
    header:
        str
    description:
        str
    return:
        dict([str])
    """

    _question_template = """
    You are a data analyst.You will now receives a JSON object below.
    This indicates the table name and its column names.
    Return questions about this data according to the following conditions, data dascription and onditions

    Header:
    {header}

    Data description:
    {description}

    Conditions:
    - Consider multiple questions to get a complete picture of the data.
    - First, think of the questions as bullet points, then format them according to the output format.
    - One question per bullet point.

    Response example:
    {{ "question: [your question 1, your question 2, ...]"}}

    """
    llm4 = OpenAIChat(temperature=0, verbose=True, model='gpt-4')
    question_chain = LLMChain(llm=llm4, prompt=PromptTemplate.from_template(
        _question_template), verbose=True)
    questions = question_chain.predict(
        header=header, description=description)
    questions_dict = json.loads(questions)

    return questions_dict


def create_answer_and_sql(question):
    """
    question:
        str
    return:
        dict(str, str)
    """

    # ouput parser
    response_schemas = [
        ResponseSchema(
            name="answer", description="Answers to user questions. "),
        ResponseSchema(
            name="query", description="The query executed in response to a user's question. Must be SQL.")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(
        response_schemas)
    format_instructions = output_parser.get_format_instructions()

    # customize SQLDabaseChain prompt
    _sql_template = """
    Given an input question, first create a syntactically correct {dialect} query to run,
    then look at the results of the query, and return the executed query and answer according to the following format instructions.

    Use the following format:

    Question: "Question here"
    SQLQuery: "SQL Query to run"
    SQLResult: "Result of the SQLQuery"
    Answer: "Final answer here"

    format instructions: {format_instructions}

    Only use the following tables:

    {table_info}

    Question: {input}"""

    sql_prompt = PromptTemplate(
        template=_sql_template,
        input_variables=["input", "table_info", "dialect"],
        partial_variables={"format_instructions": format_instructions}
    )
    llm16kmodel = OpenAIChat(temperature=0, verbose=True,
                             model='gpt-3.5-turbo-16k-0613')

    # load data
    db = SQLDatabase.from_uri("sqlite:///data.db")
    db_chain = SQLDatabaseChain.from_llm(
        llm16kmodel, db, prompt=sql_prompt, verbose=True)

    # generae answer(answer and sql)
    answer_and_sql = db_chain.run(question)
    answer_and_sql_dict = output_parser.parse(answer_and_sql)

    return answer_and_sql_dict


def generate_consideration(analysis, description):
    """
    analysis:
        str
    description:
        str
    return:
        str
    """

    _consideration_template = """
    You are a data analyst.You will now receives a JSON object below.
    This JSON contains the results of data analysis.
    Summarize the results and output a discussion according to the following conditions.

    JSON:
    {analysis}

    Data description:
    {description}

    Conditions:
    - Considerations should be in the form of markdown bullet points
    - One consideration per one bullet point.

    Response example:
    - Considerations1
    - Considerations2
    - Considerations3
    """
    llm16kmodel = OpenAIChat(temperature=0, verbose=True,
                             model='gpt-3.5-turbo-16k-0613')
    consideration_chain = LLMChain(llm=llm16kmodel, prompt=PromptTemplate.from_template(
        _consideration_template), verbose=True)
    consideration = consideration_chain.predict(
        analysis=analysis, description=description)

    return consideration


st.title('CSV auto analyser')
user_api_key = st.sidebar.text_input(
    label="OpenAI API key",
    placeholder="Paste your OpenAI API key here",
    type="password")
os.environ['OPENAI_API_KEY'] = user_api_key

st.subheader('I read CSV and analyze it automatically')
uploaded_file = st.file_uploader('Choose a file', type='csv')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write('data header')
    st.table(df.head(1))
    df.to_sql('data', 'sqlite:///data.db', if_exists='replace')

description = st.text_input('Input data description')

if st.button('Start analysis') and user_api_key is not None and uploaded_file is not None:
    with st.spinner('Thinking of questions....'):
        header = json.dumps(df.head(1).to_json())
        analysis_questions = generate_question_list(header, description)

    questions_and_answers = []

    for question in analysis_questions['question']:
        with st.spinner("Analyzing..."):
            q_and_a = {}
            try:
                answer_and_sql = create_answer_and_sql(question)
            except:
                st.write('SQL execution failed.')
                continue
            q_and_a["question"] = question
            q_and_a["answer"] = answer_and_sql['answer']
            questions_and_answers.append(q_and_a)
            df_answer = pd.read_sql(
                answer_and_sql['query'], 'sqlite:///data.db')
            st.subheader(question)
            st.table(df_answer)
            st.write(answer_and_sql['answer'])

    with st.spinner("The results of the analysis are summarized..."):
        result = {}
        result["questions_and_answers"] = questions_and_answers
        analysis_result = json.dumps(result)

        consideration = generate_consideration(analysis_result, description)
        st.markdown("## Summary")
        st.markdown(consideration)
