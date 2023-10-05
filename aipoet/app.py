#AIPoet_main

#0. Importing libraries

import streamlit as st
import pandas as pd
from streamlit_server_state import server_state, server_state_lock
from PIL import Image 
from transformers import AutoProcessor
from transformers import AutoModelForCausalLM as tAMCL
import re
from os.path import dirname
import time
from langchain.llms import CTransformers

#1. Sidebar component

with st.sidebar:
    st.title(":grey[_AI_]:green[Poet]")
    st.markdown('''
                
                ''')
    st.image(r'ai poet se.png')
    st.markdown("_Now, AI can see you and your world and write poems._")



#2. Data needed for one time loading stored in server-level variables

checkpoint = 'microsoft/git-base'
llama_checkpoint = 'TheBloke/Llama-2-7B-Chat-GGML'

with server_state_lock["processor"]:  # Lock the "count" state for thread-safety
    if "processor" not in server_state:
        server_state.processor = AutoProcessor.from_pretrained(checkpoint)

with server_state_lock["model"]:  # Lock the "count" state for thread-safety
    if "model" not in server_state:
        server_state.model = tAMCL.from_pretrained(checkpoint)
        
with server_state_lock["chat_model"]:  # Lock the "count" state for thread-safety
    if "chat_model" not in server_state:
        server_state.chat_model = CTransformers(model=llama_checkpoint,
        model_type='llama',
        max_new_tokens = 512)
        
with server_state_lock["poem_descriptions"]:  # Lock the "count" state for thread-safety
    if "poem_descriptions" not in server_state:
        server_state.poem_descriptions = pd.read_csv("poem_type_descriptions.csv",encoding='cp1252')
        

 
#3. Process 
     
#3.1. Tabs
tab1, tab2 = st.tabs([
    "Looking at the world",
    "My poem"]
    )

#3.2 Inside Tab 1
with tab1:

    def capture_photo(): #function to get image by webcam
        capture = st.camera_input("Show me a good view that makes me lost")
        if "rerun" not in st.session_state:
            with st.spinner("Wait for me to bring my notebook and pen. Don't click photo yet!"): #st.camera doesn't store the image at the first run with some browsers 
                time.sleep(10)
            st.session_state.rerun = 1
            st.experimental_rerun()
        return capture
    
    #3.2.1. Get Image
    image_file =  capture_photo() or st.file_uploader("**_OR_**    Show me a good picture that ignites my thoughts",type=['png','jpeg','jpg'])
    
    if image_file is not None:
        img = Image.open(image_file)
        
        #3.2.2. Generate caption
        with st.spinner("I'm diving into the view..."):
            device = "cpu"
            inputs = server_state.processor(images=img, return_tensors="pt").to(device)
            pixel_values = inputs.pixel_values
            generated_ids = server_state.model.generate(pixel_values=pixel_values, max_length=50)
            generated_caption = server_state.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]  #generate caption
        
        #3.2.3. Options to user
        Type1 = st.radio( #
            "You want me to write a long poem?",
            ["Short", "Long"])
        
        label = "Of which kind? Definitions: [jerichowriters](https://jerichowriters.com/25-different-types-of-poems/)"
        
        Type2 = st.selectbox(
            label,
            ("Prose Poetry", "Ballad", "Elegy", "Epic", "Free Verse", "Blank Verse", "Haiku", "Limerick", "Acrostic Poem", "Sonnet", "Ekphrastic Poem", "Lyric Poetry", "Narrative Poetry", "Ode", "Epitaph", "List Poem", "Occasional Poetry"))
        
        #3.2.4. Retrieve poem_type_description
        poem_descriptions = pd.read_csv("poem_type_descriptions.csv",encoding='cp1252')  
        description = server_state.poem_descriptions[server_state.poem_descriptions['poem_type'] == Type2]['description'].values[0]
        
        #3.2.5. Create prompt including caption. Include poem_type_description as context in prompt_template.
        prompt = f"Write a {Type1} {Type2} on {generated_caption}. Write the title at the start. DO NOT write anything else."
        prompt_template = f'''[INST] <<SYS>>
You are a renowned creative poet. Write according to the knowledge:

"{description}"
<</SYS>>
{prompt}[/INST]'''
        
        #3.2.6. LLM response to prompt
        if st.button('Leave me to write'):
            with st.spinner("Imagining. I'll take all the time in the world..."):
                output = server_state.chat_model(prompt_template)
                if 'Title' in output:
                    output = output[output.index('Title'):]
                output = re.sub(r'([A-Z])', r'\n\1', output)
                st.write("I wrote the poem in :green[My poem] space")
            
            #3.3 Inside Tab 2 - show Image and Poem
            with tab2:
                with st.container():
                    st.image(img, width=400)
                    st.write(output)
