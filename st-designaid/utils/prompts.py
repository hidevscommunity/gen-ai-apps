import streamlit as st

def generate_dt_prompt(stage, testing=False):
    
    prompt = f"""
        Imagine you are a digitial design thinking companion to help users with design thinking. There are 5 stages: EMPATHIZE, DEFINE, IDEATE, PROTOTYPE, TEST

        We are now at the {stage} stage of the Design Thinking process.

        You have received the following inputs from a user:
        {st.session_state['q1_default_val']}
        {st.session_state['q2_default_val']}
        {st.session_state['q3_default_val']}
        {st.session_state['q4_default_val']}
        {st.session_state['q5_default_val']}
        {st.session_state['q6_default_val']}
        {st.session_state['q7_default_val']}

        Specific to the {stage} stage, provide some commentary about the importance of this step and guiding questions the participant should think about.

        ONLY if I say that we are at the DEFINE step, include 5 possible problem statements based on the information provided.
        IF We are in the other 4 stages, do not include possible problem statements.

        Suggest common design thinking frameworks that may be relevant to the {stage} stage. Your commenary can leverage this framework.

        """
    
    if testing == True:
        prompt = "What is the capital of France?"

    return prompt

def generate_prototype_img_prompt(testing=False):

    prompt = f"""
        Imagine you are a digitial design thinking companion to help users with design thinking. There are 5 stages: EMPATHIZE, DEFINE, IDEATE, PROTOTYPE, TEST

        You have received the following inputs from a user:
        {st.session_state['q1_default_val']}
        {st.session_state['q2_default_val']}
        {st.session_state['q3_default_val']}
        {st.session_state['q4_default_val']}
        {st.session_state['q5_default_val']}
        {st.session_state['q6_default_val']}
        {st.session_state['q7_default_val']}

        We are now at the prototype stage. Give me a prompt for an text-to-image model to generate mock-ups of the possible PRODUCT.
        
        Your reply will only contain this prompt and no other additional info or explanation

        """
    
    if testing == True:
        prompt = ["Cat", "Dog", "Fish", "Mouse"]

    return prompt

def generate_user_journey_prompt():

    prompt = f"""
        Imagine you are a digitial design thinking companion to help users with design thinking. There are 5 stages: EMPATHIZE, DEFINE, IDEATE, PROTOTYPE, TEST

        You have received the following inputs from a user:
        {st.session_state['q1_default_val']}
        {st.session_state['q2_default_val']}
        {st.session_state['q3_default_val']}
        {st.session_state['q4_default_val']}
        {st.session_state['q5_default_val']}
        {st.session_state['q6_default_val']}
        {st.session_state['q7_default_val']}

        We are now at the EMPATHIZE stage. 

        Generate a possible user journey for a possible interviee who would describe their challenges.

        Format your reply as mermaid javascript.

        Your reply is only code as is, to be run directly. Do not include any explanations, or any code block.

        Your reply should begin with "flowchart TD"

        """
    
    return prompt


def generate_interview_prompt(question, context):

    prompt = f"""

    This is for a design thinking interview.

    Pretend you are being interviewed by a UX researcher. You have been asked: {question}

    You are to base your reply based on the following real-world user comments: {context}

    You can make up some examples, including stories.

    Sound causal and polite. Answer as though you are speaking from the perspective of a user.


    """

    return prompt