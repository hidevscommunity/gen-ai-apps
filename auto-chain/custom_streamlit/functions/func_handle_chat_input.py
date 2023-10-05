import streamlit as st
from utils.session_state import *
from custom_streamlit.functions import func_delete_messages,func_stop_generating,func_sources_buttons
from models.execute import execute
def func_handle_chat_input(user_question):

    if st.session_state['executing']==True:   
        st.session_state['executing']=False
        return
    with st.chat_message("user"):
        col1,col2 = st.columns([11,1])
        with col1:
            st.markdown(f'{user_question}',unsafe_allow_html=True)
        with col2:
            st.button('🗑',type="primary",on_click=func_delete_messages,args=(len(messages_session_state()),))

    messages_session_state().append({"role": "user", "content": user_question})
    messages_session_state().append({"role": "assistant", "content": "","disliked":False})
    
    with st.chat_message("assistant"):
        id = st.session_state['execute']["current_id"]
        st.session_state['execute']["ids"][id]["type"] = "Started"
        st.session_state['executing'] = True
        executed = execute(user_question = user_question)
        if(executed):
            st.session_state['executing'] = False  
            st.session_state['execute']["ids"][id]["type"] = "Ended" 
            
        #if "source_documents" in messages_session_state()[-1]:
        #    func_sources_buttons(3,messages_session_state()[-1]["source_documents"])
                  

                
                
                   
                


