import streamlit as st
import ast
from public import tpl_bot, tpl_user

from .audio import handle_text_2_speech


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    chat_history_list = response['chat_history']

    # Extract content from each message object
    for i, message in enumerate(chat_history_list):
        st.session_state.chat_history.insert(i, message.content)
    # only keep the latest 12 chat history
    if len(st.session_state.chat_history) >= 12:
        st.session_state.chat_history = st.session_state.chat_history[:-2]

    chat_history = st.session_state.chat_history
    print(f"length of chat_history is {len(chat_history)}")
    for i, message in enumerate(chat_history):
        if i % 2 == 0:  # User's message 
            print(f'User question is {message}')
            st.write(
                tpl_user.replace(
                    '{{MSG}}', message,
                ), unsafe_allow_html=True,
            )
        else:  # AI message
            st.write(
                tpl_bot.replace(
                    '{{MSG}}', message,
                ), unsafe_allow_html=True,
            )

#    if len(chat_history) > 0:
#        handle_text_2_speech(chat_history[-1].content)
