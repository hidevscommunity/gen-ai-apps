from dotenv import load_dotenv
load_dotenv()
import streamlit as st


import extra_streamlit_components as stx
from utils.session_state import *
from utils.helpers import *
from streamlit.components.v1 import html
from custom_streamlit.components import *
from custom_streamlit.functions import *
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.web.server.server import Server
from utils.session_id import *
@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

def main():
    model_id = st.experimental_get_query_params().get('model_id', [''])[0]
    
    st.set_page_config(page_title="Auto Chain",
                       page_icon=":exploding_head:")


    with open('html/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
   
    init_session_state()

    cookie_manager = get_manager()

    if not st.session_state.user_id:
        cookies = cookie_manager.get_all()
        empty = st.empty()
        if cookies == {}:
            empty.write('Loading')
        else:
            if 'ajs_anonymous_id' not in cookies:
                empty.write("You're now authenticated. Please refresh the page")
            else:

                empty.empty()
                st.session_state.user_id = cookies['ajs_anonymous_id']
                session_id = get_script_run_ctx().session_id
                #Add session_id to sessions.json
                clear_sessions()
                add_to_process(session_id,st.session_state.user_id)
                st.session_state.session_id = session_id
                st.experimental_rerun()
    else:
        if(st.session_state.max_iterations!=0):
            executor_session_state().max_iterations = st.session_state.max_iterations
            st.session_state.max_iterations = 0
            

        
        func_handle_url(model_id)
        
        header,subheader = st.empty(),st.empty()
        
        if not st.session_state.processed:

            remove_dir(f'dataset/process/{st.session_state.user_id}/{st.session_state.session_id}/output')
            remove_dir(f'dataset/process/{st.session_state.user_id}/{st.session_state.session_id}/input')
            ##Custom Streamlit Header
            st_header_home(header,subheader)
            
            ## Custom Streamlit Process Button Block
            st_process()

            ## Custom Streamlit Sidebar Chat Models
            st_models_load()
            
            ## Custom Streamlit Changelog
            st_examples()
            st_changelog()

        else:
            
            
            # Custom Streamlit Sidebar Component        
            option = st_sidebar()

            # Custom Streamlit Chat Header Component           
            st_header_chat(header,option)

            # Custom Streamlit Chat Component        
            st_chat()

            # Custom Streamlit Model Save
            st_model_save()

            # Custom Streamlit Chat Input
            st_chat_input()
        
        
        with open('html/script.txt',"r") as f:
            js_content = f.read()
        
        html(f"""{js_content}""")
    
    
if __name__ == '__main__':
    main()







#"show in a histogram sbp as a function of age with 10 years bins"

