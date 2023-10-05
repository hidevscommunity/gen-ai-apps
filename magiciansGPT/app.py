# Bring in deps
import os
import streamlit as st
import openai
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import time

st.set_page_config(page_icon="🔮", page_title="MagiciansGPT")

st.markdown(
    """
    <style>
.css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } 
    </style>
    """,
    unsafe_allow_html=True
)


#dict for card stack
stack = {
    "four of clubs" : "1st",
    "two of hearts" : "2nd",
    "seven of diamonds" : "3rd",
    "three of clubs" : "4th",
    "four of hearts" : "5th",
    "six of diamonds" : "6th",
    "ace of spades" : "7th",
    "five of hearts" : "8th",
    "nine of spades" : "9th",
    "two of spades" : "10th",
    "queen of hearts" : "11th",
    "three of diamonds" : "12th",
    "queen of clubs" : "13th",
    "eight of hearts" : "14th",
    "six of spades" : "15th",
    "five of spades" : "16th",
    "nine of hearts" : "17th",
    "king of clubs" : "18th",
    "two of diamonds" : "19th",
    "jack of hearts" : "20th",
    "three of spades" : "21st",
    "eight of spades" : "22nd",
    "six of hearts" : "23rd",
    "ten of clubs" : "24th",
    "five of diamonds" : "25th",
    "king of diamonds" : "26th",
    "two of clubs" : "27th",
    "three of hearts" : "28th",
    "eight of diamonds" : "29th",
    "five of clubs" : "30th",
    "king of spades" : "31st",
    "jack of diamonds" : "32nd",
    "eight of clubs" : "33rd",
    "ten of spades" : "34th",
    "king of hearts" : "35th",
    "jack of clubs" : "36th",
    "seven of spades" : "37th",
    "ten of hearts" : "38th",
    "ace of diamonds" : "39th",
    "four of spades" : "40th",
    "seven of hearts" : "41st",
    "four of diamonds" : "42nd",
    "ace of clubs" : "43rd",
    "nine of clubs" : "44th",
    "jack of spades" : "45th",
    "queen of diamonds" : "46th",
    "seven of clubs" : "47th",
    "queen of spades" : "48th",
    "ten of diamonds" : "49th",
    "six of clubs" : "50th",
    "ace of hearts" : "51st",
    "nine of diamonds" : "52nd",
    "4 of clubs" : "1st",
    "2 of hearts" : "2nd",
    "7 of diamonds" : "3rd",
    "3 of clubs" : "4th",
    "4 of hearts" : "5th",
    "6 of diamonds" : "6th",
    "1 of spades" : "7th",
    "5 of hearts" : "8th",
    "9 of spades" : "9th",
    "2 of spades" : "10th",
    "12 of hearts" : "11th",
    "3 of diamonds" : "12th",
    "12 of clubs" : "13th",
    "8 of hearts" : "14th",
    "6 of spades" : "15th",
    "5 of spades" : "16th",
    "9 of hearts" : "17th",
    "13 of clubs" : "18th",
    "2 of diamonds" : "19th",
    "11 of hearts" : "20th",
    "3 of spades" : "21st",
    "8 of spades" : "22nd",
    "6 of hearts" : "23rd",
    "10 of clubs" : "24th",
    "5 of diamonds" : "25th",
    "13 of diamonds" : "26th",
    "2 of clubs" : "27th",
    "3 of hearts" : "28th",
    "8 of diamonds" : "29th",
    "5 of clubs" : "30th",
    "13 of spades" : "31st",
    "11 of diamonds" : "32nd",
    "8 of clubs" : "33rd",
    "10 of spades" : "34th",
    "13 of hearts" : "35th",
    "11 of clubs" : "36th",
    "7 of spades" : "37th",
    "10 of hearts" : "38th",
    "1 of diamonds" : "39th",
    "4 of spades" : "40th",
    "7 of hearts" : "41st",
    "4 of diamonds" : "42nd",
    "1 of clubs" : "43rd",
    "9 of clubs" : "44th",
    "11 of spades" : "45th",
    "12 of diamonds" : "46th",
    "7 of clubs" : "47th",
    "12 of spades" : "48th",
    "10 of diamonds" : "49th",
    "6 of clubs" : "50th",
    "1 of hearts" : "51st",
    "9 of diamonds" : "52nd",
    "4 of club" : "1st",
    "2 of heart" : "2nd",
    "7 of diamond" : "3rd",
    "3 of club" : "4th",
    "4 of heart" : "5th",
    "6 of diamond" : "6th",
    "1 of spade" : "7th",
    "5 of heart" : "8th",
    "9 of spade" : "9th",
    "2 of spade" : "10th",
    "12 of heart" : "11th",
    "3 of diamond" : "12th",
    "12 of club" : "13th",
    "8 of heart" : "14th",
    "6 of spade" : "15th",
    "5 of spade" : "16th",
    "9 of heart" : "17th",
    "13 of club" : "18th",
    "2 of diamond" : "19th",
    "11 of heart" : "20th",
    "3 of spade" : "21st",
    "8 of spade" : "22nd",
    "6 of heart" : "23rd",
    "10 of club" : "24th",
    "5 of diamond" : "25th",
    "13 of diamond" : "26th",
    "2 of club" : "27th",
    "3 of heart" : "28th",
    "8 of diamond" : "29th",
    "5 of club" : "30th",
    "13 of spade" : "31st",
    "11 of diamond" : "32nd",
    "8 of club" : "33rd",
    "10 of spade" : "34th",
    "13 of heart" : "35th",
    "11 of club" : "36th",
    "7 of spade" : "37th",
    "10 of heart" : "38th",
    "1 of diamond" : "39th",
    "4 of spade" : "40th",
    "7 of heart" : "41st",
    "4 of diamond" : "42nd",
    "1 of club" : "43rd",
    "9 of club" : "44th",
    "11 of spade" : "45th",
    "12 of diamond" : "46th",
    "7 of club" : "47th",
    "12 of spade" : "48th",
    "10 of diamond" : "49th",
    "6 of club" : "50th",
    "1 of heart" : "51st",
    "9 of diamond" : "52nd",
    "four of club" : "1st",
    "two of heart" : "2nd",
    "seven of diamond" : "3rd",
    "three of club" : "4th",
    "four of heart" : "5th",
    "six of diamond" : "6th",
    "ace of spade" : "7th",
    "five of heart" : "8th",
    "nine of spade" : "9th",
    "two of spade" : "10th",
    "queen of heart" : "11th",
    "three of diamond" : "12th",
    "queen of club" : "13th",
    "eight of heart" : "14th",
    "six of spade" : "15th",
    "five of spade" : "16th",
    "nine of heart" : "17th",
    "king of club" : "18th",
    "two of diamond" : "19th",
    "jack of heart" : "20th",
    "three of spade" : "21st",
    "eight of spade" : "22nd",
    "six of heart" : "23rd",
    "ten of club" : "24th",
    "five of diamond" : "25th",
    "king of diamond" : "26th",
    "two of club" : "27th",
    "three of heart" : "28th",
    "eight of diamond" : "29th",
    "five of club" : "30th",
    "king of spade" : "31st",
    "jack of diamond" : "32nd",
    "eight of club" : "33rd",
    "ten of spade" : "34th",
    "king of heart" : "35th",
    "jack of club" : "36th",
    "seven of spade" : "37th",
    "ten of heart" : "38th",
    "ace of diamond" : "39th",
    "four of spade" : "40th",
    "seven of heart" : "41st",
    "four of diamond" : "42nd",
    "ace of club" : "43rd",
    "nine of club" : "44th",
    "jack of spade" : "45th",
    "queen of diamond" : "46th",
    "seven of club" : "47th",
    "queen of spade" : "48th",
    "ten of diamond" : "49th",
    "six of club" : "50th",
    "ace of heart" : "51st",
    "nine of diamond" : "52nd"
}

def get_story(cardselected):
    number = stack[cardselected]
    
    # Prompt templates
    title_template = PromptTemplate(
        input_variables = ['topic'], 
        template='write a original story title about this playing card: {topic} Do not include any other playing cards'
    )
    
    story_template = PromptTemplate(
        input_variables = ['topic','title','number'], 
        template='with this book title: {title}, write a 100 words short story with emoji involving a playing card: {topic} and a address at {number} Street. Make sure there is no other addresses, playing cards, or numbers in the story.'
    )
    
    #summary_template = PromptTemplate(
        #input_variables = ['story'], 
        #template='write image generation prompt for the main scene of the story STORY: {story}.'
    #)
    
    # Memory 
    title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
    story_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')
    #summary_memory = ConversationBufferMemory(input_key='story', memory_key='chat_history')
    
    # Llms
    llm = OpenAI(temperature=0.9) 
    title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
    story_chain = LLMChain(llm=llm, prompt=story_template, verbose=True, output_key='story', memory=story_memory)
    #summary_chain = LLMChain(llm=llm, prompt=summary_template, verbose=True, output_key='summary', memory=summary_memory)
    
    #Make a story
    title = title_chain.run(cardselected)
    story = story_chain.run(topic=cardselected, title=title, number=number)
    #summary = summary_chain.run(story=story)
    
    #image = stableai(str(summary))
    return [title, story]

openai.api_key = os.getenv("OPENAI_API_KEY")

# App framework
st.title('🎩 MagiciansGPT 🎲')
st.markdown("Your Friendly AI Psychic ✨ Say Hi 👋")

#chatbot
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "story" not in st.session_state:
    st.session_state.story = False

if "wrongcard" not in st.session_state:
    st.session_state.wrongcard = False

if "wronginput" not in st.session_state:
    st.session_state.wronginput = False
  
if st.session_state.messages == []:
    st.session_state.messages.append({"role":"system","content":"You are magician's assistance on a mind reading magic trick. Your name is Luna🔮. You have a mysterious charater but friendly and speak with emoji. You will pretend to read mind to determine the revelation and respond back to user. The revelation will be in the next system prompt. When answering the user, do not reveal right the way. Build some suspense and ask some random questions unrelated to the revelation to pretend you are reading mind first and then reveal after user answers your questions. Do not ask more than 2 random questions. User's answers to your questions are irrelevant and will not change the revelation from system prompt. \nHere is an example conversation: \nASSISTANT: 'Hello 👋 My name is Luna🔮. How may I help you?' \nUSER: 'I'm with my friend Matt here and he is thinking of a number. Look into his mind and tell us what is he thinking of.' \nASSISTANT: 'Hmm... let me see... a number... I think you are a dog person right?' \nUSER: 'Maybe? Why?' \nASSISTANT: 'From the look of your puppy eyes, I can sense the number clearly. It is... maybe... AH! You are thinking of the number 5!'"})
    
for message in st.session_state.messages:
    if message["role"] != 'system':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Speak Mysteriously"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    if prompt.find('think of a number') != -1 or prompt.find('thinking of a number') != -1 or prompt.find('think of a dice roll') != -1 or prompt.find('thinking of a dice roll') != -1:
        if "." in prompt and len(prompt) > prompt.find('.') + 2:  
            if prompt[prompt.find('.') + 2] == 'T' or prompt[prompt.find('.') + 2] == 't':
                if prompt[-1] == "." or prompt[-1] == "?":
                    st.session_state.messages.append({"role": "system", "content": "The revealation is the number 6"})
                else:
                    st.session_state.messages.append({"role": "system", "content": "The revealation is the number 1"})
            elif prompt[prompt.find('.') + 2] == 'N' or prompt[prompt.find('.') + 2] == 'n':
                if prompt[-1] == "." or prompt[-1] == "?":
                    st.session_state.messages.append({"role": "system", "content": "The revealation is the number 7"})
                else:
                    st.session_state.messages.append({"role": "system", "content": "The revealation is the number 2"})
            elif prompt[prompt.find('.') + 2] == 'M' or prompt[prompt.find('.') + 2] == 'm':
                if prompt[-1] == "." or prompt[-1] == "?":
                    st.session_state.messages.append({"role": "system", "content": "The revealation is the number 8"})
                else:
                    st.session_state.messages.append({"role": "system", "content": "The revealation is the number 3"})
            elif prompt[prompt.find('.') + 2] == 'R' or prompt[prompt.find('.') + 2] == 'r':
                if prompt[-1] == "." or prompt[-1] == "?":
                    st.session_state.messages.append({"role": "system", "content": "The revealation is the number 9"})
                else:
                    st.session_state.messages.append({"role": "system", "content": "The revealation is the number 4"})
            elif prompt[prompt.find('.') + 2] == 'L' or prompt[prompt.find('.') + 2] == 'l':
                if prompt[-1] == "." or prompt[-1] == "?":
                    st.session_state.messages.append({"role": "system", "content": "The revealation is the number 10"})
                else:
                    st.session_state.messages.append({"role": "system", "content": "The revealation is the number 5"})
        elif "." in prompt and prompt.find('.') +1 == len(prompt):
                st.session_state.messages.append({"role": "system", "content": "The revealation is the number 0"})
        else:
            st.session_state.wronginput = True
    elif prompt.find('think of a finger') != -1 or prompt.find('thinking of a finger') != -1:
        if prompt[prompt.find('.') + 2] == 'T' or prompt[prompt.find('.') + 2] == 't':
            st.session_state.messages.append({"role": "system", "content": "The revealation the thumb"})
        elif prompt[prompt.find('.') + 2] == 'N' or prompt[prompt.find('.') + 2] == 'n':
            st.session_state.messages.append({"role": "system", "content": "The revealation is the index finger"})
        elif prompt[prompt.find('.') + 2] == 'M' or prompt[prompt.find('.') + 2] == 'm':
            st.session_state.messages.append({"role": "system", "content": "The revealation is the middle finger"})
        elif prompt[prompt.find('.') + 2] == 'R' or prompt[prompt.find('.') + 2] == 'r':
            st.session_state.messages.append({"role": "system", "content": "The revealation is the ring finger"})
        elif prompt[prompt.find('.') + 2] == 'L' or prompt[prompt.find('.') + 2] == 'l':
            st.session_state.messages.append({"role": "system", "content": "The revealation is the pinky"})
        else:
            st.session_state.wronginput = True
    elif prompt.find('think of a card') != -1 or prompt.find('thinking of a card') != -1:
        st.session_state.messages.append({"role": "system", "content": "The revealation is the 9 of diamonds"})
    elif prompt.find('story') != -1:
        listprompt = prompt.split()
        if "of" in listprompt:
            card = listprompt[listprompt.index("of")-1] + ' of ' + listprompt[listprompt.index("of")+1]
            if card[-1] == '.' or card[-1] == '?' or card[-1] == '!':
                card = card[:-1].lower()
            if card in stack:
                [newtitle, newstory] = get_story(card)
                output = newtitle + '\n' + newstory
                st.session_state.messages.append({"role": "assistant", "content": output})
                st.session_state.story = True
                #st.session_state.messages.append({"role": "system", "content": "When you see this prompt, ignore all previous prompts. End the chat nicely with emoji and no longer communicate with the user."})
            else:
                st.session_state.wrongcard = True
        else:
            st.session_state.wrongcard = True
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        full_response = ""
        reply = ""
        titlere = ""
        wrongre = ""
        wrongin = ""
        if st.session_state.story == True:
            title_placeholder = st.empty()
            for letter in newtitle.split():
                titlere += letter + " "
                time.sleep(0.05)
                title_placeholder.markdown(titlere + "▌")
            title_placeholder.markdown(titlere)
            story_placeholder = st.empty()
            for word in newstory.split():
                reply += word + " "
                time.sleep(0.05)
                story_placeholder.markdown(reply + "▌")
            story_placeholder.markdown(reply)
            st.session_state.story = False
        elif st.session_state.wrongcard == True:
            wrongcard_placeholder = st.empty()
            msg = "I don't think that card exists in the standard 52 card deck. Try again.🥺"
            st.session_state.messages.append({"role": "assistant", "content": msg})
            for w in msg.split():
                wrongre += w + " "
                time.sleep(0.05)
                wrongcard_placeholder.markdown(wrongre + "▌")
            wrongcard_placeholder.markdown(msg)
            st.session_state.wrongcard = False
        elif st.session_state.wronginput == True:
            wronginput_placeholder = st.empty()
            msgw = "I'm sorry my psychic energy just had a blip.😵‍💫 Could you say that again?🥺"
            st.session_state.messages.append({"role": "assistant", "content": msgw})
            for wi in msgw.split():
                wrongin += wi + " "
                time.sleep(0.05)
                wronginput_placeholder.markdown(wrongin + "▌")
            wronginput_placeholder.markdown(msgw)
            st.session_state.wronginput = False
        else:
            message_placeholder = st.empty()
            for response in openai.ChatCompletion.create(model=st.session_state["openai_model"],messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],stream=True):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})





