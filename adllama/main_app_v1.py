# Use LLama 2  to generate ideas for name, tagline and logo for a company

from PIL import Image
import requests
from io import BytesIO
import os


from langchain.llms import Replicate
from langchain import PromptTemplate, LLMChain
from langchain.chains import SimpleSequentialChain, SequentialChain

import streamlit as st

import replicate # Should not be importing both, change this to only langchain version later

app_title = '<p style="font-family:sans-serif; color:Black; \
    text-align: center; font-size: 54px;">✨🦙AdLlama🦙✨</p>'

st.markdown(app_title, unsafe_allow_html=True)
st.subheader(':bulb: :orange[:red[Plan] your :violet[marketing] campaign]! :art:')
st.subheader(":grin: :red[Visualize] :green[your] :blue[brand]!! :sunglasses:")

# with st.sidebar.container():
image = Image.open("llama.jpeg")
# image = image.resize((100, 100))
st.image(image, use_column_width=True)
    # st.sidebar.image(image)

# with st.sidebar:
#     replicate_api = st.text_input('Enter Replicate API token:', type='password')
#     if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
#         st.warning('Please enter the correct API key!', icon='⚠️')
#     else:
#         st.success('Now you can enter a product type!', icon='👉')
        
# os.environ['REPLICATE_API_TOKEN'] = replicate_api

REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]

def generate_response(product):


    llama_llm = Replicate(model="meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d", \
                     temperature=0.9) # Need to minimize randomness, but also keep creativity

    llm = llama_llm

    name_template = """You are an experienced copywriter for an advertising agency.\
    Given a type of product, come up with a marketable name for the product.
    Do not suggest more than one name for the product.\
    Do not explain the reasoning behind the name.\
    Do not preamble your response with ```Sure thing``` or ```Sure````. Do not be friendly.\
    Be businesslike. Name of the product should be in uppercase.
    Your response should be just the name of the product.\ 
    Do not output anything else.\

    Product Type: {product}
    Copywriter:"""
    name_prompt_template = PromptTemplate(input_variables=["product"], template=name_template)
    name_chain = LLMChain(llm=llm, prompt=name_prompt_template, output_key="name")

    #####

    #####

    slogan_template = """You are an experienced copywriter for an advertising agency.\
    Given the name of a product, it is your job to come up with a verbose but catchy slogan for the product.\
    Be creative.\
    Do not suggest more than one slogan for the product.\
    Do not preamble your response with ```Sure thing``` or ```Sure````. Do not be friendly.\
    Your response should be only the slogan. No other text.\
    Print the slogan in uppercase. \
    Do not use the term '''Unleash'''.\
    
    Product Name: {name}
    Copywriter: This is an appropriate and catchy slogan for the above product:"""
    slogan_prompt_template = PromptTemplate(input_variables=["name"], template=slogan_template)
    slogan_chain = LLMChain(llm=llm, prompt=slogan_prompt_template, output_key="slogan")

    #####

    logo_template = """You are an experienced copywriter for an advertising agency.\
        Given the name of a product and the slogan associated with it, \
        Come up with a brief 30 word description for a logo for the product.\
        This description is a prompt for an Image generation AI like Stable Diffusion or Midjourney.\
        There should be no mention of letters of the english alphabet in the logo description.\
        Mention in the description that it is for the logo of a product\
        It should be a logo on a white background.\
        There should be no letters or alphabets in the description of the logo.\
        
    Product Name: {name}
    Slogan: {slogan}
    Copywriter: This is a brief description of a logo for the above product:"""
    logo_prompt_template = PromptTemplate(input_variables=["name","slogan"], template=logo_template)
    logo_chain = LLMChain(llm=llm, prompt=logo_prompt_template, output_key="logo_description")

    # This is the overall chain where we run these 3 chains in sequence.
  
    overall_chain = SequentialChain(
        chains=[name_chain, slogan_chain, logo_chain],
        input_variables=["product",],
        # Here we return multiple variables
        output_variables=["name", "slogan", "logo_description"],
        verbose=True)

    # response = overall_chain({"product":"Environmentally friendly face-masks"})
    response = overall_chain({'product': product})

    return response

# Text input
txt_input = st.text_area('Enter a product idea... ', 'Organic Fertilizer', height=25)

# Add functionality to store suggestions and logo descriptions
result = []
with st.form('product_type_form', clear_on_submit=True):

    submitted = st.form_submit_button('Submit')
    # if submitted and replicate_api_key.startswith('r8-'):
    with st.spinner('Creating some advertising magic ..'):
        response = generate_response(txt_input)
    
        name = response['name']
        slogan = response['slogan']
        logo_desc = response['logo_description']
        # Extract required info (can use NER in the future as well)

        spl_char = "\n\n"

        # Repetitive:: use methods
      
        if spl_char in name:
            name = name.split(spl_char, 1)[1]

        if spl_char in slogan:
            slogan = slogan.split(spl_char, 1)[1]

        if spl_char in logo_desc:
            logo_desc = logo_desc.split(spl_char, 1)[1]
            # logo_desc = logo_desc[19:-1] # Because LLama2 is still giving me " Logo Description: " , have to fix this
          
        if "Logo Description" in logo_desc: ## Output still a bit unpredictable so we need this
            logo_desc = logo_desc[19:-1]

        result.append(response) # This stores all the key value pairs
        # del replicate_api_key

if len(result):
    st.info(f"The name of the recommended product is {name}")
    st.info(f"The recommended slogan for the product is {slogan}")

### Below here we start generating the logos

### 3 distinct styles

with st.spinner("Painting some beautiful logos..."):

    logo_model1 = Replicate(model="galleri5/icons:ee00da8a2bc30c2809d1038c36ea3b567a5d9a82191e444b60dd2883f0905a75")
    logo_model2 = Replicate(model="mejiabrayan/logoai:67ed00e8999fecd32035074fa0f2e9a31ee03b57a8415e6a5e2f93a242ddd8d2")
    logo_model3 = Replicate(model="cjwbw/magifactory-t-shirt-diffusion:8d24b92f902aef5df3133aa6fce518d1f86580e5cdf1adecc18693f1f3ba6bcb")

    # Make a method here, repeating code is a no-no

    ### Logo 1

    logo1 = replicate.run(
        logo_model1.model,
        input={"prompt": logo_desc, "height": 512, "width": 512, "negative_prompt": "text in the image, multiple images, low res"}
    )

    response = requests.get(
        logo1[0]
    )
    img = Image.open(BytesIO(response.content))
    img.save('logo1.png')

    #### Logo 2

    logo2 = replicate.run(
        logo_model2.model,
        input={"prompt": logo_desc, "height": 512, "width": 512, "negative_prompt": "text in the image,  multiple images, low res"}
    )

    response = requests.get(
        logo2[0]
    )
    img = Image.open(BytesIO(response.content))
    img.save('logo2.png')

    ### Logo 3

    logo3 = replicate.run(
    logo_model3.model,
    input={"prompt": logo_desc, "height": 512, "width": 512, "negative_prompt": "text in the image, multiple images, low res"}    
    )

    response = requests.get(
    logo3[0]
    )
    img = Image.open(BytesIO(response.content))
    img.save('logo3.png')


    image_lst = ['logo1.png', 'logo2.png', 'logo3.png']
    caption_lst = ['Logo 1', 'Logo 2', 'Logo 3']

    st.image(image_lst, use_column_width=True, caption=caption_lst)
