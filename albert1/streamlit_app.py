import streamlit as st
from components.sidebar import sbar

#Config
st.set_page_config(layout="wide", page_icon="💬", page_title="Albert🤖")

st.markdown(
    "<h1 style='text-align: center; background-color:WHITE; padding: 20px; color: Black; border-radius: 10px;'>Welcome to ALBERT !👋🤖</h1>",
    unsafe_allow_html=True,
)

st.markdown("""
<style>

	.stTabs [data-baseweb="tab-list"] {
		gap: 50px;
    }

	.stTabs [data-baseweb="tab"] {
		height: 50px;
        white-space: pre-wrap;
		background-color: #red;
		border-radius: 4px 6px 0px 0px;
		gap: 10px;
		padding-top: 20px;
		padding-bottom: 20px;
    }

	.stTabs [aria-selected="true"] {
  		background-color: #FFFF;
	}

</style>""", unsafe_allow_html=True)

import streamlit as st


sbar() 

tab1, tab2 = st.tabs(["Wiki-Chat", "News Summary"])  
css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.5rem;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)

with tab1:
    import os
    import time
    import pickle
    import streamlit as st
    from datetime import datetime
    from streamlit_chat import message

    from langchain.vectorstores import FAISS
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.chat_models import ChatOpenAI
    from langchain.vectorstores import Chroma 
    from langchain.schema import AIMessage, HumanMessage, SystemMessage

    #from wiki_content import get_wiki

    import requests
    import wikipedia
    from bs4 import BeautifulSoup

    st.markdown(
    """
    
    ##### WikiChat
    * A sample app for to generate information instantly from Wikipedia and also ask questions over it .
    """
)

    def get_wiki(search):
        # set language to English (default is auto-detect)
        lang = "en"

        """
        fetching summary from wikipedia
        """
        # set language to English (default is auto-detect)
        summary = wikipedia.summary(search, sentences = 5)

        """
        scrape wikipedia page of the requested query
        """

        # create URL based on user input and language
        url = f"https://{lang}.wikipedia.org/wiki/{search}"

        # send GET request to URL and parse HTML content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # extract main content of page
        content_div = soup.find(id="mw-content-text")

        # extract all paragraphs of content
        paras = content_div.find_all('p')

        # concatenate paragraphs into full page content
        full_page_content = ""
        for para in paras:
            full_page_content += para.text

        # print the full page content
        return full_page_content, summary


    global embeddings_flag
    embeddings_flag = False

    st.markdown("<h1 style='text-align: center; color: Red;'>Chat-Wiki</h1>", unsafe_allow_html=True)

    buff, col, buff2 = st.columns([1,3,1])
    # Set API keys from session state
    openai_key = st.secrets['openai_api_key']

    if len(openai_key):

        chat = ChatOpenAI(temperature=0, openai_api_key=openai_key)

        if 'all_messages' not in st.session_state:
            st.session_state.all_messages = []

        def build_index(wiki_content):
            print("building index .....")
            text_splitter = CharacterTextSplitter(        
            separator = "\n",
            chunk_size = 1000,
            chunk_overlap  = 200,
            length_function = len,  
                )  
            texts = text_splitter.split_text(wiki_content)
            embeddings = OpenAIEmbeddings()
            docsearch = FAISS.from_texts(texts, embeddings)
            with open("./embeddings.pkl", 'wb') as f:
                pickle.dump(docsearch, f)

            return embeddings, docsearch

        # Create a function to get bot response
        def get_bot_response(user_query, faiss_index):
            docs = faiss_index.similarity_search(user_query, K = 6)
            main_content = user_query + "\n\n"
            for doc in docs:
                main_content += doc.page_content + "\n\n"
            messages.append(HumanMessage(content=main_content))
            ai_response = chat(messages).content
            messages.pop()
            messages.append(HumanMessage(content=user_query))
            messages.append(AIMessage(content=ai_response))

            return ai_response

        # Create a function to display messages
        def display_messages(all_messages):
            for msg in all_messages:
                if msg['user'] == 'user':
                    message(f"You ({msg['time']}): {msg['text']}", is_user=True, key=int(time.time_ns()))
                else:
                    message(f"IA-Bot ({msg['time']}): {msg['text']}", key=int(time.time_ns()))

        # Create a function to send messages
        def send_message(user_query, faiss_index, all_messages):
            if user_query:
                all_messages.append({'user': 'user', 'time': datetime.now().strftime("%H:%M"), 'text': user_query})
                bot_response = get_bot_response(user_query, faiss_index)
                all_messages.append({'user': 'bot', 'time': datetime.now().strftime("%H:%M"), 'text': bot_response})

                st.session_state.all_messages = all_messages
                
            
        # Create a list to store messages

        messages = [
                SystemMessage(
                    content="You are a Q&A bot and you will answer all the questions that the user has. If you dont know the answer, output 'Sorry, I dont know' .")
            ]

        search = st.text_input("What's on your mind?")

        if len(search):
            wiki_content, summary = get_wiki(search)

            if len(wiki_content):
                try:
                    # Create input text box for user to send messages
                    st.write(summary)
                    user_query = st.text_input("You: ","", key= "input")
                    send_button = st.button("Send")

                    if len(user_query) and send_button:
                        # Create a button to send messages
                        if not embeddings_flag:
                            embeddings, docsearch = build_index(wiki_content)
                            embeddings_flag = True
                            with open("./embeddings.pkl", 'rb') as f: 
                                faiss_index = pickle.load(f)
                    # Send message when button is clicked
                    if embeddings_flag:
                        send_message(user_query, faiss_index, st.session_state.all_messages)
                        display_messages(st.session_state.all_messages)

                except:
                    st.write("something's Wrong... please try again")
            
with tab2:
    import streamlit as st, tiktoken
    from langchain.chat_models import ChatOpenAI
    from langchain.utilities import GoogleSerperAPIWrapper
    from langchain.document_loaders import UnstructuredURLLoader
    from langchain.chains.summarize import load_summarize_chain

    st.markdown(
    """   
    ##### News Summary
    * A sample app for Google news search and summaries using OpenAI and Langchain.
    
    
    """
)

    # Set API keys from session state
    openai_api_key = st.secrets['openai_api_key']
    serper_api_key = st.secrets['serper_api_key']


    # Streamlit app
    # st.subheader('News Summary')
    num_results = st.number_input("Number of Search Results", min_value=1, max_value=3) 
    search_query = st.text_input("Enter Search Query")
    col1, col2 = st.columns(2)

    # If the 'Search' button is clicked
    if col1.button("Search"):
        # Validate inputs
        if not openai_api_key or not serper_api_key:
            st.error("Please provide the missing API keys in Settings.")
        elif not search_query.strip():
            st.error("Please provide the search query.")
        else:
            try:
                with st.spinner("Please wait..."):
                    # Show the top X relevant news articles from the previous week using Google Serper API
                    search = GoogleSerperAPIWrapper(type="news", tbs="qdr:w1", serper_api_key=serper_api_key)
                    result_dict = search.results(search_query)

                    if not result_dict['news']:
                        st.error(f"No search results for: {search_query}.")
                    else:
                        for i, item in zip(range(num_results), result_dict['news']):
                            st.success(f"Title: {item['title']}\n\nLink: {item['link']}\n\nSnippet: {item['snippet']}")
            except Exception as e:
                st.exception(f"Exception: {e}")


        



