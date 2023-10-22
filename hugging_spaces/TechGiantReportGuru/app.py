# Import required modules from the langchain library and other packages
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import  RetrievalQA
from langchain.chat_models import ChatOpenAI
import os
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
from PIL import Image

def main():
    # Streamlit page configuration
    st.set_page_config(page_title="Tech Giant Report Guru")
    st.title("Tech Giant Report Guru")
    path = os.path.dirname(__file__)
    style = path+'/style.css'
    # style = '/mount/src/gen-ai-apps/useful/TechGiantReportGuru/style.css'
    with open(style) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Custom CSS for Streamlit using Google Fonts
    # st.markdown(
    #     """
    #     <style>
    #     @import url('https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500&family=Literata:opsz,wght@7..72,500&display=swap');
    #     html, body, textarea , [class*="css"] {
    # 			font-family: 'Inter Tight', sans-serif !important;
    # 			}
    #     </style>
    #     """,
    #     unsafe_allow_html=True,
    # )

    # # Custom CSS for Streamlit using Google Fonts
    # st.markdown(
    #     """
    #     <style>
    #     @import url('https://fonts.googleapis.com/css2?family=Audiowide&display=swap');
    #     html, body, textarea , [class*="css"] {
    # 			font-family: 'Audiowide', 'Gloria Hallelujah', 'Poppins', 'Oswald', 'DM Sans', 'Urbanist', 'Gothic A1', 'Audiowide', 'Dela Gothic One', 'Special Elite', sans-serif !important;
    # 			}
    #     </style>
    #     """,
    #     unsafe_allow_html=True,
    # )


    # Introductory messages and sample questions
    # intoductory_message='''Hello, I'm **Ben**—your go-to expert for **Form 10K Benchmarking**!\n\nPowered by GPT-4, I can assist you with **in-depth analysis** and **benchmarking** of annual reports of some of the world's leading tech giants:\n- **Meta**\n- **Amazon**\n- **Alphabet**\n- **Apple**\n- **Microsoft**,\n\nfor the years **2022, 2021, and 2020**.\n\nWhether you are comparing financial performances, exploring trends, or seeking detailed insights across different companies and years, I transform complex data into actionable knowledge. Unlock the power of informed decision-making today with me!'''


    # with st.sidebar:
        # st.error('**Ben- Form 10K  x  Benchmarking Agent**')
        # st.image(Image.open('BenLogo.png'))
        # st.warning(intoductory_message)

    with st.sidebar:
    # st.title("Characters")
    # with st.sidebar.container():
        path1 = os.path.dirname(__file__)
        image_path = path1+'/logo.jpeg'
        image = Image.open(image_path)
        # image = image.resize((25, 25))

        st.image(image, use_column_width=True)
        sidebar_title = '<h2 style="font-family:sans-serif; text-align: center;">Build & Developed <br> By HiDevs Community</h2>'
        st.markdown(sidebar_title, unsafe_allow_html=True)

        
        openai_api_key = st.text_input("OpenAI API Key", key="openai_api_key", type="password")
        

    if openai_api_key.startswith('sk-'):
        @st.cache_resource
        def preparing_benchmarking_agent():
            # Initialize embeddings and chat models
            embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
            llm = ChatOpenAI(temperature=0, model="gpt-4", streaming=True, openai_api_key=openai_api_key)

            # Load local FAISS document stores for multiple companies and years
            apple_2022_docs_store = FAISS.load_local(r'/home/user/app/repo_directory/hugging_spaces/TechGiantReportGuru/data/datastores/apple_2022', embeddings)
            apple_2021_docs_store = FAISS.load_local(r'/home/user/app/repo_directory/hugging_spaces/TechGiantReportGuru/data/datastores/apple_2021', embeddings)
            apple_2020_docs_store = FAISS.load_local(r'/home/user/app/repo_directory/hugging_spaces/TechGiantReportGuru/data/datastores/apple_2020', embeddings)
        
            microsoft_2022_docs_store = FAISS.load_local(r'/home/user/app/repo_directory/hugging_spaces/TechGiantReportGuru/data/datastores/msft_2022', embeddings)
            microsoft_2021_docs_store = FAISS.load_local(r'/home/user/app/repo_directory/hugging_spaces/TechGiantReportGuru/data/datastores/msft_2021', embeddings)
            microsoft_2020_docs_store = FAISS.load_local(r'/home/user/app/repo_directory/hugging_spaces/TechGiantReportGuru/data/datastores/msft_2020', embeddings)


            amazon_2022_docs_store = FAISS.load_local(r'/home/user/app/repo_directory/hugging_spaces/TechGiantReportGuru/data/datastores/amzn_2022', embeddings)
            amazon_2021_docs_store = FAISS.load_local(r'/home/user/app/repo_directory/hugging_spaces/TechGiantReportGuru/data/datastores/amzn_2021', embeddings)
            amazon_2020_docs_store = FAISS.load_local(r'/home/user/app/repo_directory/hugging_spaces/TechGiantReportGuru/data/datastores/amzn_2020', embeddings)


            alphabet_2022_docs_store = FAISS.load_local(r'/home/user/app/repo_directory/hugging_spaces/TechGiantReportGuru/data/datastores/alphbt_2022', embeddings)
            alphabet_2021_docs_store = FAISS.load_local(r'/home/user/app/repo_directory/hugging_spaces/TechGiantReportGuru/data/datastores/alphbt_2021', embeddings)
            alphabet_2020_docs_store = FAISS.load_local(r'/home/user/app/repo_directory/hugging_spaces/TechGiantReportGuru/data/datastores/alphbt_2020', embeddings)


            meta_2022_docs_store = FAISS.load_local(r'/home/user/app/repo_directory/hugging_spaces/TechGiantReportGuru/data/datastores/meta_2022', embeddings)
            meta_2021_docs_store = FAISS.load_local(r'/home/user/app/repo_directory/hugging_spaces/TechGiantReportGuru/data/datastores/meta_2021', embeddings)
            meta_2020_docs_store = FAISS.load_local(r'/home/user/app/repo_directory/hugging_spaces/TechGiantReportGuru/data/datastores/meta_2020', embeddings)

            # Create QA retrieval chains for various companies and years
            apple_2022_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=apple_2022_docs_store.as_retriever(search_kwargs={'k':5}))
            apple_2021_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=apple_2021_docs_store.as_retriever(search_kwargs={'k':5}))
            apple_2020_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=apple_2020_docs_store.as_retriever(search_kwargs={'k':5}))


            microsoft_2022_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=microsoft_2022_docs_store.as_retriever(search_kwargs={'k':5}))
            microsoft_2021_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=microsoft_2021_docs_store.as_retriever(search_kwargs={'k':5}))
            microsoft_2020_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=microsoft_2020_docs_store.as_retriever(search_kwargs={'k':5}))


            amazon_2022_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=amazon_2022_docs_store.as_retriever(search_kwargs={'k':5}))
            amazon_2021_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=amazon_2021_docs_store.as_retriever(search_kwargs={'k':5}))
            amazon_2020_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=amazon_2020_docs_store.as_retriever(search_kwargs={'k':5}))


            meta_2022_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=meta_2022_docs_store.as_retriever(search_kwargs={'k':5}))
            meta_2021_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=meta_2021_docs_store.as_retriever(search_kwargs={'k':5}))
            meta_2020_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=meta_2020_docs_store.as_retriever(search_kwargs={'k':5}))


            alphabet_2022_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=alphabet_2022_docs_store.as_retriever(search_kwargs={'k':5}))
            alphabet_2021_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=alphabet_2021_docs_store.as_retriever(search_kwargs={'k':5}))
            alphabet_2020_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=alphabet_2020_docs_store.as_retriever(search_kwargs={'k':5}))

            # Define the tools (queries against different document stores)
            tools = [
                Tool(
                    name="Apple Form 10K 2022",
                    func=apple_2022_qa.run,
                    description="useful when you need to answer from Apple 2022",
                ),
                Tool(
                    name="Apple Form 10K 2021",
                    func=apple_2021_qa.run,
                    description="useful when you need to answer from Apple 2021",
                ),
                Tool(
                    name="Apple Form 10K 2020",
                    func=apple_2020_qa.run,
                    description="useful when you need to answer from Apple 2020",
                ),
                Tool(
                    name="Microsoft Form 10K 2022",
                    func=microsoft_2022_qa.run,
                    description="useful when you need to answer from Microsoft 2022",
                ),
                Tool(
                    name="Microsoft Form 10K 2021",
                    func=microsoft_2021_qa.run,
                    description="useful when you need to answer from Microsoft 2021",
                ),
                Tool(
                    name="Microsoft Form 10K 2020",
                    func=microsoft_2020_qa.run,
                    description="useful when you need to answer from Microsoft 2020",
                ),
                Tool(
                    name="Meta Form 10K 2022",
                    func=meta_2022_qa.run,
                    description="useful when you need to answer from Meta 2022",
                ),
                Tool(
                    name="Meta Form 10K 2021",
                    func=meta_2021_qa.run,
                    description="useful when you need to answer from Meta 2021",
                ),
                Tool(
                    name="Meta Form 10K 2020",
                    func=meta_2020_qa.run,
                    description="useful when you need to answer from Meta 2020",
                ),
                Tool(
                    name="Alphabet Form 10K 2022",
                    func=alphabet_2022_qa.run,
                    description="useful when you need to answer from Alphabet or Google 2022",
                ),
                Tool(
                    name="Alphabet Form 10K 2021",
                    func=alphabet_2021_qa.run,
                    description="useful when you need to answer from Alphabet or Google 2021",
                ),
                Tool(
                    name="Alphabet Form 10K 2020",
                    func=alphabet_2020_qa.run,
                    description="useful when you need to answer from Alphabet or Google 2020",
                ),
                Tool(
                    name="Amazon Form 10K 2022",
                    func=amazon_2022_qa.run,
                    description="useful when you need to answer from Amazon 2022",
                ),
                Tool(
                    name="Amazon Form 10K 2021",
                    func=amazon_2021_qa.run,
                    description="useful when you need to answer from Amazon 2021",
                ),
                Tool(
                    name="Amazon Form 10K 2020",
                    func=amazon_2020_qa.run,
                    description="useful when you need to answer from Amazon 2020",
                ),
            ]


            # Construct the agent. We will use the default agent type here.
            # See documentation for a full list of options.
            return initialize_agent(
                tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
            )

        # Initialize the agent
        agent = preparing_benchmarking_agent()

        # Session state to manage user messages
        if "messages" not in st.session_state:
            st.session_state["messages"] = []


        sample_question_1 = '''What is the net sales of Apple in 2022?'''
        sample_question_2 = '''What are some of the risk factors Microsoft reported in 2021?'''
        sample_question_3 = '''Give me the Apple's breakdown of net sales by products and services.'''
        sample_question_4 = '''Compare the revenue of Apple, Meta, Microsoft for the year 2022. Present your response in table with columns Revenue, Apple 2022, Meta 2022, Microsoft 2022.'''
        sample_question_5 = '''Compare the risk factors of Microsoft and Alphabet for 2021. Present your response in a table with columns "Risk Category", "Risk Details - Microsoft", "Risk Details - Alphabet"'''
        sample_question_6 = '''Compare the covid-19 impact on Apple in 2020, 2021 and 2022? Present your response in table with columns "Impact category", "Key Details-2020", "Key Details-2021, "Key Details-2022", "Changes/Conclusion"'''

        with st.chat_message("assistant"):
            st.write("Hello, Tech Giant Report Guru")
            # st.image(Image.open('BenLogo.png'))
            # st.write(intoductory_message)
            st.write(f'''Ready to dive in? Here are your starting queries:\n\n🎯 **Basic queries:**''')
            st.info(sample_question_1)
            st.info(sample_question_2)
            st.info(sample_question_3)
            st.write(f'''🎯 **Complex & Benchmarking Queries:**''')
            st.info(sample_question_5)
            st.info(sample_question_6)

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
            
        if prompt := st.chat_input(placeholder="What is the net sales of Apple in 2022?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            with st.chat_message("assistant"):
                st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
                response = agent.run(prompt, callbacks=[st_cb])
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.success(response)
