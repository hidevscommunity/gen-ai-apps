import streamlit as st
from utils.session_state import load_session_state,reset_session_state
from utils.conversation_chain import get_conversation_chain
from firebase.service import load
from utils.helpers import remove_dir
def func_handle_url(model_id):
    if(st.session_state.url["clicked"] and st.session_state.url["path"]!=""):
        st.session_state.url["clicked"] = False
        model_id = st.session_state.url["path"]
    if(st.session_state.url["clicked"] and st.session_state.url["path"]==""):
        st.session_state.url["clicked"] = False
        st.session_state.processed = False
        st.experimental_set_query_params()
        #reset_session_state()
    elif(model_id and model_id!='chat' and not st.session_state.processed):
        
        my_bar = st.empty()
        my_bar.progress(0, text="Operation in progress")
        with my_bar:
            model,agents = load(model_id)
            if(model == None or agents == None):
                st.error('Chat Model Does Not Exist')
                st.experimental_set_query_params()
            else:
                st.session_state.model = model
                get_conversation_chain(agents["conversation"])
                st.session_state.processed = True
                load_session_state()
                st.experimental_set_query_params(model_id=model_id)
                #st.experimental_rerun()
        my_bar.empty()
    elif(model_id == 'chat' and not st.session_state.processed):
        remove_dir(f"dataset/process/{st.session_state.user_id}/{st.session_state.session_id}/output")
        my_bar = st.empty()

        my_bar.progress(0, text="Operation in progress")
        with my_bar:
            
            get_conversation_chain()
            st.session_state.processed = True
            st.session_state.model = {
                        'id':'NEW',
                        'index':0,
                        'name':''
            }
            #st.experimental_rerun()
        my_bar.empty()