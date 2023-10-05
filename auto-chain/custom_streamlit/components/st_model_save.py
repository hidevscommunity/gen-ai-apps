import streamlit as st
from utils.session_state import *
import pandas as pd
from firebase.service import save

def save_df():
    #st.session_state.df_changed = True
    df = issues_session_state()
    if(len(df) == 0):
        df = [{"issue":"Description Here"}]
    dataframe = st.session_state[st.session_state.agent]

    #df = [{"issue":dataframe["edited_rows"][0]["issue"]}]
   
    for key,row in dataframe["edited_rows"].items():
        if "issue" in row:
            df[key]["issue"] = row["issue"]
    for row in dataframe["added_rows"]:
        if "issue" in row:
            df.append({"issue":row["issue"]})
    count = 0
    for row in dataframe["deleted_rows"]:
        df.pop(row-count)
        count +=1     
    issues_session_state()[:] = df

def st_model_save():
    with st.sidebar:
        name = st.text_input("Name",st.session_state.model["name"])
        if st.session_state.model['show']:
            container = st.container()

            df = issues_session_state()
            if(len(df) == 0):
                df = [{"issue":"Description Here"}]
            df =  pd.DataFrame(df) 
            
            edited_df = st.data_editor(
                df,
                use_container_width=True,
                column_config={
                    "issue": "Issue"
                },
                num_rows="dynamic",
                hide_index=True,
                key=f'{st.session_state.agent}',
                on_change=save_df,
            )
        
            with container:
            
                if(st.session_state.model['id']=="NEW"):
                    options = st.multiselect(
                    'Choose Agents',
                    list(st.session_state.conversation_chain.keys()),
                    list(st.session_state.conversation_chain.keys()))
                else:
                    options = list(st.session_state.conversation_chain.keys())
                unsaved = st.empty()
                if st.button("Save",use_container_width=True,type='primary'):
                    if not name:
                        st.error('Please provide a name')
                        return
                    my_bar = st.progress(0, text=f'Operation in Progress')
                    with my_bar:
                        id = save(st.session_state.model["id"],name,st.session_state.conversation_chain,options)
                        load_session_state()
                        st.success(f'Chat Model Saved ID {id}')
                        st.experimental_set_query_params(model_id=id)
                        st.session_state.model['id'] = id
                if(compare_session_state()):
                    unsaved.error("**Unsaved Changes**")        