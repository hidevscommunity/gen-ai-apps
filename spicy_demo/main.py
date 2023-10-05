import streamlit as st
import openai
import json
import re
import time
from streamlit_extras.switch_page_button import switch_page
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
from llama_index import SimpleDirectoryReader
from llama_index import load_index_from_storage, StorageContext
from llama_index.indices.postprocessor import SimilarityPostprocessor
from llama_index.schema import Node, NodeWithScore
from llama_index.response_synthesizers import ResponseMode, get_response_synthesizer

#################################################################################################################################
# We customized llama_index so that it generates a memo for Spicy from a CBT guideline document, considering the user's concerns. 
# This involves 
# 1) calling a seperate agent created by me that generates a retriever query from the chat history, 
# 2) retrieving relevant information from the CBT guideline document, and
# 3) synthesizing a memo from the retrieved information.
#################################################################################################################################


OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY
storage_context = StorageContext.from_defaults(persist_dir="./data/")

index = load_index_from_storage(storage_context) 
retriever = index.as_retriever()

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 시작 시간 측정
        result = func(*args, **kwargs)  # 원래 함수 실행
        end_time = time.time()  # 종료 시간 측정
        elapsed_time = end_time - start_time  # 실행 시간 계산
        print(f"{func.__name__} 함수 실행 시간: {elapsed_time:.6f}초")
        return result
    return wrapper

# Initialize task_list
if "task_list" not in st.session_state:
    st.session_state.task_list = ""

# Initialize instructions
initial_instruction = """
Spicy, the main character, is a vibrant robot with a zest for fun, always ready with a cheeky joke or a playful roast.
ot one to let you off the hook too easily, Spicy teases with warmth and humor, turning your planning sessions into light-hearted banter. 
Prepping for tomorrow with Spicy feels like a lively chat with that friend who loves to poke fun but always has your back.
The check-in session consists of four states: 0. Beginning of the session 1. Prioritization 2. End of prioritization and start of breakdown, 3. Breakdown, and 4. Final confirmation. 
In the Prioritization part, Spicy asks the user to dump all of tomorrow's tasks in the chatbox. 
Then, Spicy helps the user prioritize the tasks by asking questions about each task. 
In the Breakdown part, Spicy asks the user to break down the prioritized tasks into smaller subtasks. 
The user can also ask Spicy to add a new task or subtask at any time.
YOU MUST provide your output in JSON compliant format with the keys: comment, task_list, and current_state.
Example: {"comment": "(Spicy and Daisy's response to the user goes here)", "task_list": "(markdown formatted task list in the order of priority goes here, blank string if no task list)", "current_state": (current state of the conversation, 0, 1, 2, or 3)}
"""
prioritize_instruction = ""
breakdown_instruction = ""
confirm_instruction = ""
instructions = [prioritize_instruction, "", breakdown_instruction, "", confirm_instruction]

# Initialize state
# state 0: prioritize 시작, state 1: prioritize 진행중, state 2: prioritize 완료 + breakdown 시작, state 3: breakdown 진행중, state 4: 확정
if "current_state" not in st.session_state:
    st.session_state.current_state = 0

# Initialize chat_history_for_model
if "chat_history_for_model" not in st.session_state:
    st.session_state.chat_history_for_model = [
        {"role": "system", "content": initial_instruction},
        {"role": "assistant", "content": 
         """{"comment": "**Spicy:**    \nAlright, champ. What's on the chaos list for tomorrow? 
         Dump all of tomorrow's tasks right here, and I'll help you prioritize them.", "task_list": ""}"""},
    ]

# Initialize chat_history_for_display
# display할 때는 1) json 형식의 content들을 parsing해서 보여줘야 하고 2) instruction이 표시되지 않게 해야 함 
if "chat_history_for_display" not in st.session_state:
    st.session_state.chat_history_for_display = [
        {"role": "assistant", "content": 
         """**Spicy:**    \nAlright, champ. What's on the chaos list for tomorrow? 
         Dump all of tomorrow's tasks right here, and I'll help you prioritize them."""},
    ]

@timer_decorator
def get_response(chat_history, previous_task_list):
    """
    지금까지의 chat history와 task list를 받아서, 새로운 chat history를 만들기 위한 구성요소와 갱신된 task list를 return하는 함수

    반환값

    raw_content: json str, chat_history_for_model에 들어감   

    comment: str, chat_history_for_display에 들어감     

    new_task_list: markdown str, st.session_state.task_list에 할당되어 화면 상단에 표시됨    

    current_state: int, st.session_state.current_state에 할당됨 
    """
    response = openai.ChatCompletion.create(
                    model= "gpt-4",
                    messages=chat_history,
                    stream=False,
                    temperature=0.5,
                    top_p = 0.93
                    )

    raw_content = response['choices'][0]['message']['content']
    raw_content.replace('\t', '    ')
    # '컨트롤 문자'를 제거
    clean_string = re.sub(r'[\x00-\x1F\x7F]', '', raw_content)
    content = json.loads(clean_string)

    # Error handling
    count = 0
    while count < 3:
        try:
            count += 1
            content = json.loads(clean_string)
            break
        except Exception as e:
            print(raw_content)
            print(e)
            content = {'comment': '**Spicy:**    \nSorry, I didn\'t get that. Could you rephrase?', 'task_list': previous_task_list}

    new_task_list = content['task_list']
    comment = content['comment']
    current_state = content['current_state']

    return raw_content, comment, new_task_list, current_state

@timer_decorator
def generate_retriever_query(chat_history_for_display):
    """
    chat_history_for_display를 받아서, retriever query를 만들어주는 함수

    반환값

    query: str
    """
    
    chat_history_for_retrieval_query = chat_history_for_display.copy()
    chat_history_for_retrieval_query.append({"role": "user", "content": "[INSTRUCTION] To address the user's concerns based on our chat history, you will refer to the CBT guideline book for adult ADHD. Provide relevant keywords or topics of interest so you can extract the most pertinent information. ONLY KEYWORDS."})

    response = openai.ChatCompletion.create(
                    model= "gpt-3.5-turbo",
                    messages=chat_history_for_retrieval_query,
                    stream=False,
                    temperature=0.5,
                    top_p = 0.93
                    )

    query = response['choices'][0]['message']['content']

    return query

@timer_decorator
def generate_relevant_info(chat_history_for_display, user_input):
    print('GENERATING QUERY...')
    try:
        query = generate_retriever_query(chat_history_for_display[-6:])
    except Exception as e:
        print(e)
        query = generate_retriever_query(chat_history_for_display[-2:])
    print(query)
    nodes = retriever.retrieve(query)
    print(nodes)
    processor = SimilarityPostprocessor(similarity_cutoff=0.75)
    filtered_nodes = processor.postprocess_nodes(nodes)
    print('SYNTHESIZING MEMO...')
    synth_start_time = time.time()
    response_synthesizer = get_response_synthesizer(response_mode=ResponseMode.COMPACT)

    i = 0
    while i < 3:
        response = response_synthesizer.synthesize(f"Provide a short, precise, straight-to-the-point and informative memo for a CBT counselor dealing with an adult ADHD patient. The patient's message was: {user_input}", nodes=filtered_nodes)
        response = response.response
        i += 1
        print(i)
        if type(response) == str:
            break
    
    if type(response) != str:
        response = ""
    synth_end_time = time.time()
    print(f"SYNTHESIZING TIME: {synth_end_time - synth_start_time:.6f}초")
    
    print("GENERATED MEMO: \n"+response)

    return response



    
st.title("SPICY: personal advisor for ADHD adults")
st.markdown("video demo: https://youtu.be/kcb5eLBIKzs")

if "saved_tasks" not in st.session_state:
    st.session_state.saved_tasks = []

if "editing" not in st.session_state:
    st.session_state.editing = False

if "change_in_task_list" not in st.session_state:
    st.session_state.change_in_task_list = False

if "hide_edit" not in st.session_state:
    st.session_state.hide_edit = True

st.markdown("""
            <style>
            [data-testid="stSidebarNav"] {
                display: none
            }
            </style>
            """, unsafe_allow_html=True)


with st.sidebar:
    st.markdown("## Tomorrow's tasks")

    # Check if there's an ongoing edit
    if st.session_state.editing:
        edited_task_list = st.text_area("Edit your task list:", st.session_state.task_list)
        if st.button("Save"):
            st.session_state.task_list = edited_task_list
            st.session_state.editing = False
            st.session_state.change_in_task_list = True

        if st.button("Cancel"):
            st.session_state.editing = False
    else:
        st.markdown(st.session_state.task_list)
        if not st.session_state.hide_edit:
            if st.button("Edit"):
                st.session_state.editing = True

        if st.button("I'm done for today. Let's move on to the next day!"):
            st.session_state.saved_tasks = st.session_state.task_list.split("\n")
            switch_page("next_day")

# Display chat history from chat_history_for_display
for message in st.session_state.chat_history_for_display:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
user_input = st.chat_input("Type here")
if user_input:
    if st.session_state.editing == True:
        st.warning("You are editing the task list. Please save or cancel your edit before proceeding.")

    else:
        # Display the user message until all the actions are done
        with st.chat_message("user"):
            st.markdown(user_input)
        
        if st.session_state.change_in_task_list:
            change_in_tasklist = "[CHANGE IN TASK LIST] The user changed the task list:\n" + st.session_state.task_list + "\n"
            st.session_state.change_in_task_list = False
        else:
            change_in_tasklist = ""

        if st.session_state.current_state == 3:
            # Generate a memo from the chat history
            memo = "[GUIDANCE MEMO]\n"
            memo = memo + generate_relevant_info(st.session_state.chat_history_for_display, user_input)
            # Append the memo to chat_history_for_model
            st.session_state.chat_history_for_model.append({"role": "user", "content": user_input + "\n" + memo + change_in_tasklist + instructions[st.session_state.current_state]})
            # Append the memo to chat_history_for_display
            st.session_state.chat_history_for_display.append({"role": "user", "content": user_input})
        
        else:
            st.session_state.chat_history_for_model.append({"role": "user", "content": user_input + "\n" + change_in_tasklist + instructions[st.session_state.current_state]})
            st.session_state.chat_history_for_display.append({"role": "user", "content": user_input})

        # Get the model response
        st.session_state.hide_edit = True
        with st.chat_message("assistant"):
            st.markdown("*Spicy is thinking...*")
            raw_content, comment, new_task_list, current_state  = get_response(st.session_state.chat_history_for_model, st.session_state.task_list)
            print("\nraw_content: "+ raw_content)
            print("\nnew_task_list: "+ new_task_list)
            print("\ncurrent_state: "+ str(current_state))
            st.markdown(comment)
        
        # Append unparsed model output to chat_history_for_model
        st.session_state.chat_history_for_model.append({"role": "system", "content": raw_content})
        # Append parsed model output to chat_history_for_display
        st.session_state.chat_history_for_display.append({"role": "assistant", "content": comment})
        st.session_state.task_list = new_task_list
        st.session_state.current_state = current_state

        st.session_state.hide_edit = False

        st.experimental_rerun()
