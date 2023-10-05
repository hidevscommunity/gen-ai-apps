# Import libraries
from datetime import datetime
import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain import PromptTemplate
from bot import Bot

# Initialize a list to store character objects
if "bots" not in st.session_state:
    st.session_state.bots = []

# Function to add a new character
def add_bot(name, relationship, human_name, common_phrases, speaking_style, important_memories, other_background):
    new_bot = Bot(name, relationship, human_name, common_phrases, speaking_style, important_memories, other_background, datetime.now(), [])
    st.session_state.bots.append(new_bot)
    return new_bot

with st.sidebar:
    # st.title("Characters")
    openai_api_key = st.text_input("OpenAI API Key", key="openai_api_key", type="password")
    
    # Display a list of characters sorted by last talked date
    bot_names = [bot.get_bot_name() for bot in st.session_state.bots]
    bot_name = st.sidebar.selectbox("Select Character", bot_names)
    bot = None
    for b in st.session_state.bots:
        if b.get_bot_name() == bot_name:
            bot = b
            break
        
    if st.sidebar.button("Add New Character"):
        st.session_state.show_form = True
        
    if st.session_state.get("show_form", False):
        # Show a form to collect character details
        st.subheader("Add a New Character")
        name = st.text_input("Character's Name")
        relationship = st.text_input("Your Relationship with the Character")
        human_name = st.text_input("Character's Nickname for You")
        common_phrases = st.text_input("Common Phrases")
        speaking_style = st.text_input("Speaking Style")
        important_memories = st.text_area("Important Memories")
        other_background = st.text_area("Other Background")
        
        # Check if the user has filled in the required fields
        if st.button("Submit Character"):
            if name and relationship:
                bot = add_bot(name, relationship, human_name, common_phrases, speaking_style, important_memories, other_background)
                st.session_state.show_form = False
                st.session_state.bot_added = True
    
    if st.session_state.get("bot_added", False):
        # Reset the bot_added state to refresh the sidebar
        st.session_state.bot_added = False
        # Use this trick to refresh the sidebar
        st.experimental_rerun()
        
    print(st.session_state.bots) 

if bot:
    st.title(f"Chat with {bot.get_bot_name()}")
    st.session_state.messages = bot.get_chat_history()
    if "history" not in st.session_state:
        st.session_state.history = ConversationBufferMemory(human_prefix=bot.get_human_name(), ai_prefix=bot.get_bot_name())

    # Create a button to clear chat history
    def clear_chat_history():
        st.session_state.messages = []
        bot.save_chat_history([])
    if st.button("Clear Chat History"):
        clear_chat_history()
        
    # Create a PromptTemplate with input variables
    template = f"""
    [Character Settings]{bot.consolidated_info()}

    Current conversation:
    {{history}}
    {bot.human_name}: {{input}}
    {bot.bot_name}:"""

    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=template,
    )

    # Create LLM & Conversation Chain
    if openai_api_key:
        # Create LLM model
        llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

        # Create the ConversationChain object with the specified configuration
        conversation = ConversationChain(
            prompt=prompt,
            llm=llm,
            memory=st.session_state['history']
        )
        
        # Load previous chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
            
        # Print user input and LLM reply
        if user_input := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            response = conversation.predict(input=user_input)
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        # Save messages in the characters
        bot.save_chat_history(st.session_state.messages)
        print(bot.chat_history)
    else:
        st.warning('OpenAI API key required to test this app.')