import streamlit as st

import os

from langchain.chat_models import ChatOpenAI
from langchain.callbacks import StreamlitCallbackHandler
from langchain.callbacks import FinalStreamingStdOutCallbackHandler
from langchain.callbacks import get_openai_callback
import openai
import base64

st.set_page_config(page_title= "The Joe RAGan Experience", page_icon="🤣", layout="wide")
#ADD Width and Theme to config


st.markdown('##')
st.markdown('##')
st.markdown('##')
st.markdown('##')
st.markdown('##')
st.markdown('##')
st.markdown('##')

def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
 
    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "gif"
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(main_bg).decode()});
             background-repeat: no-repeat;
             background-size: cover;
             background-position: center;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

with open('Final_Background.gif', 'rb') as pic_file:
   background = pic_file.read()
   set_bg_hack(background)

# Lets implement the enter api key function
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
openai.api_key = openai_api_key


### ADDING THE SIDE BAR INFO
st.markdown("""
<style>
    .stChatFloatingInputContainer {
        padding-bottom: 30px !important;
        padding-top: 0rem;
        background-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🔎  Query the Joe Rogan Experience")

    st.markdown('''
    ## Improve RAG applications via intelligent chunking and information enrichment 🚀
    
    This app enables exploration into the episodes of the Joe Rogan Experience, allowing you to ask specific questions regarding the content of certain epsiodes. 
    
    This app is powered by Streamlit, OpenAI, LangChain and Weaviate.'''
    )
    
    with st.expander("✨ ABOUT", False):
       st.markdown("""
        Welcome to The Joe RAG-an Experience! This chatbot has access to a few episode transcripts of the Joe Rogan podcast and can answer questions about the discussions that occurred within those episodes. This project attempts to improve upon the traditional RAG (Retrieval Augmented Generation) implementation by chunking the episode transcripts dynamically based on semantic context, as well as enriching these chunks with tags describing the topics discussed within the chunk. 
        """
       )

    with st.expander("📚 AVAILABLE EPISODES", False):
       st.markdown("""
        - The Joe Rogan Experience #1470 - Elon Musk
        - The Joe Rogan Experience #1863 - Mark Zuckerberg
        - The Joe Rogan Experience #1904 - Neil deGrasse Tyson
        """
       )
    with st.expander("📝 SAMPLE QUESTIONS", False):
       st.markdown("""
        - What did Elon say about the neuralink's potential health hazards?
        - What did Zuckerberg say about Spotify's recommendation algorithm?s
        - What are Zuckerberg's' thoughts on the future of VR?
        - According to Neil deGrasse Tyson how do people misunderstand statistics?
        """
       )
    with st.expander("🧠 SMART CHUNKING", False):
       st.markdown("""
        One issue we have noticed with traditional chunking methods is that they can often cut off relevant context as they denote chunk boundaries with arbitrary word or token counts. Although this is partially solved by adding overlap between chunks, we thought that perhaps this could be made even better by having a LLM determine where the chunk boundaries should be placed. To do this we first use a standard text splitter to create “default” chunks, then prompt a LLM to adjust these chunks in order to retain semantic context and avoid cutting off a chunk in the middle of a thought or sentence. This way, our chunks are “intelligently” selected in order to optimally retain context. 
        """
       )
    with st.expander("🔮 INFORMATION ENRICHMENT", False):
       st.markdown("""
        Another improvement we wanted to try on the traditional RAG implementation was information enrichment. The idea is to add another form of metric to retrieve context based on, rather than relying purely on a vector similarity search based on the user query. When performing the chunking process, we additionally have a LLM assign topic descriptions to each chunk. This comes in the form of a couple ~sentence long tags describing what is discussed within the chunk. When we are attempting to retrieve context to help answer a user query, we first search through the topic descriptions to grab relevant topics, then use those topics to help us narrow down the similarity search for the embedded chunks. The goal behind this technique was to improve retrieval of relevant context and limit retrieval of irrelevant context. 
        """
       )


    st.markdown(""" 
                Created by Lucas Werneck & Preston Goren
                


                ** ALL EPSIODES WILL BE ADDED AT A LATER DATE **
                
                """)

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

st.markdown("""
<style>
    [data-testid=stChatFloatingInputContainer css-1v6qhwz e1d2x3se2] {
        background-color: #FF8080;
        padding-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)



from langchain.callbacks.base import BaseCallbackHandler
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


# Connect to and create weaviate vectorstores:
import weaviate
auth_config = weaviate.AuthApiKey(api_key=st.secrets.WEAVIATE_API_KEY)

client = weaviate.Client(
    url="https://streamlit-hackathon-llm-2zcna00b.weaviate.network",
    auth_client_secret=auth_config,
    additional_headers={
        "X-OpenAI-Api-Key": openai_api_key
    }
)

from langchain.vectorstores import Weaviate
from langchain.embeddings.openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(openai_api_key= openai_api_key)
chunk_vectorstore = Weaviate(client, index_name = "Chunk_Node", text_key = "chunk_body", attributes=['ep_title','ep_link'])
topic_vectorstore = Weaviate(client, index_name = "Topic_Node", text_key = "topic")


#Custom Search Function using Topics Filter:
def search_with_topics(question):
    topics = topic_vectorstore.similarity_search(question)
    topicList = []
    for doc in topics:
        topicList.append(doc.page_content)
    print("List of relevant topics: {}".format(topicList))

    #construct where filter with relevant topic list
    where_filter = {
            "path": ["chunk_topics"],
            "operator": "ContainsAny",
            "valueText": topicList     
    }

    #perform search of chunks with relevant topics
    chunks = chunk_vectorstore.similarity_search(question, where_filter = where_filter, additional = ["certainty"])
    return chunks



# Create the sessionstate tools and agent:
from langchain.tools import Tool
if 'tools' not in st.session_state:
   st.session_state.tools = [
    Tool.from_function(
    name = "joerogansearch",
    description="Searches and returns documents from the Joe Rogan knowledge base to answer any questions regarding content from the podcast episode.",
    func=search_with_topics,)
]

from langchain.schema import SystemMessage
sys_mes_joe = SystemMessage(content="Do your best to answer the questions. The questions will all be about the content of epsiodes from the Joe Rogan Podcast. Use the joerogansearch tool to look up relevant information. When using the context from the tool be sure to cite the source by providing the URL Link at the end of your response.")


from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
if 'joe_rogan_agent' not in st.session_state:
   llm = ChatOpenAI(temperature=0,openai_api_key=openai_api_key, model="gpt-3.5-turbo-16k", streaming=True)
   st.session_state.joe_rogan_agent = create_conversational_retrieval_agent(llm, st.session_state.tools, verbose = False, system_message=sys_mes_joe)
   


# Set up the streamlit chat interface
avatars = {"user": '👨🏽‍💻', "assistant": 'jrelogo.webp'}

if "messages" not in st.session_state:
   st.session_state["messages"] = [{"role":"assistant", "content": "What would you like to know?"}]

if "tokens" not in st.session_state:
    st.session_state.tokens = ["Tokens Used: 0 Prompt Tokens: 0 Completion Tokens: 0 Successful Requests: 0 Total Cost (USD): $0.0"]

if st.sidebar.button("Clear message history"):
    st.session_state.messages = [{"role":"assistant", "content": "What would you like to know?"}]
    llm = ChatOpenAI(temperature=0,openai_api_key=openai_api_key, model="gpt-3.5-turbo-16k", streaming=True)
    st.session_state.joe_rogan_agent = create_conversational_retrieval_agent(llm, st.session_state.tools, verbose = True, system_message=sys_mes_joe)

with st.container():
   for n, msg in enumerate(st.session_state.messages):
      st.chat_message(msg["role"], avatar=avatars[msg["role"]]).write(msg["content"])

user_query = st.chat_input(placeholder="Enter Question")

if user_query:
   st.session_state.messages.append({"role": "user", "content": user_query})
   st.chat_message("user", avatar=avatars["user"]).write(user_query)

   with st.chat_message("assistant", avatar=avatars["assistant"]):
    stream_handler = StreamHandler(st.empty())
    response = st.session_state.joe_rogan_agent({"input": user_query},callbacks=[stream_handler])
    st.session_state.messages.append({"role": "assistant", "content": response["output"]})
   
