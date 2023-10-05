import streamlit as st
import streamlit.components.v1 as components
import extra_streamlit_components as stx
from streamlit_option_menu import option_menu

from datetime import datetime
import json
from fpdf import FPDF
import base64
from utils.flowchart import mermaid
from utils.pdf import sanitise_text, multi_cell, create_download_link
from utils.clarifai import query_gpt4, query_SDXL, moderate_input
from utils.prompts import generate_dt_prompt, generate_prototype_img_prompt, generate_user_journey_prompt, generate_interview_prompt
from utils.weaviate import load_data_to_weaviate, query_weaviate, clear_weviate

from langchain.llms import Clarifai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

######


##########
st.set_page_config(
    page_title="designAId",
    page_icon="🧑‍🎨",
    layout="wide",
    initial_sidebar_state="auto"
)

##########

if 'menu_option' not in st.session_state:
    st.session_state['menu_option'] = 0

if 'generated' not in st.session_state:
    st.session_state['generated'] = 0

if 'autofilled' not in st.session_state:
    st.session_state['autofilled'] = False

if 'persona_loaded' not in st.session_state:
    st.session_state["persona_loaded"] = False


st.session_state["session_id"] = datetime.now().strftime('%H:%M:%S')


if st.session_state.get('fwd_btn', False):
    st.session_state['menu_option'] = (st.session_state.get('menu_option', 0) + 1) % 5
    manual_select = st.session_state['menu_option']
else:
    manual_select = None

demo_values = [f"q{i}_default_val" for i in range(1, 8)]

for demo_val in demo_values:
    if demo_val not in st.session_state:
        st.session_state[demo_val] = ""

nav_emoji = {
    "Empathise":"❤️", 
    "Define": "🖊️", 
    "Ideate": "💡", 
    "Prototype": "🔧",
    "Test": "✅"}

DT_STAGES = ["EMPATHISE", "DEFINE", "IDEATE", "PROTOTYPE", "TEST"]

##########
st.markdown("# Design:rainbow[AI]d")
st.caption("An AI-powered Design Thinking companion")

# testing_mode = st.toggle('Testing Mode')
testing_mode = False

def load_dt_tool():
    # for stage in DT_STAGES:
    #     st.session_state[f"gpt_results_{stage}"] = query_gpt4(generate_dt_prompt(stage, testing=testing_mode))
    st.session_state["gpt_results_EMPATHISE"] = query_gpt4(generate_dt_prompt("EMPATHISE", testing=testing_mode))

def render_dt_page():
    st.session_state['generated'] = 1
    st.experimental_rerun()

def nsfw(text):        
    results = moderate_input(text)
    if results[0] == True:
        st.toast(f"Moderation flag: {results[1]} ({results[2]})", icon='⚠️')
        return 1
    return 0

##########
if st.session_state['generated'] == 0:

    # Autofill
    with st.expander("Demo Quick Start"):
        st.write("For the purposes of this demo, we can autofill the fields below. Please also download the sample user comments")
        colA, colB, colC, _ = st.columns(4)
        
        if colA.button("Autofill"):
            st.session_state['q1_default_val'] = "I'm a Product Designer with a focus on developing assistive technology tools to enhance the daily lives of individuals with disabilities."
            st.session_state['q2_default_val'] = "Our primary target audience includes individuals with physical impairments, specifically those who have mobility challenges. This ranges from elderly individuals with reduced dexterity to younger individuals who might have been born with or acquired physical limitations."
            st.session_state['q3_default_val'] = "Many daily tasks are challenging for our audience due to a lack of accessible devices. This hinders their independence and confidence daily."
            st.session_state['q4_default_val'] = "Mainstream design often overlooks disability needs, perceptions of high development costs, and a lack of empathy for unique challenges."
            st.session_state['q5_default_val'] = "Modular tools for customization, voice and gesture-controlled devices, and partnerships with therapists for insight."
            st.session_state['q6_default_val'] = "Yes, but they were often too specialized, expensive, or lacked aesthetics and durability."
            st.session_state['q7_default_val'] = "Increased user independence, high adoption rates, and positive user feedback indicating enhanced daily living."
            st.session_state['autofilled'] = True

            st.session_state["user_inputs"] = [st.session_state[f'q{i}_default_val'] for i in range(1, 8)]
        
        with open("sample-data/user_comments.json", "rb") as file:
            btn = st.download_button(
                label="Download Sample",
                data=file,
                file_name="user_comments.json",
          )

        if colB.button("Clear"):
            for i in range(1, 8):
                st.session_state[f'q{i}_default_val'] = ""

        btn_generate = colC.button("Generate Now")
        if btn_generate & (not st.session_state['autofilled']):
            colA.error("Please click 'Autofill'")
        elif btn_generate & st.session_state['autofilled']:

            with st.spinner("Checking your answers..."):
                failed = 0
                for q_num in range(1, 8):
                    failed += nsfw(st.session_state[f'q{q_num}_default_val'])

            if failed == 0:
                with st.spinner('Starting up my engines. Please give me about 3 mins to think about your project...'):

                    with open("sample-data/user_comments.json", 'r') as json_file:
                        q8_file = json.load(json_file)

                    st.session_state["user_inputs"] = [st.session_state['q1_default_val'],
                                                       st.session_state['q2_default_val'],
                                                       st.session_state['q3_default_val'], 
                                                       st.session_state['q4_default_val'], 
                                                       st.session_state['q5_default_val'], 
                                                       st.session_state['q6_default_val'], 
                                                       st.session_state['q7_default_val']
                                                       , q8_file]
                    load_dt_tool()
                    render_dt_page()


    # Form
    st.markdown("#### Please fill up the below")
    col1, col2 = st.columns(2)
    q1 = col1.text_area("Q1: What is your role?", 
                         value=f"{st.session_state['q1_default_val']}")
    q2= col1.text_area("Q2: Who is your target audience?",
                         value=f"{st.session_state['q2_default_val']}")
    q3 = col1.text_area("Q3: What is the problem? How is the target audience affected on a day-to-day basis?",
                        value=f"{st.session_state['q3_default_val']}")
    q4 = col1.text_area("Q4: What are some possible root causes?",
                        value=f"{st.session_state['q4_default_val']}")
    q5 = col2.text_area("Q5: What are your prelim solutions?",
                        value=f"{st.session_state['q5_default_val']}")
    q6 = col2.text_area("Q6: Have there been previous attempts?",
                        value=f"{st.session_state['q6_default_val']}")
    q7 = col2.text_area("Q7: What does success look like?",
                        value=f"{st.session_state['q7_default_val']}")
    q8_file = col2.file_uploader("Q8: Upload any available user interviews")
    st.session_state["user_inputs"] = [q1, q2, q3, q4, q5, q6, q7, q8_file]
    
    st.divider()
    pressed = st.button("Generate")
    if pressed & (q1 == "" or q2 == "" or q3 =="" or q4 ==""):
            st.error("Please complete fill up q1 to q4.")
    elif pressed:
        with st.spinner("Checking your answers..."):

            failed = 0

            for inputs in st.session_state["user_inputs"][:7]:
                failed += nsfw(inputs)

        if failed == 0:
            with st.spinner('Starting up my enginges. Please give me about 3 mins to think about your project...'):
                load_dt_tool()
                render_dt_page()
                st.balloons()

elif st.session_state['generated'] == 1:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🤔 Guiding Questions  ", "🚀 Sample User Journey  ", "💬 Mock User Interviews  ", "📄 Download Report  ", "✍️ Your Input  ", "🔁 Restart"])    

    with tab1:
        col1, col2 = st.columns((2,8))

        with col1: 
            selected_step = option_menu("Stages", ["Empathise", "Define", "Ideate", "Prototype", "Test"], 
                icons=['heart', 'pen', "lightbulb", 'wrench', 'check-circle'], 
                orientation="vertical",
                manual_select=manual_select,
                key='menu_4')
            
            if selected_step == "Empathise":
                st.session_state['menu_option'] = 0 
            elif selected_step == "Define":
                st.session_state['menu_option'] = 1
            elif selected_step == "Ideate":
                st.session_state['menu_option'] = 2 
            elif selected_step == "Prototype":
                st.session_state['menu_option'] = 3 
            elif selected_step == "Test":
                st.session_state['menu_option'] = 4 

        with col2: 
            colX, _,colY = st.columns((5, 10, 3))
            colX.markdown(f"## {nav_emoji[selected_step]} {selected_step}")
            colY.write("")
            if (st.session_state['menu_option'] != 4) or (selected_step != "Test"):
                colY.button("Next Stage ⏭️", key='fwd_btn')

            else: 
                if colY.button("Back to start ↩️"):
                    st.session_state['menu_option'] = 0
                    selected_step == "Empathise"

            if (st.session_state['menu_option'] == 0) or (selected_step == "Empathise"):
                st.info(st.session_state[f'gpt_results_{selected_step.upper()}'])
            elif (st.session_state['menu_option'] == 1) or (selected_step == "Define"):
                with st.spinner("Please give me some time to think 🙏 ..."):
                    selected_step_UPPER = selected_step.upper()
                    st.session_state[f"gpt_results_{selected_step_UPPER}"] = query_gpt4(generate_dt_prompt(selected_step_UPPER, testing=testing_mode))
                    st.info(st.session_state[f'gpt_results_{selected_step.upper()}'])
            elif (st.session_state['menu_option'] == 2) or (selected_step == "Ideate"):
                with st.spinner("Please give me some time to think 🙏 ..."):
                    selected_step_UPPER = selected_step.upper()
                    st.session_state[f"gpt_results_{selected_step_UPPER}"] = query_gpt4(generate_dt_prompt(selected_step_UPPER, testing=testing_mode))
                    st.info(st.session_state[f'gpt_results_{selected_step.upper()}'])
            elif (st.session_state['menu_option'] == 3) or (selected_step == "Prototype"):
                col2a, col2b = st.columns(2)
                with st.spinner("Please give me some time to think 🙏 ..."):
                    selected_step_UPPER = selected_step.upper()
                    st.session_state[f"gpt_results_{selected_step_UPPER}"] = query_gpt4(generate_dt_prompt(selected_step_UPPER, testing=testing_mode))
                    col2a.info(st.session_state[f'gpt_results_{selected_step.upper()}'])
                col2b.markdown("### Want to see a possible mock-up?")
                if col2b.button("Yes! 😍"):
                    with st.spinner("Please give me some time to draw 🙏 ..."):
                        st.toast('Generating your image...', icon='🏃')
                        img_prompt = query_gpt4(generate_prototype_img_prompt(testing=testing_mode))
                        image = query_SDXL(img_prompt)
                        st.session_state[f'generated_image'] = image
                        col2b.success(f'**Prompt:** {img_prompt}', icon='🧑‍🎨')
                        col2b.image(image.base64)
                        st.toast('Your mock-ups have been generated!', icon='😍')    
            elif (st.session_state['menu_option'] == 4) or (selected_step == "Test"):
                with st.spinner("Please give me some time to think 🙏 ..."):
                    selected_step_UPPER = selected_step.upper()
                    st.session_state[f"gpt_results_{selected_step_UPPER}"] = query_gpt4(generate_dt_prompt(selected_step_UPPER, testing=testing_mode))
                    st.info(st.session_state[f'gpt_results_{selected_step.upper()}'])








    with tab2:
        if st.button("Generate user journey"):
            with st.spinner("Please give me some time to draw 🙏 ..."):
                user_journey_prompt = query_gpt4(generate_user_journey_prompt())
                mermaid(user_journey_prompt)
                st.toast('Your user journey has been generated!', icon='😍')









    with tab3:
        col3_1, col3_2 = st.columns((5, 8))
        col3_1.markdown("## Interview your virtual persona")

        if st.session_state["persona_loaded"] == False:
            if col3_1.button("Load"):
                with st.spinner("Loading your persona..."):
                    load_data_to_weaviate(st.session_state["user_inputs"][-1])
                    st.session_state["persona_loaded"] = True

        if 'question_list' not in st.session_state:
            st.session_state['question_list'] = []
        question_asked = col3_1.text_area("What do you want to ask?")
        st.session_state['question_list'].append(question_asked)

        if len(st.session_state['question_list']) > 1:
            col3_1.markdown("**Your Previous Qns**")
            for qn in st.session_state['question_list']:
                if qn != "":
                    col3_1.markdown(f"* {qn}")

        if question_asked != "":
            question_to_reply = st.session_state['question_list'][-1]
            col3_2.info(f"**QN**: {question_to_reply}")
            user_context = query_weaviate(question_to_reply)
            col3_2.success(f"**ANS**: {query_gpt4(generate_interview_prompt(question_to_reply, user_context))}")







    with tab4:
        if st.button("Generate Report"):
            with st.spinner("Please give me some time to prepare your report"):
                for stage in ["DEFINE", "IDEATE", "PROTOTYPE", "TEST"]:
                    if f'gpt_results_{stage}' not in st.session_state:
                        st.session_state[f'gpt_results_{stage}'] = query_gpt4(generate_dt_prompt(stage, testing=testing_mode))

                pdf = FPDF()
                pdf.set_left_margin(20)  # Set left margin to 20mm (or whatever value you desire)
                pdf.set_top_margin(20)   # Set top margin to 30mm (or whatever value you desire)
                pdf.add_page()

                # Add long text with automatic line breaks
                multi_cell(pdf, 160, 10, "Your Report", 'Arial', 'B', 16)  # 190 is nearly the width of an A4 paper
                multi_cell(pdf, 160, 10, "", 'Arial', 'B', 16)  # 190 is nearly the width of an A4 paper
                multi_cell(pdf, 160, 10, "Original Input", 'Arial', 'U', 14)  # 190 is nearly the width of an A4 paper

                for qn_num, demo_val in enumerate(demo_values):
                    value = st.session_state.get(demo_val, "")
                    multi_cell(pdf, 160, 10, f"Q{qn_num+1}: {value}", 'Arial', '', 11)
                    multi_cell(pdf, 160, 10, "", 'Arial', '', 11)

                for stage_num, stage in enumerate(DT_STAGES):
                    pdf.add_page()
                    multi_cell(pdf, 160, 10, f"Stage {stage_num+1}: {stage}", 'Arial', 'U', 14)  # 190 is nearly the width of an A4 paper
                    results = st.session_state[f'gpt_results_{stage}']
                    multi_cell(pdf, 160, 10, sanitise_text(results), 'Arial', '', 11)  # 190 is nearly the width of an A4 paper
                    if stage_num == 3:
                        try:
                            multi_cell(pdf, 160, 10, "AI-generated prototype", 'Arial', 'U', 12)  # 190 is nearly the width of an A4 paper
                            pdf.image(st.session_state[f'generated_image'].base64, w=150, h=150)
                        except:
                            pass

                html = create_download_link(pdf.output(dest="S"), "report")

                st.toast('Your report has been generated!', icon='😍')
                
                st.markdown(html, unsafe_allow_html=True)






    with tab5:
        col3, col4 = st.columns(2)
        col3.markdown(f"**What is your role:** {st.session_state['user_inputs'][0]}")
        col3.markdown(f"**Who are you trying to help:** {st.session_state['user_inputs'][1]}")
        col3.markdown(f"**What is the problem:** {st.session_state['user_inputs'][2]}")
        col3.markdown(f"**What are some possible root causes:** {st.session_state['user_inputs'][3]}")
        col4.markdown(f"**Any prelim solutions:** {st.session_state['user_inputs'][4]}")
        col4.markdown(f"**Have there been previous attempts:** {st.session_state['user_inputs'][5]}")
        col4.markdown(f"**What does success look like:** {st.session_state['user_inputs'][6]}")







    with tab6:
        st.error("⚠️ This step is not reversible ⚠️")
        if st.button("Restart"):
            st.session_state['generated'] = 0
            # clear_weviate()
            st.experimental_rerun()