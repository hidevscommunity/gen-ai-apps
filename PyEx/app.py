import streamlit as st
from question import *
from exercise import *
from feedback import *
import logging
from langchain import callbacks
from streamlit_ace import st_ace
from similarity_check import *
from langchain.output_parsers import PydanticOutputParser
from langchain.chains import LLMChain
from langchain.llms.base import BaseLLM
from typing import Tuple, Dict


logging.basicConfig(level=logging.INFO)

os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

st.set_page_config(page_title="Coding Room",
                   page_icon="📚",
                   layout="wide",
                   initial_sidebar_state="auto",
                   menu_items=None)


@st.cache_data(ttl=3000, show_spinner="Generating exercise ...")
def get_exercise(language: str,
                 _exercise_parser: PydanticOutputParser,
                 _exercise_llm_chain: LLMChain,
                 _llm: BaseLLM) -> Tuple[Dict, str]:

    exercise_generate_prompt = f"Generate a {language} coding exercise according to above format. The problem statement content MUST contain the `{context}` keywords."
    exercise_generate_metadata = {
                                    "metadata": {
                                        "type": "exercise_generator"
                                    }
                                 }

    with callbacks.collect_runs() as cb:
        exercise_generate_response = _exercise_llm_chain.invoke({"question": exercise_generate_prompt}, exercise_generate_metadata)
        exercise_chain_run_id = cb.traced_runs[-1].id
        logging.info(exercise_chain_run_id)

    logging.info(exercise_generate_response)
    if 'text' in exercise_generate_response:
        exercise_dict = parse_response(exercise_generate_response['text'], _exercise_parser, _llm, exercise_generate_prompt)
    else:
        exercise_dict = parse_response(exercise_generate_response, _exercise_parser, _llm, exercise_generate_prompt)

    return exercise_dict, exercise_chain_run_id

@st.cache_data(ttl=3000, show_spinner="Please hang tight ...")
def get_explanation(exercise_dict: Dict, _llm: BaseLLM) -> Tuple[str, str]:
    explanation_prompt = create_code_explanation_prompt(generated_question=exercise_dict['problem_statement'],
                                                        code=exercise_dict['solution'])
    explanation_llm_chain = get_llm_chain(llm=_llm,
                                          template=explanation_prompt,
                                          parser=None,
                                          tag=os.getenv('ENV_TAG', 'test-run'))
    explanation_generate_prompt = f"Generate explanation for the above code"
    explanation_generate_metadata = {
                                        "metadata": {
                                            "type": "explanation_generator"
                                        }
                                    }

    with callbacks.collect_runs() as cb:
        explanation_response = explanation_llm_chain.invoke({"question": explanation_generate_prompt}, explanation_generate_metadata)
        explanation_chain_run_id = cb.traced_runs[-1].id
        logging.info(explanation_chain_run_id)
    logging.info(explanation_response)
    return explanation_response, explanation_chain_run_id


st.title("🤖 PyEx")
st.info("AI-powered exercise generation that accelerates your programming journey! 🚀")

st.sidebar.image(image=f"{os.getcwd()}/logo.png",
                 use_column_width=True,
                 width=20)
st.sidebar.header("Programming Exercise Generator")

language = st.sidebar.selectbox(label="Programming Language",
                                options=['Python'])

difficulty = st.sidebar.selectbox(label="Difficulty",
                                  options=['Easy', 'Medium', 'Hard'])

topic = st.sidebar.selectbox(label="Programming Topic",
                             options=['Array', 'String', 'Math', 'Dyanamic Programming', 'Binary Search'])

context = ""
# context = st.sidebar.text_input(label="New Question Keyword Context",
#                                 help="The context under which the question will be formed.",
#                                 placeholder="Context can be anything, e.g. cars/balloons/trains")

num_ref_exercises = st.sidebar.slider(label="No. Reference Exercises",
                                      help="Number of similar topic exercises that you can refer to",
                                      min_value=2,
                                      max_value=5,
                                      value=3,
                                      step=1)

temperature = st.sidebar.slider(label="LLM temperature",
                                help="Lower temperature yields focused and deterministic responses, while higher temperature introduces more randomness and diversity in responses",
                                min_value=0.5,
                                max_value=0.99,
                                value=0.8,
                                step=0.01)

gpt_model = st.sidebar.selectbox(label="GPT model",
                                 options=['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo-16k-0613'])

generate_btn = st.sidebar.button(label="Generate")
llm = get_llm(model=gpt_model,
              temperature=temperature,
              tag=os.getenv("ENV_TAG", "test-run"))

st.sidebar.warning("*❗ Do regenerate as LLM response is flaky*")
st.sidebar.markdown(f"""
***
```
🔥 Copyright 🔥
©author={{Dev317,giaphuongphan}}
year={{2023}}
```
""",
unsafe_allow_html=True)


if generate_btn or "feedback_state" in st.session_state:

    if generate_btn:
        st.cache_data.clear()

    try:
        dataset_path = generate_sample_question(language=language.lower(),
                                                difficulty=difficulty,
                                                topic=topic)
        sample_questions = select_random_n_questions(dataset_path=dataset_path,
                                                     n=num_ref_exercises)
        prompt = create_exercise_prompt(language=language.lower(),
                                        sample_questions=sample_questions,
                                        topic=topic + "\n" + context)
        exercise_parser = get_parser(Exercise)
        exercise_llm_chain = get_llm_chain(llm=llm,
                                           template=prompt,
                                           parser=exercise_parser,
                                           tag=os.getenv('ENV_TAG', 'test-run'))
        exercise_dict, exercise_chain_run_id = get_exercise(language=language.lower(),
                                                            _exercise_parser=exercise_parser,
                                                            _exercise_llm_chain=exercise_llm_chain,
                                                            _llm=llm)

        if exercise_dict:
            explanation_response, explanation_chain_run_id = get_explanation(exercise_dict=exercise_dict,
                                                                             _llm=llm)

        st.subheader(body="AI-generated Programming Exercise",
                    divider="rainbow")

        with st.expander(label=exercise_dict['title'],
                         expanded=True):
            problem_statement_tab, explanation_tab, feedback_tab = st.tabs(['❓ Problem Statement', '💡 Code Hint Explanation', '❤️ Feedback'])
            with problem_statement_tab:
                st.markdown(body=exercise_dict['problem_statement'])
                st.markdown(f"*Topic: {exercise_dict['topic']}*")

                st.subheader(body="Try out now!",
                             divider="grey")

                function_def = exercise_dict['solution'].split("\n")[0]
                code_snippet = st_ace(theme="clouds_midnight",
                                      language="python",
                                      wrap=True,
                                      value=function_def)

                st.warning("❗ Remember to 'Apply' to save your code and check your syntax. Failing to 'Apply' will cause the similarity checker to fail to process")

                try:
                    if st.button(label="Similarity check"):
                        percentage_sim = similarity_check(ref_code=exercise_dict['solution'],
                                                          actual_code=code_snippet)
                        st.info(f"Similarity with hinted solution: {percentage_sim * 100}%")
                except Exception as ex:
                    st.toast(f"Error: {str(ex)} ", icon="❗")

            with explanation_tab:
                st.code(body=exercise_dict['solution'], language="markdown")
                st.markdown(body=explanation_response['text'])

            with feedback_tab:
                st.session_state['feedback_state'] = True
                exercise_comment = st.text_input(label="Comments on the exercise generation")
                exercise_accuracy_score = st.slider(label="Accuracy score on the exercise",
                                min_value=0.0,
                                max_value=1.0,
                                step=0.1,
                                value=0.5,
                                help="0.0 is the least accurate and 1.0 is the most accurate")
                exercise_correction = st.text_input(label="Additional correction on the exercise generation")
                explanation_comment = st.text_input(label="Comments on the code explanation")
                explanation_accuracy_score = st.slider(label="Accuracy score on the explanation",
                                min_value=0.0,
                                max_value=1.0,
                                step=0.1,
                                value=0.5,
                                help="0.0 is the least accurate and 1.0 is the most accurate")
                explanation_correction = st.text_input(label="Additional correction on the explanation response")

                if st.button(label="Submit"):
                    if os.environ['ENV_TAG'] == "test-run":
                        send_comment(run_id=exercise_chain_run_id,
                                    comment=exercise_comment,
                                    score=exercise_accuracy_score,
                                    correction={"additional_correction": exercise_correction})

                        send_comment(run_id=explanation_chain_run_id,
                                    comment=explanation_comment,
                                    score=explanation_accuracy_score,
                                    correction={"additional_correction": explanation_correction})

                    st.toast(body="Thank you for your input!", icon="✅")

    except Exception as ex:
        logging.info(str(ex))
        st.toast(body="Please try again", icon="🚨")
