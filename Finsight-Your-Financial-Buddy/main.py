# Author: Suresh Ratlavath
# Email: srdev3175@gmail.com
# Date: 15-09-2023

# Import statements
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import BaseChatPromptTemplate
from langchain import SerpAPIWrapper, LLMChain
from langchain.chat_models import ChatOpenAI
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, HumanMessage
import re
import os
import streamlit as st
from pprint import pprint
from langchain.retrievers.web_research import WebResearchRetriever
from elevenlabs import generate, play
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models.openai import ChatOpenAI
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.chains import RetrievalQAWithSourcesChain
# Importing necessary libraries
import langchain
from elevenlabs import set_api_key
# Load environment variables from the .env file
def setup():
    OPENAI_API_KEY=st.text_input("Enter your OPENAI GPT4 API KEY:",type="password")
    GOOGLE_CSE_ID=st.text_input("Enter your GOOGLE CSE ID:",type="password")
    GOOGLE_API_KEY=st.text_input("Enter your GOOGLE API KEY:",type="password")
    ELEVENLABS_API_KEY=st.text_input("Enter ElevenLabs API KEY:",type="password")
    # Set the environment variables
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    os.environ["GOOGLE_CSE_ID"] = GOOGLE_CSE_ID
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
    set_api_key(ELEVENLABS_API_KEY)
    
    if st.button("Submit"):
        st.success("Succesfully Setup keys")
        st.success("Please go to Chat section")
def app():
    # Function for web scraping tool
    def web_scraping_tool(query: str) -> str:
        # Vectorstore
        vectorstore = Chroma(embedding_function=OpenAIEmbeddings(), persist_directory="./chroma_db_oai")

        # LLM
        llm = ChatOpenAI(model="gpt-3.5-turbo-16k",temperature=0.4)

        # Search
        search = GoogleSearchAPIWrapper()

        # Initialize
        web_research_retriever = WebResearchRetriever.from_llm(
            vectorstore=vectorstore,
            llm=llm,
            search=search,
        )
        qa_chain = RetrievalQAWithSourcesChain.from_chain_type(llm, retriever=web_research_retriever)
        result = qa_chain({"question": query})
        return result
    # List of available tools
    tools = [
        Tool(
            name="WebScraping",
            func=web_scraping_tool,
            description="Useful for when you need to answer questions about current events and market data. Use this tool to get current information about Financial investment and more. and also Useful for scraping information of Financial and market from websites and internet"
        ),
    ]

    # Defining chat prompts
    # (Please note that prompt variables are repeated and will need to be maintained in sync)
    prompt = """Hey AI your name is Sunny,Your Financial Buddy, please act as if you're my close friend, not a professional, and let's talk about my financial goals and plans. Your tone should be warm, friendly, and reassuring, just like a trusted friend. Feel free to guide me through financial decisions and offer advice as you would to a close buddy. You can also access this tool to get more better responses.

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be {tool_names}
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    These were previous tasks you completed:
    {history}
    Begin!

    Question: {input}
    {agent_scratchpad}"""

    if "messages" not in st.session_state:
            st.session_state.messages = []

    # Set up a prompt template
    class CustomPromptTemplate(BaseChatPromptTemplate):
        template: str
        tools: List[Tool]

        def format_messages(self, **kwargs) -> str:
            intermediate_steps = kwargs.pop("intermediate_steps")
            thoughts = ""
            for action, observation in intermediate_steps:
                thoughts += action.log
                thoughts += f"\nObservation: {observation}\nThought: "
            kwargs["agent_scratchpad"] = thoughts
            kwargs["history"] = st.session_state.messages
            kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
            kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
            formatted = self.template.format(**kwargs)
            return [HumanMessage(content=formatted)]

    # Creating a custom prompt
    prompt = CustomPromptTemplate(
        template=prompt,
        tools=tools,
        input_variables=["input", "intermediate_steps"]
    )

    # Custom output parser
    class CustomOutputParser(AgentOutputParser):

        def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
            if "Final Answer:" in llm_output:
                return AgentFinish(
                    return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                    log=llm_output,
                )

            regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
            match = re.search(regex, llm_output, re.DOTALL)
            if match:
                action = match.group(1).strip()
                action_input = match.group(2).strip(" ").strip('"')
                return AgentAction(tool=action, tool_input=action_input, log=llm_output)

            if "\nObservation:" in llm_output:
                observation = llm_output.split("\nObservation:", 1)[-1].strip()
                return AgentAction(tool="Observation", tool_input="", log=llm_output)

            return AgentFinish(
                return_values={"output": llm_output.strip()},
                log=llm_output,
            )

    # Creating an output parser
    output_parser = CustomOutputParser()

    # Initializing ChatOpenAI model
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0.8)

    # Creating an LLMChain
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # List of tool names
    tool_names = [tool.name for tool in tools]

    # Creating an LLMSingleActionAgent
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\nObservation:"],
        allowed_tools=tool_names
    )

    # Creating an AgentExecutor
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

    # Streamlit chat interface
    spinner_html = """
    <div class="spinner"></div>

    <style>
    .spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-left: 4px solid #3498db;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    animation: spin 1s linear infinite;
    }

    @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
    }
    </style>
    """
    st.markdown("<h1 align=center>💲FinSight - Your Finance Buddy📈</h1>", unsafe_allow_html=True)
    for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    if prompt := st.chat_input("Ask a Question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown(spinner_html,unsafe_allow_html=True)
            ai_response = agent_executor.run(prompt)
            message_placeholder.write(ai_response)
            audio = generate(
                text=ai_response,
                voice="Bella",
                model="eleven_monolingual_v1"
            )
            play(audio)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
def home_page():

    # HTML code for the welcome message
    welcome_message = """
    <div style="text-align: center;">
        <h1>Welcome <br> 💲FinSight - Your Finance Buddy📈</h1>
        <p>To get started,Please go to <a href='#' onclick='open_settings()'>Settings</a> and set up your API keys.</p>
    </div>
    
    <script>
        // JavaScript function to open the Settings page
        function open_settings() {
            window.location.href = '#Settings';
        }
    </script>
    """
    
    # Display the welcome message using st.markdown
    st.markdown(welcome_message, unsafe_allow_html=True)
def main():
    st.sidebar.title("FinSight")
    selected_page = st.sidebar.radio("Go to:", ["Home", "Settings", "Chat"])
    if selected_page=="Home":
        home_page()
    elif selected_page == "Settings":
        setup()
    elif selected_page == "Chat":
        app()
main()
