
import streamlit as st
from firebase.service import load_all,delete
from utils.session_state import *
from custom_streamlit.html_components import my_component
    
def st_models_load():
    with st.sidebar:
        
            
        option = st.selectbox(
                    "Sort by",
                    options= [
                        {"name":"Last Updated","value":"last_updated"},
                        {"name":"Created","value":"created_at"},
                        {"name":"Issues","value":"total_issues"}
                        ],
                    format_func=lambda x: str(x["name"]),
                    placeholder="Sort by",
                    
                    
        )
        with st.spinner("Loading Models"):
            names = load_all(option["value"])
            if(len(names)!=0):
                num_clicks = my_component(names,type=option["value"],key='hg')
                if num_clicks:
                    if(num_clicks['type'] == 'delete'):

                        delete(num_clicks["id"])
                        st.experimental_rerun()
                        
                    else:
                        st.experimental_set_query_params(model_id=num_clicks['id'])
                        st.session_state.url  = {"path":num_clicks['id'],"clicked":True}
                        st.experimental_rerun()
            else:
                st.write(" No Chat Models Found")        