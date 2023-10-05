import os
from ast import literal_eval
from PIL import Image

import pandas as pd
import streamlit as st
from langchain.llms import Clarifai
from langchain import PromptTemplate
from langchain.document_loaders import BSHTMLLoader


st.set_page_config(layout="centered")


@st.cache_data
def load_pat():
    if "CLARIFAI_PAT" not in st.secrets:
        st.error("You need to set the CLARIFAI_PAT in the secrets.")
        st.stop()
    return st.secrets.CLARIFAI_PAT


@st.cache_resource
def get_text_model(pat):
    USER_ID = "openai"
    APP_ID = "chat-completion"
    MODEL_ID = "GPT-4"
    llm = Clarifai(pat=pat, user_id=USER_ID, app_id=APP_ID, model_id=MODEL_ID)
    return llm


def read_html_files(html_paths):
    docs = []
    for path in html_paths:
        loader = BSHTMLLoader(path)
        doc = loader.load()[0]
        lines = doc.page_content.split("\n")
        filtered_lines = [line for line in lines if line.strip()]
        docs.append("\n".join(filtered_lines))
    return docs


def get_prompt(text):
    prompt_template = """Analyze the provided text to extract eligibility criteria for 
the following fields: Gender, Occupations, and Category, based on information from a 
government scheme. The eligible options for each field are as follows:
1. Gender: ["Male", "Female", "Others", "None"]
2. Occupations: ["Student", "Farmers", "Retired", "None"]
3. Category: ["SC", "ST", "OBC", "General", "None"]

Text to Analyze: {text}


Output Format: Only return a json object wrapped around by "<json> </json>" tags

Example: <json>{{"gender": ["value_1", "value_2", ...], "occupation": ["value_1", "value_2", ...], "category": ["value_1", "value_2", ...]}}</json>

Note: 
* Ensure that the extracted values for the eligibility criteria are from the provided options only.

Response:"""
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    return prompt.format(text=text)


@st.cache_data
def load_database():
    df = pd.read_csv(
        "database.csv",
        converters={
            "gender": literal_eval,
            "occupation": literal_eval,
            "category": literal_eval,
        },
    )
    return df


pat = load_pat()
llm = get_text_model(pat)
df = load_database()
image = Image.open("banner.png")


st.title("`योजना साथी`")
st.image(image, caption="योजना साथी")
st.info(
    "`नमस्ते! मैं हूँ  आपका AI साथी जो आपको देगा हर जानकारी सरकारी योजनाओ के विषय में (Hello! I am your AI companion who will provide you with information on government schemes)`"
)
st.markdown(
    f"""
    <style>
    .stTabs {{
        background: #ffffff10;
        padding: 8px 16px;
        border-radius: 4px;
    }}
    """,
    unsafe_allow_html=True
)

beneficiary_map = {
    "farmers": "किसान (Farmers)",
    "pregnant women": "गर्भवती महिलाएँ (Pregnant Women)",
    "students": "विद्यार्थी (Students)",
    "person with disability": "दिव्यांग व्यक्ति (Specially Abled Person)",
    "journalists": "पत्रकार (Journalist)",
    "SC/ST": "अनुसूचित जाति/अनुसूचित जनजाति (SC/ST)"
}

gender_map = {
    "None": "कोई नहीं (None)", 
    "male": "पुरुष (Male)",
    "female": "स्त्री (Female)",
    "others": "अन्य  (Others)",
}

category_map = {
    "None": "कोई नहीं (None)", 
    "SC": "अनुसूचित जाति (Scheduled Caste)",
    "ST": "अनुसूचित जनजाति  (Scheduled Tribes)",
    "OBC": "अन्य पिछड़ी जाति (Other backward classes)",
    "General": "सामान्य (General)",
}
st.subheader("User Information", divider="green")
with st.form("my_form"):
    beneficiary = st.selectbox(
        "लाभार्थी (Beneficiary): ", 
        tuple(beneficiary_map.keys()),
        format_func=lambda x: beneficiary_map[x]
    )
    st.divider()
    gender = st.selectbox(
        "Gender(Optional): ", 
        tuple(gender_map.keys()), 
        format_func=lambda x: gender_map[x]
    )
    category = st.selectbox(
        "Category (Optional): ",
        tuple(category_map.keys()),
        format_func=lambda x: category_map[x]
    )
    st.divider()
    language = st.radio("Language for Summary:", ["Hindi", "English"], horizontal=True)
    submitted = st.form_submit_button("भेजें  (Submit)")

if submitted:
    st.subheader("योजनाएं  (Schemes)", divider="green")
    filtered_df = df.loc[
        df.apply(lambda x: beneficiary in x["beneficiary"], axis=1)
    ]
    if gender != "None":
        filtered_df = filtered_df.loc[
            filtered_df.apply(
                lambda x: gender in x["gender"] or "any" in x["gender"], axis=1
            )
        ]
    if category != "None":
        filtered_df = filtered_df.loc[
            filtered_df.apply(
                lambda x: category in x["category"] or "any" in x["category"], axis=1
            )
        ]
    for idx, row in filtered_df.iterrows():
        if language == "English":
            st.markdown(row["summary"])
        else:
            st.markdown(row["hindi_summary"])
        st.divider()
