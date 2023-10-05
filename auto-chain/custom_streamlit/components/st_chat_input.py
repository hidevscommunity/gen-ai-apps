import streamlit as st
from custom_streamlit.functions import func_handle_chat_input,func_stop_generating
def submitted():
     st.session_state.execute["current_id"]+=1
     new_id = st.session_state.execute["current_id"]
     st.session_state.execute["ids"][new_id] = ({
                    "type":"Ready"
     })
def st_chat_input():     
        disabled = st.session_state['executing']
        if disabled:
             st.markdown('<span id = "button-after"></span>',unsafe_allow_html=True)
             st.button('Stop Generating',type="primary",on_click=func_stop_generating)
        user_question = st.chat_input("Ask a question about your documents:",disabled=disabled,key='chat-enabled',on_submit=submitted)    
        #submitted()
        #user_question = 'Hello'
        if user_question and st.session_state['execute']["ids"][st.session_state['execute']["current_id"]]["type"]=="Ready":
            st.markdown('<span id = "button-after"></span>',unsafe_allow_html=True)
            st.button('Stop Generating',type="primary",on_click=func_stop_generating)
            st.chat_input("Ask a question about your documents:",disabled=True,key='chat-disabled') 
            func_handle_chat_input(user_question)      
            st.experimental_rerun()
           
            