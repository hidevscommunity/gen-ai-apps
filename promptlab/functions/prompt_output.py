# prompt_output.py

import streamlit as st
import pandas as pd
import re
import random

from functions.get_parameters import get_parameters
from functions.prompt_input import prompt_input
from functions.processing_messages import messages

# Get user's prompts and params
def get_prompts(num_prompts):
    prompts_dict = {}
    for i in range(num_prompts):
        prompt_input = st.text_area(
            f'Prompt {i + 1}:', 
            placeholder=f'Prompt {i + 1}:', 
            label_visibility="collapsed"
        )
        prompts_dict[f"prompt_{i + 1}"] = prompt_input

        with st.expander(f"__Prompt {i+1} parameters setting__"):
            response_params = get_parameters(f"prompt_{i + 1}")
            st.session_state[f"response_params_{i + 1}"] = response_params

    return prompts_dict

# Placeholder columns
def generate_placeholder_dict(prompts):
    placeholder_dict = {}
    for prompt_key in prompts.keys():
        if prompts[prompt_key]:
            placeholder_dict[prompt_key] = re.findall(r'\[\[(.*?)\]\]', prompts[prompt_key])
    return placeholder_dict

# Get relevant cols to output table
def output_relevant_cols(df, prompts, placeholder_dict):
    prompt_output = pd.DataFrame(index=df.index)

    for prompt_key in prompts.keys():
        if prompts[prompt_key]:
            placeholder_columns_in_df = placeholder_dict[prompt_key]
            relevant_cols = [col for col in placeholder_columns_in_df if col in df.columns]
            for col in relevant_cols:
                prompt_output[col] = df[col]
    return prompt_output

# Get responses 
def process_prompts(df, prompts, placeholder_dict, prompt_output):
    for idx, prompt_key in enumerate(prompts.keys()):
        random_message = random.choice(messages)
        if prompts[prompt_key]:
            apply_prompt_state = st.text(random_message)
            placeholder_columns = placeholder_dict[prompt_key]
            result_series = df.apply(
                prompt_input, 
                args=(prompts[prompt_key], prompt_key, placeholder_columns, st.session_state[f"response_params_{idx+1}"]),
                axis=1
            )
            prompt_output[prompt_key] = result_series[prompt_key]
            apply_prompt_state.text("Done!")
    return prompt_output

def generate_prompts_output(df, prompts):
    placeholder_dict = generate_placeholder_dict(prompts)
    prompt_output = output_relevant_cols(df, prompts, placeholder_dict)
    prompt_output = process_prompts(df, prompts, placeholder_dict, prompt_output)
    return prompt_output
