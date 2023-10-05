import os
from dotenv import load_dotenv
import streamlit as st
from llama_index.llms import OpenAI
# from llama_index import VectorStoreIndex, SimpleDirectoryReader, load_index_from_storage, StorageContext, ServiceContext, LLMPredictor

from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.llms import OpenAI
from langchain.tools import Tool
from langchain.utilities import SerpAPIWrapper, DuckDuckGoSearchAPIWrapper
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, LLMMathChain, SimpleSequentialChain
# from langchain.memory import ConversationBufferMemory

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
SERP_API_KEY = st.secrets["SERPAPI_API_KEY"]

# Initialize Web Agent and LLM
def initialize_app(model_name='gpt-4', temperature=0.6):
    search = DuckDuckGoSearchAPIWrapper()
    tools = [
        Tool(
            name="Intermediate Answer",
            func=search.run,
            description="useful for when you need to answer questions about latest company research, events or news"
        ),
    ]
    llm = OpenAI(model_name=model_name, temperature=temperature)
    agent_chain = initialize_agent(tools, llm, agent='self-ask-with-search', handle_parsing_errors=True, verbose=True)
    return agent_chain, llm

agent_chain, llm = initialize_app()


# Cache the SERP API call
@st.cache_resource(show_spinner=False)
def get_latest_info(company_prompt):
    basic_info = agent_chain.run(f"Provide a detailed analysis of the company, {company_prompt}")
    exec_team_info = agent_chain.run(f"Provide information on the top executives at the company, {company_prompt} and its headcount")
    combined_info = f"{basic_info}\n\n{exec_team_info}"
    return combined_info

# Cache the LLM responses
@st.cache_resource(show_spinner=False)
def generate_research(company_prompt, latest_info):
    notes = {"notes": latest_info}
    sequential_chain = SimpleSequentialChain(chains=[research_chain, notes_chain, memo_chain], verbose=True)
    return sequential_chain.run(company_prompt)

# @st.cache_resource(show_spinner=False)
# def get_latest_info(company_prompt):
#     # Basic company analysis
#     basic_info = agent_chain.run(f"Provide a detailed analysis of the company, {company_prompt}")
#     # Executive team details
#     exec_team_info = agent_chain.run(f"Provide extensive details on the executive team of the company, {company_prompt}")
#     # Fundraising status
#     fundraising_info = agent_chain.run(f"Provide information on the fundraising status of the company, {company_prompt}")
#     # Value chain analysis
#     value_chain_info = agent_chain.run(f"Give me extensive detail on the value chain analysis for the company, {company_prompt}")
#     # Combine all the information
#     combined_info = f"{basic_info}\n\n{exec_team_info}\n\n{fundraising_info}\n\n{value_chain_info}"
#     return combined_info

# App frontend and framework

# copies 
home_title = "Finsights"
home_introduction = "Where researching and investing in startups meets the prowess of OpenAI's LLM technology. Powered by #Langchain & #LlamaIndex, Bringing OpenAI's prowess to your fingertips to generate detailed investment memos and company insights to supercharge your research."
home_privacy = "We value and respect your privacy. To safeguard your personal details, we utilize the hashed value of your OpenAI API Key, ensuring utmost confidentiality and anonymity. Your API key facilitates AI-driven features during your session and is never retained post-visit. You can confidently fine-tune your research, assured that your information remains protected and private."
home_icon="https://api.dicebear.com/7.x/icons/svg?seed=Abby&backgroundColor=80cbc4&icon=cashCoin,coin,eyeglasses,newspaper"

st.set_page_config(
    page_title="Startup Review (with Langchain + LlamaIndex)",
    page_icon="https://api.dicebear.com/7.x/icons/svg?seed=Abby&backgroundColor=80cbc4&icon=cashCoin,coin,eyeglasses,newspaper",
    layout="wide",
    menu_items={"About": "Powered by #Langchain & #LlamaIndex, Bringing OpenAI's prowess to your fingertips to generate detailed memos or company insights in seconds. Input company info & get a detailed investment memo.", "Get help": None, "Report a Bug": None}
)

with st.sidebar:
    st.header("👨‍💻 About the Author")
    st.write("""
    **Yaksh Birla** is a financial professional and tech enthusiast. Driven by passion and a love for leveraging AI tools and sharing knowledge, he created this platform to test new AI tools in the context of Web-enabled investment research and financial analysis.

    Connect with me, or contribute!
    """)

    st.divider()
    st.subheader("🔗 Connect with Me", anchor=False)
    st.markdown(
        """
        - [👔 LinkedIn](https://www.linkedin.com/in/yakshb/)
        - [🐙 Github Profile](https://github.com/yakshb)
        - [🌐 Medium](https://medium.com/@yakshb)
        """
    )

    st.divider()
    st.subheader("🏆 Streamlit Hackathon 2023", anchor=False)
    st.write("This application is Yaksh's entry for the Streamlit Hackathon held in September 2023.")

    st.divider()
    st.write("Made with 🦜️🔗 Langchain and 🦙 LlamaIndex")

#st.title(home_title)
st.markdown(f"""## VC/Startup Research Assistant⚡ <span style=color:#2E9BF5><font size=6>Beta</font></span>""",unsafe_allow_html=True)
st.markdown(f"#### Powered by Langchain and LlamaIndex")

with st.expander("What is this app about?", expanded=True):
    st.info("""
    Welcome to the AI-powered Startup Analyzer!

    Designed for angel investors, analysts, and VCs, this application offers a seamless way to generate in-depth investment research on any company, whether public or private. Key features include:

    1. **Deep Analysis**: Harnessing the power of AI, the app delves into the web, extracting the latest and most pertinent data about your chosen company.
    
    2. **Comprehensive Reports**: The AI's output encompasses a range of facets such as the company's value proposition, business model, market potential, leadership team, financial health, and technological edge.
    
    3. **User-Friendly Interface**: Simply input the company's name, and let the AI do the heavy lifting, furnishing you with a detailed report in mere moments.

    Aimed at both investment considerations and general curiosity, this tool is your gateway to a profound understanding of any company, all underpinned by cutting-edge AI technology.
    
    """, icon="ℹ️")

with st.expander("How does it work?"):
    st.info("""

    The Startup Analyzer employs sophisticated Large Language Models (LLMs) to craft extensive research reports on startups or companies. Here's the process:

    1. **User Input**: Begin by entering the name of a startup or company you wish to investigate. You can also incorporate your personal "field notes" to enhance the AI's output.
    
    2. **AI Agents at Work**: Langchain Agents are deployed to retrieve and refine the relevant data about the specified company.
    
    3. **Deep Dive with LLM**: The accumulated data undergoes a thorough analysis by the LLM, yielding insights that span the company's value proposition, business strategy, market opportunities, leadership dynamics, and more.
    
    4. **Customization via Advanced Filters**: Tailor the AI's operations using the advanced filters. Currently, the app supports OpenAI's GPT Models, and you can modulate the AI's temperature to tweak the style and depth of the ensuing report.
    
    5. **Final Report**: The culmination is a detailed research report, accessible directly on the platform or available for download for offline perusal.
    
    The overarching objective is to equip investors, analysts, and the curious-minded with a potent tool that expedites comprehensive research.

    """, icon="ℹ️")

with st.expander("Will my data be private?"):
    st.info(f"{home_privacy}")

st.divider()

main_col, history_col = st.columns([3,1])
with main_col:
    # with col1:
    company_prompt = st.text_input('**Enter the Startup / Company Name Here:**')

    with st.expander("Advanced Filters (Testing)"):
        col1, col2 = st.columns(2)
        with col1:
            llm_model_options = ['gpt-4', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo-16k','gpt-3.5-turbo']  # Add more models if available
            llmmodel_input = st.selectbox('Select LLM Model:', llm_model_options, index=0)
        with col2:
            llmtemperature_input = st.slider('Set AI Randomness / Creativity', min_value=0.1, max_value=1.0, value=0.6)
        
    agent_chain, llm = initialize_app(model_name=llmmodel_input, temperature=llmtemperature_input)

    user_notes = st.text_area('Add Your Personal Notes About the Company Here:')


    # Prompt templates
    research_template = PromptTemplate(
        input_variables = ['company'],
        template='Evaluate the value proposition, product or service, business model, market opportunity, executive team, financials, and technology-related information about the company, {company}. Keep your answers technical and based on facts – do not hallucinate features.'
    )

    memo_template = PromptTemplate(
        input_variables = ['company'],
        template='As an experienced investor with deep experience in private equity and venture capital, write me a detailed investment analysis about the company, {company}. This report should, at a minimum, have the following sections: Summary, Product Evaluation, Market Opportunity, Financials & Unit Economics, Executive Team, Risks'
    )

    notes_template = PromptTemplate(
        input_variables = ['notes'],
        template='Evaluate the {notes} provided in the context of evaluating a company or startup as an investment'
    )

    research_chain = LLMChain(llm=llm, prompt=research_template)
    memo_chain = LLMChain(llm=llm, prompt=memo_template)
    notes_chain = LLMChain(llm=llm, prompt=notes_template)

    if company_prompt:
        latest_info = get_latest_info(company_prompt)

    # Display LLM answers
    if st.button(f'Generate Investment Research'):
            with st.spinner(f'Generating Research for {company_prompt}... This could take 1-2 mins'):
                response = generate_research(company_prompt, latest_info)
                st.markdown(response)
                st.download_button('Download Report', response, file_name=f'Finsights Research - {company_prompt}.doc')

with history_col:
    with st.expander("**Research History**"):
        st.info("Coming Soon")

