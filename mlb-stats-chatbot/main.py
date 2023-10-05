from langchain.llms import Clarifai
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.tools import AIPluginTool
from langchain.callbacks import StreamlitCallbackHandler

import streamlit as st

USER_ID = 'openai'
APP_ID = 'chat-completion'
MODEL_ID = 'GPT-4' 
MODEL_VERSION_ID = 'ad16eda6ac054796bf9f348ab6733c72'

tool = AIPluginTool.from_plugin_url("https://mlb-stats-chatbot-production.up.railway.app//.well-known/ai-plugin.json")


# Used to load the plugin
tools = load_tools(["requests_get"])

tools += [tool]

### Streamlit Implementation

st.title("⚾ MLB Stats Chatbot")

"""
You can use this chatbot to retrieve up-to-date MLB statistics and information. 
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot that can search for MLB stats. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="What team is leading the AL East standings? Go Orioles 😉"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    clarifai_llm = Clarifai(user_id=USER_ID,app_id=APP_ID, model_id=MODEL_ID, model_version_id=MODEL_VERSION_ID)
    agent_chain = initialize_agent(tools, clarifai_llm, verbose=True, agent_chain=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)
    with st.chat_message("assistant"):
        try:
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = agent_chain.run(st.session_state.messages, callbacks=[st_cb])
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            # Log the error on stdout
            print(f"An error occured: {e}")

            if "OpenAI API Error: InvalidRequestError" in str(e):
                response = """The request is too long for the AI model to digest. Try altering your prompt to segment the requests i.e. if you would like to 
                            get the game logs over a 4 month period, try writing 4 separate prompts for each month. Otherwise, the chatbot will
                            try to retrieve all the months at once and you will get this error."""

            else:
                response = "I'm sorry but an error was encountered while processing your request. Please try again. If the error persists, try a different prompt."

        st.write(response)