import streamlit as st
from langchain.llms import Clarifai
from langchain import PromptTemplate, LLMChain
from hairAi import get_best_hair_type
from PIL import Image
import io
import time

st.title('Llama HairSense')
st.caption('Clarifai X Llama2 - Lablab.ai Hackathon')
st.write("Elevate your hair care journey with HairSense: a transformative project uniting Clarifai's advanced vision AI and Llama 2's perceptive prowess. Effortlessly decipher your hair's distinct nature through imagery, unlocking custom-tailored solutions that redefine hair care precision.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def model(text, mess):
    with st.spinner("Llama is thinking ..."):
        # Clarifai API key - Personal Access Token
        CLARIFAI_PAT = 'c18a2b6b798045fb9d3c6b0dbf9a0f5b'
        # Initialize the Clarifai LLM with proper settings
        USER_ID = 'meta'
        APP_ID = 'Llama-2'
        MODEL_ID = 'llama2-13b-chat'
        MODEL_VERSION_ID = '79a1af31aa8249a99602fc05687e8f40'
        clarifai_llm = Clarifai(
            pat=CLARIFAI_PAT, user_id=USER_ID, app_id=APP_ID, model_id=MODEL_ID, model_version_id=MODEL_VERSION_ID
        )

        # Create LLM chain
        template = """What is the good hait routine for {question} hair? Write it compactly"""
        prompt_template = PromptTemplate(template=template, input_variables=["question"])
        llm_chain = LLMChain(prompt=prompt_template, llm=clarifai_llm)

        # Get the assistant's response
        response = llm_chain.run(question=text)
        print(response)
    return response

@st.cache_data
def load_image(image_file):
    img = Image.open(image_file)
    # Convert the image data to bytes
    image_bytes = io.BytesIO()
    img.save(image_bytes, format=img.format)
    image_bytes = image_bytes.getvalue()
    return image_bytes

if __name__ == "__main__":
    with st.chat_message("assistant"):
            st.markdown("Hello, I am your haircare assistant. I would appreciate the opportunity to examine your hair. May I take a closer look? 🔍")
            image_file = st.file_uploader("Kindly upload a picture that clearly displays your hair",type=['png','jpeg','jpg'])
            if image_file is not None:
                image = load_image(image_file)
                st.image(image_file)
                st.success("Image uploaded succesfully")
                USER_ID = 'infinitebeing'
                PAT = 'c18a2b6b798045fb9d3c6b0dbf9a0f5b'
                APP_ID = 'hair-ai'
                WORKFLOW_ID = 'hair-ai-workflow'
                hairType, score = get_best_hair_type(image, USER_ID, PAT, APP_ID, WORKFLOW_ID)
                st.write("Based on the visual characteristics, it appears that your hair has a", hairType, "texture.")
                # Ask user to input a message
                user_message = 1
                # Check if user provided a message
                if user_message:
                    # Call the model function
                    assistant_response = model(hairType, user_message)
                    # Display assistant's response
                    st.success('Done!')
                    with st.expander("Curated Hair-Care Solution"):
                        st.write(assistant_response.split("\n",2)[2])