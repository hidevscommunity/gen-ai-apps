import streamlit as st
def on_button_click(model_id):
    st.session_state.url = {"path":model_id,"clicked":True}
def create_button(example):
    return st.button(example["name"],on_click=on_button_click,args=(example["id"],),use_container_width=True)

def st_examples():
    st.markdown("### Examples")
    col1,col2,col3 = st.columns([1,1,1])
    examples = [
        {
            "name":"Image Chat Agent:green [v0.0.4]",
            "id":"7eTRxzehOW4IBxKppjyb"
        },
        {
            "name":"CSV Agent [v0.0.2]",
            "id":"cB6bpnpIQdiyBRXKtXVe"
        },
        {
            "name":"Conversational Agent [v0.0.1]",
            "id":"Gfwvc6yuSkIv9JnBpNtf"
        }
    ]
    for i,example in enumerate(examples):
        if(i%3 == 0):
            with col1:
                create_button(example)
        elif((i-1)%3 == 0):
            with col2:
                create_button(example)
        elif((i-2)%3==0):
            with col3:
                create_button(example)
        
