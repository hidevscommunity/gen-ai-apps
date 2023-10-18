import streamlit as st
import utils as ut
from google.cloud import storage
from google.oauth2 import service_account

st.set_page_config(page_title='ACW Playground', layout='wide')
ut.add_logo()
ut.set_acw_header("ACW - Playground")

# st.expander label font change
st.markdown("""
  <style>
    div[data-testid="stExpander"] div[role="button"] p {
    font-size: 20px;
    }
    .st-c8:hover {
    color: #3371FF !important;
    }
  </style>
""", unsafe_allow_html=True)

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["secrets-gcp"]
)

file_upload_container = st.expander("Upload an audio file to see ACW in action", expanded=False)
with file_upload_container:
    uploaded_file = st.file_uploader(type=['wav', 'mp3', 'm4a', 'ogg'], label="Upload here", label_visibility="collapsed")

custom_file_container = st.expander("Do not have the audio file for testing? Download one of the following sample audio files for testing.*", expanded=False)
with custom_file_container:
    # st.markdown("<br/><h6 style='text-align: left;'>Do not have the audio file for testing? Test using one of the following sample audio files</h6>", unsafe_allow_html=True)
    # positive_clicked = st.markdown("""<a href="Upload_File" target="_self">Download Positive Sentiment Audio File</a>""", unsafe_allow_html=True)
    # neutral_clicked = st.markdown("""<a href="Upload_File" target="_self">Download Neutral Sentiment Audio File</a>""", unsafe_allow_html=True)
    # negative_clicked = st.markdown("""<a href="Upload_File" target="_self">Download Negative Sentiment Audio File</a>""", unsafe_allow_html=True)

    st.markdown("Positive Sentiment Audio File")
    pos_file = open('audio/positive_sentiment.m4a', "rb") # opening for [r]eading as [b]inary
    pos_data = pos_file.read() # if you only wanted to read 512 bytes, do .read(512)
    pos_file.close()
    dg = st.audio(pos_data, format="audio/wav")

    st.markdown("Neutral Sentiment Audio File")
    neu_file = open('audio/neutral_sentiment.m4a', "rb")
    neu_data = neu_file.read()
    neu_file.close()
    st.audio(neu_data, format="audio/mp3")

    st.markdown("Negative Sentiment Audio File")
    neg_file = open('audio/negative_sentiment.m4a', "rb")
    neg_data = neg_file.read()
    neg_file.close()
    st.audio(neg_data, format="audio/mp3")
    
    disclaimer = '<p style="color:Grey; font-size: 10px;">(*) Please note that this is a sample recording only for demo and testing purpose.</p>'
    st.markdown(disclaimer, unsafe_allow_html=True)


    # st.markdown(ut.file_download('positive_sentiment.m4a', 'audio/positive_sentiment.m4a' , 'Download Positive Sentiment Audio File'), unsafe_allow_html=True)
    # st.markdown(ut.file_download('neutral_sentiment.m4a', 'audio/neutral_sentiment.m4a' , 'Download Neutral Sentiment Audio File'), unsafe_allow_html=True)
    # st.markdown(ut.file_download('negative_sentiment.m4a', 'audio/negative_sentiment.m4a' , 'Download Negative Sentiment Audio File'), unsafe_allow_html=True)


storage_client = storage.Client(credentials=credentials)
bucket = storage_client.bucket("call-recordings-genai")

if uploaded_file is not None:
    # Hide filename on UI
    st.markdown('''<style>.uploadedFile {display: none}<style>''', unsafe_allow_html=True)
    original_title = '<p style="color:Green; font-size: 20px; font-weight: bold;">Successfully uploaded \'{filename}\'! After processing, the new ACW record will be available <a style="font-weight: normal;" href="ACW_Records" target="_self">here</a>.</p>'.format(filename = uploaded_file.name)
    st.markdown(original_title, unsafe_allow_html=True)

    blob = bucket.blob(uploaded_file.name)
    blob.upload_from_file(uploaded_file)

ut.add_footer()