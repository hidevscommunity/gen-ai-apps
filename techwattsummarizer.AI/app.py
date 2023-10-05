import os
from youtube_transcript_api import YouTubeTranscriptApi as yta
from langchain.llms import OpenAI
from langchain.chains import LLMChain 
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain.memory import ConversationBufferMemory
import streamlit as st
import openai
from bs4 import BeautifulSoup
import requests



key = st.secrets['key']
os.environ['OPENAI_API_KEY'] = key
llm = OpenAI(temperature=0.6)
memory = ConversationBufferMemory(input_key='transcript',memory_key='chat history')

global options

with st.sidebar:
    st.image('LOGO.png')
    st.title('TechWatt.AI')
    options = st.radio('OPTIONS',['🦜️🔗YOUTUBE','🦜️🔗WEBSITE'])
    
st.title('🦜️🔗 TechWatt Summarizer🦜️🔗')

try:
    if options == '🦜️🔗YOUTUBE':
        st.title('Youtube Transcript Summarizer')
        prompt = st.text_input(label='Enter link of a Youtube video',)
        if prompt:
            expander = st.expander('Main Youtube Transcript')
            id = prompt.split('/')
            vid_id = id[-1]
            data = yta.get_transcript(vid_id)
            final_data = ''
            for val in data:
                for key, value in val.items():
                    if key == 'text':
                        final_data += value
            processed_data = final_data.splitlines()
            clean_data = ' '.join(processed_data)


            clean_template = PromptTemplate(
            input_variables=['transcript'],
            template = 'Correct all errors in this Youtube {transcript} accurately.'
            )

            main_template = PromptTemplate(
            input_variables=['Correct'],
            template ='List the mainpoints in this given Youtube transcript {Correct} begin each mainpoint with asterish or emoji and not numbers'

            )

            clean_chain = LLMChain(llm=llm,prompt=clean_template, output_key='Correct',memory=memory)
            main_chain = LLMChain(llm=llm,prompt=main_template, output_key='mainpoints',memory=memory)


            country_chain = SequentialChain(
                chains=[clean_chain,main_chain],
                input_variables =['transcript'],
                output_variables = ['Correct','mainpoints']
                )        


            result = country_chain({'transcript':clean_data})
            summary = result['Correct']
            mainpoints = result['mainpoints']
            expander.write(clean_data)
            st.title('Summary')
            st.write(summary)
            st.title('Main Points')
            st.write(mainpoints)
            with st.expander('Chat History'):
                st.info(memory.buffer)
            
    

except Exception as e:
    st.write('Video length too long try a short video')
    st.write(e)


try:
    if options == '🦜️🔗WEBSITE':
        st.title('Website Summarizer')
        prompt = st.text_input(label='Enter link of a website',)
        if prompt:
            expander = st.expander('Main Website Text')
            response = requests.get(prompt)
            soup = BeautifulSoup(response.content, "html.parser")
            paragraphs = soup.find_all("p")
            text = ''
            for paragraph in paragraphs:
                text += paragraph.get_text()
            
            

            summary_template = PromptTemplate(
            input_variables=['transcript'],
            template = 'summarize this {transcript} and remove all unnecessary data from it'
            )

            mainpoints_template = PromptTemplate(
            input_variables=['summarize'],
            template ='List the mainpoints in this {summarize} for me.'

            )

            summary_chain = LLMChain(llm=llm,prompt=summary_template, output_key='summarize',memory=memory)
            mainpoints_chain = LLMChain(llm=llm,prompt=mainpoints_template, output_key='mainpoints',memory=memory)


            country_chain = SequentialChain(
                chains=[summary_chain,mainpoints_chain],
                input_variables =['transcript'],
                output_variables = ['summarize','mainpoints']
                )        


            result = country_chain({'transcript':text})
            summary = result['summarize']
            mainpoints = result['mainpoints']
            expander.write(text)
            st.title('Summary')
            st.write(summary)
            st.title('Main Points')
            st.write(mainpoints)
            
            with st.expander('Chat History'):
                st.info(memory.buffer)
            
except Exception as e:
    st.write('Article too long try with short article')

