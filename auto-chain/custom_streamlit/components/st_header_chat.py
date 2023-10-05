import streamlit as st
from custom_streamlit.functions import func_toggle_thought_process,func_reset_messages
from annotated_text import annotated_text,annotation

def st_header_chat(header,option):
    with header:
            col1,col2,col3,col4 = st.columns([9,1,1,1])
            with col1:
                annotated_text(
                    annotation(f"""{option}""",background="transparent",fontSize="28px",fontWeight="bold"),
                ) 
            with col2:
                if(st.session_state["show_thought_process"]):
                    type = 'primary'
                else:
                    type = 'secondary' 
                
                st.button('💡',type=type,use_container_width=True,on_click=func_toggle_thought_process)
            with col3:
                
                st.button('↺',type="primary",use_container_width=True,on_click=func_reset_messages)
            with col4:
                pass