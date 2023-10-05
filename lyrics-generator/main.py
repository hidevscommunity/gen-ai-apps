import streamlit as st
import os
import assemblyai as aai
st.set_page_config("Lyrics generator","🎶",initial_sidebar_state="collapsed")


st.markdown("""<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
            </style><body style='background-color:#0f172a;'></body>""",unsafe_allow_html=True)




# AssemblyAI API Key
aai.settings.api_key = st.secrets["API_KEY"]
# Create a transcriber object.
transcriber = aai.Transcriber()
st.title("Lyrics Generator")
st.divider()
song = st.file_uploader("Upload a file", type=["mp3", "wav","audio/mpeg"])

if song :
    # Get the file name
    file_name = song.name

    # Save the uploaded file to a local directory
    with open(file_name, "wb") as f:
        f.write(song.read())

    st.success(f"File '{file_name}' saved successfully!")


def generate_lyrics(obj):
    transcript = transcriber.transcribe(obj)
    st.write(transcript.text)

button = st.columns(3)[1].button("Generate")
if button:
    if song :
        st.text(f"Song name : {song.name}")
        st.audio(song.name)
    # generate_lyrics()
        st.text("Generating Lyrics ...")
        st.divider()
        transcript = transcriber.transcribe(song.name)
        st.write(transcript.text)
        os.remove(song.name)
    else:
        st.warning("Please upload a file first")
