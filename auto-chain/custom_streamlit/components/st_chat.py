import streamlit as st

from utils.session_state import messages_session_state,executor_session_state
from custom_streamlit.functions import func_delete_messages,func_sources_buttons
from utils.multi_modal import st_multi_modal

def st_chat():
    for i,message in enumerate(messages_session_state()):
        with st.chat_message(message["role"]):

            col1,col2 = st.columns([11,1])
            with col1:
                placeholder = st.container()
                st_multi_modal(placeholder,message["content"],[])
            with col2:
                if(message["role"] == "user"):
                    st.button('🗑',type="primary",key=f"b{i}",on_click=func_delete_messages,args=(i,))
                else:
                    dislike = st.empty()
                    if(not message['disliked']):
                        if dislike.button('👎',key=f"d{i}"):
                            dislike.button('👎',type='primary',key=f"d{i}-active")
                            messages_session_state()[i]['disliked'] = True
                            
                    else:
                        
                        if dislike.button('👎',key=f"d{i}-active",type='primary'):
                            dislike.button('👎',key=f"d{i}")
                            messages_session_state()[i]['disliked'] = False
            if(st.session_state.show_thought_process):
                if(message['role']=='assistant'):
                    with st.expander('Thought Process'):
                        st.write(message['thought_process'])        
                        
            
            if "source_documents" in message:
                func_sources_buttons(3,message["source_documents"])