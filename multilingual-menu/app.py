from langchain.llms import Clarifai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from config import *
from sidebar import display_sidebar
from image_prediction import get_ingredient_from_image 

#sidebar
display_sidebar()

try:
    prompt = PromptTemplate(template=template, input_variables=["question"])
    clarifai_llm = Clarifai(pat=PAT, user_id=USER_ID, app_id=APP_ID, model_id=MODEL_ID)
    llm_chain = LLMChain(prompt=prompt, llm=clarifai_llm)
except Exception as e:
    st.error("Something unexpected happened,Please Try After sometime")
    st.stop()

    
st.title('Multilingual Menu👨‍🍳🍳')

st.markdown("""
    <style>
        .reportview-container .main .block-container {
            position: relative;
        }
        #sampleLink {
            position: absolute;
            top: 15px;
            right: 20px;
            z-index: 2;
        }
    </style>
    <a id="sampleLink" href="https://github.com/SabarinathK/multilingual-menu/tree/main/images" target="_blank">Download Sample Images</a>
""", unsafe_allow_html=True)

uploaded_images = st.file_uploader("Upload ingredients image one after another", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

st.markdown('<p style="text-align: center;">or</p>', unsafe_allow_html=True)

if 'predicted_ingredients' not in st.session_state:
    st.session_state.predicted_ingredients = []

if uploaded_images:
    for uploaded_image in uploaded_images:
        predicted_ingredient = get_ingredient_from_image(uploaded_image)
        if predicted_ingredient: 
            st.session_state.predicted_ingredients.append(predicted_ingredient)

unique_ingredients = list(set(st.session_state.predicted_ingredients))
ingredients_str = ', '.join(unique_ingredients)
st.write(f"Predicted Ingredient: {ingredients_str}")
ingredients_input = st.text_input("Enter ingredients : *", ingredients_str, placeholder="eg: onion, rice, tomato")
user_country = st.text_input("Enter country style : *", placeholder="eg: american")
language = st.text_input("Enter menu language : (optional)", placeholder="eg: hindi, default : english")


warnings_placeholder = st.empty()

if st.button('Generate Recipe'):
    try:
        language = language or 'english'
        warnings_placeholder.empty()

        warnings = []
        if not ingredients_input:
            warnings.append("Kindly enter ingredients.")
        if not user_country:
            warnings.append("Kindly enter your country style.")

        if warnings:
            warning_message = ' | '.join(warnings)
            warnings_placeholder.warning(warning_message)

        else:
            question = f"create recipe with {ingredients_input} these ingredients with {user_country} style, in {language} language"
            response = llm_chain.run(question)
            st.write(response)
    except Exception as e:
        st.error("Something unexpected happened,Please Try After sometime")
        st.stop()
