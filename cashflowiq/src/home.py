import streamlit as st
import pandas as pd 
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from collections import Counter
import os
import random

from langchain.agents import initialize_agent, AgentType, Tool, create_csv_agent
from langchain.memory import ConversationBufferMemory
from langchain.schema.output_parser import OutputParserException

st.set_page_config(page_title="CashFlowIQ 💰✨", page_icon="✨")

NEW_CHAT_START = [{"role": "assistant", "content": "Upload your transactions file to the left and I'll get started!"}]
BUDGET_PROMPT = """
You're a friendly and talkative chatbot who is an expert at helping whoever talks to you analyze their spending habits. 
You're very accomodating to requests and want to help whoever talks to you save money while still enjoying their lifestyle. 
The person you're talking to can't see your thoughts so be sure to include any important or pertinent information within your thoughts in your final answer.
"""
NEW_BUDGET = Counter({"total_tokens": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_cost": 0
    })

LOADING_THOUGHTS = [
    "Calculating... CashFlowIQ is figuring out how to turn pennies into dollars 💰✨",
    "Hold onto your wallet... CashFlowIQ is counting virtual piggy bank coins 🐖🏦",
    "Loading... CashFlowIQ is learning to do the financial fandango 💃💸",
    "Just a moment... CashFlowIQ is auditing its virtual cookie jar 🍪💼",
    "Cha-ching! CashFlowIQ is deciphering the secret language of dollar bills 💵🔍",
    "Wait for it... CashFlowIQ is deciding between stocks and memes 📈🚀",
    "One sec... CashFlowIQ is negotiating with virtual financial gurus 🕊️💼",
    "Loading... CashFlowIQ is exploring the digital treasure map 🗺️💰",
    "Counting... CashFlowIQ is practicing its money magic tricks 🎩✨",
    "Hang in there... CashFlowIQ is budgeting for intergalactic vacations 🌌✈️"
]

GRAPH_PREFIX = """GRAPH: ~{}~ Respond with a single line of python code that draws a streamlit chart. 
The pandas dataframe object you need to use is called 'pd.read_csv(uploaded)'. 
do not explain your response or ask about follow up questions. 
the streamlit library is already imported and available as 'st'. 
pandas library is already imported and available as 'pd'. 
return only valid, executable python code that starts with the characters 'st.'. 
Do not surround the line by any single-quotes, double-quotes, or backticks. 
For example, here are several a working lines that your response should always similar to: 
`st.bar_chart(pd.read_csv(uploaded), x=\"Date\", y=\"Amount\")`
`st.line_chart(pd.read_csv(uploaded), x=\"Date\", y=\"Amount\")`
"""

INITIAL_PROMPTS = [
        # "Make a good line chart using the data uploaded. Use the Graphing Tool. the input should be related to date and the other an amount. Return only those two columns as a single string, separated by commas like 'Date,Balance'. don't provide any other information."
        GRAPH_PREFIX.format("Create a line chart showing my daily transaction amount."),
        # "Describe the data in the file I just uploaded?",
        # "How many records are in the file I uploaded?",
        "What are my top 5 expense categories?",
        # "What are my most common vendor transactions?",
        # "How has my spending in groceries changed over the year?",
        # "Are there any unusual or suspicious transactions in my accounts?",
        # "What are the columns in the file i uploaded?",
        # "Use the pandas df.describe() function on the dataframe and provide your thoughts and analysis in your final answer.",
        # "What's the total amount of money spent in the file i uploaded?",
        "How much money is spent in a typical month?"
    ]

def parsing_columns(string):
    a, b = string.split(",")
    return f"st.line_chart(pd.read_csv(uploaded), x={a}, y={b})"


def get_random_thought():
    return LOADING_THOUGHTS[random.randint(0, len(LOADING_THOUGHTS)-1)]

def new_chat():
    st.session_state["messages"] = NEW_CHAT_START

def add_assistant_response(response, cb=None):
    if cb:
        st.session_state["token_usage"] += parse_cb(cb)
    try:
        if 'st.' in response:
            if not response.startswith('st.'):
                response = response.strip("'").strip('`').strip('"')
            msg = {"role": "assistant", "content": response}
            st.session_state.messages.append(msg)
            eval(response) 
        else:
            msg = {"role": "assistant", "content": response}
            st.session_state.messages.append(msg)
            st.chat_message("assistant").write(msg["content"])
    except OutputParserException as e:
        st.chat_message("assistant").write(e)
    except Exception as e:
        st.chat_message("assistant").write("Hmm, something went wrong. Here's my last thought: " + str(response))
        st.toast("Sorry about that, I'm still learning. Try asking the question again, usually I can get it right the second time.", icon='🤖')

def load_example_file():
    return open('src/1000ExampleRecords.csv')

def add_user_prompt(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

def parse_cb(callback):
    return Counter({
        "total_tokens": callback.total_tokens,
        "prompt_tokens": callback.prompt_tokens,
        "completion_tokens": callback.completion_tokens,
        "total_cost": callback.total_cost
    })

def get_return(investment, profit):
    investment = float(investment[1:])
    profit = float(profit[1:])
    return (profit - investment)/investment

if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []

if "conversation_memory" not in st.session_state:
    st.session_state["conversation_memory"] = ConversationBufferMemory(memory_key="chat_history")

if "token_usage" not in st.session_state: 
    st.session_state["token_usage"] = NEW_BUDGET
 

with st.sidebar:
    st.markdown("# CashFlowIQ 💰✨")
    st.markdown("---")
    st.markdown("CashFlowIQ can analyze your personal finance transactions and help you save money!")
    st.markdown("Download your transactions from your personal finance app like [Intuit Mint](https://mint.intuit.com/transactions) or [Rocket Money](https://app.rocketmoney.com/transactions).")
    st.markdown("No information is stored permanently and all data processing happens in your browser on your device.")
    with st.expander("_Just want to try it first? Click here_"):
        st.download_button("Download Example Transactions", data=load_example_file(), use_container_width=True)

    # openai_api_key = st.sidebar.text_input("OpenAI API Key", key="chatbot_api_key", type="password", autocomplete="off")
    openai_api_key = st.secrets.openai.api_key

    uploaded = st.file_uploader("Upload Transactions")

    st.button("New Chat", on_click=new_chat, type="primary", use_container_width=True)
    st.markdown("---")
    if "token_usage" in st.session_state:
        st.markdown("Model Usage Stats")
        total_cost = st.text_input(disabled=True, label="Total Cost (USD)", value="$"+str(st.session_state['token_usage'].get('total_cost')))
        # theo_savings = st.text_input(label="Theoretical Monthly Savings (USD)", value="$20")
        # total_return = get_return(total_cost, theo_savings)
        # st.markdown(total_return)
        with st.expander("Usage Details"):
            st.text_input(disabled=True, label="Total Tokens", value=st.session_state['token_usage'].get('total_tokens'))
            st.text_input(disabled=True, label="Prompt Tokens", value=st.session_state['token_usage'].get('prompt_tokens'))
            st.text_input(disabled=True, label="Completion Tokens", value=st.session_state['token_usage'].get('completion_tokens'))
    st.sidebar.button("Refresh Token Data", use_container_width=True)

if uploaded is not None and "agent" not in st.session_state and openai_api_key:
    st.session_state["model_id"] = "gpt-4"
    st.session_state["llm"] = ChatOpenAI(model_name=st.session_state["model_id"], openai_api_key=openai_api_key, temperature=0)
    tools = [
        # Tool(
        #     name="Graphing Tool",
        #     func=parsing_columns,
        #     description="Useful for when you need to graph something simple using two columns you know relate to both time and value. The input to this tool should be a comma separated list of those two columns. for example 'Date,Amount' would be valid input."
        # )
    ]
    st.session_state["agent"] = create_csv_agent(
                path=uploaded,
                tools=tools,
                llm=st.session_state["llm"],
                agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                # agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                memory=st.session_state["conversation_memory"],
                handle_parsing_errors=True,
                verbose=False, 
                max_iterations=5
            )

    add_assistant_response("Thanks for uploading that! I'll start crunching the numbers right away...", None)
    
    for prompt in INITIAL_PROMPTS:
        if prompt.startswith('GRAPH'):
            user_prompt = prompt.split('~')[1] # hiding the prompt template
            add_user_prompt(user_prompt)
            with st.spinner(text=get_random_thought()):
                with get_openai_callback() as cb:
                    add_assistant_response(st.session_state["agent"].run(prompt), cb)
        else:
            add_user_prompt(prompt)
            with st.spinner(text=get_random_thought()):
                with get_openai_callback() as cb:
                    add_assistant_response(st.session_state["agent"].run(BUDGET_PROMPT + prompt), cb)
    
    # outro = "Thanks! What are 3 other questions I should ask you about my transactions?"
    # add_user_prompt(outro)
    # with st.spinner(text=get_random_thought()):
    #     with get_openai_callback() as cb:
    #         add_assistant_response(st.session_state["agent"].run(BUDGET_PROMPT + outro), cb)

if "messages" not in st.session_state:
    st.session_state["messages"] = NEW_CHAT_START

for msg in st.session_state.messages:
    if msg['content'].startswith('st.'):
        try: 
            eval(msg['content'])
        except Exception as e:
            st.toast("Loading a graph failed...")
    else:
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Type your personal finance question here. Start your message with 'GRAPH' to graph it!", disabled=uploaded is None):
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if uploaded is None:
        st.toast("Please upload your transactions file to use CashFlowIQ!")
    add_user_prompt(prompt)
    st.line_chart(pd.read_csv(uploaded), x="Date", y="Balance")


    if uploaded is not None and "agent" in st.session_state:
        with st.spinner(text=get_random_thought()):
            with get_openai_callback() as cb:
                if prompt.startswith('GRAPH'):
                    prompt = GRAPH_PREFIX.format(prompt)
                    add_assistant_response(st.session_state["agent"].run(prompt), cb)
                elif prompt.startswith('st.'):
                    add_assistant_response(prompt)
                else:
                    add_assistant_response(st.session_state["agent"].run(BUDGET_PROMPT + prompt), cb)

    
        


    
