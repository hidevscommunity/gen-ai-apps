# get_parameters.py

import streamlit as st

def get_parameters(prefix=""):
    
    col1, col2, col3 = st.columns(3)

    models = [
        "gpt-3.5-turbo", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0613", 
        "gpt-4", "gpt-4-0613", "gpt-4-32k", "gpt-4-32k-0613"    
    ]
    
    model = col1.selectbox("Model", models, key=f"{prefix}set_model")

    max_tokens = int(col2.number_input(
        "Max tokens", min_value=0, value=150,
        help="The maximum number of [tokens](https://platform.openai.com/tokenizer) to generate in the chat completion.", 
        key=f"{prefix}set_tokens"
    ))
    
    temperature = float(col3.slider(
        "Temperature", min_value=0.0, max_value=1.0, value=0.25, 
        help="Lower values for temperature result in more consistent outputs, while higher values generate more diverse and creative results. Select a temperature value based on the desired trade-off between coherence and creativity for your specific application.", 
        key=f"{prefix}set_temp"
    ))

    col11, col12, col13 = st.columns(3)
    
    top_p = float(col11.slider(
        "Top p", min_value=0.0, max_value=1.0, value=1.0, 
        help="An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.",
        key=f"{prefix}set_top_p"
        ))
    
    presence_penalty = float(col12.slider(
        "Presence penalty", min_value=-2.0, max_value=2.0, value=0.0, 
        help="Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.",
        key=f"{prefix}set_p_penalty"
    ))

    frequency_penalty = float(col13.slider(
        "Frequency penalty", min_value=-2.0, max_value=2.0, value=0.0,
        help="Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.",
        key=f"{prefix}set_f_penalty"
        ))
    
    return {
        'model': model,
        'max_tokens': max_tokens,
        'temperature': temperature,
        'top_p': top_p,
        'presence_penalty': presence_penalty,
        'frequency_penalty': frequency_penalty        
    }