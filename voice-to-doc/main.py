import os
from tempfile import NamedTemporaryFile

import assemblyai as aai
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from process_doc import process_extraction, process_qa

load_dotenv()

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
transcriber = aai.Transcriber()

audio = st.file_uploader("Upload an audio file", type=["mp3"])


def get_transcript():
    with NamedTemporaryFile(suffix="mp3") as temp:
        temp.write(audio.getvalue())
        temp.seek(0)
        transcript = transcriber.transcribe(temp.name)
        return transcript


def process_download(dataframe):
    doctype = st.radio("Choose file format", ["CSV (.csv)", "JSON (.json)"])
    if doctype == "CSV (.csv)":
        file = dataframe.to_csv(index=False)
        st.download_button("Download", data=file, file_name="streamlit_download.csv")
    elif doctype == "JSON (.json)":
        file = dataframe.to_json(orient="records")
        st.download_button("Download", data=file, file_name="streamlit_download.json")


if audio is not None:
    tab1, tab2 = st.tabs(["Extract", "Q&A"])

    with tab1:
        st.caption("Extract values from transcript.")
        obj = st.text_input("Object name e.g User, Food, Content etc.")
        labels = st.text_input("Enter the fields to extract separated by commas.")

        if st.button("Extract"):
            transcript = get_transcript()
            result = process_extraction(labels, obj, transcript.text)
            result_df = pd.DataFrame(result["data"])
            st.divider()
            st.button("Preview", on_click=st.dataframe, args=(result_df,))
            st.button("Save to File", on_click=process_download, args=(result_df,))

    with tab2:
        st.caption("Automatically create Question & Answers from transcript.")
        if st.button("Create"):
            transcript = get_transcript()
            result = process_qa(content=transcript.text)
            result_df = pd.DataFrame(result["data"])
            st.divider()
            st.button("Preview", on_click=st.dataframe, args=(result_df,))
            if st.button("Save to File"):
                doctype = st.radio("Choose file format", ["CSV (.csv)", "JSON (.json)"])
                if doctype == "CSV (.csv)":
                    file = result_df.to_csv(index=False)
                    st.download_button(
                        "Download", data=file, file_name="streamlit_download.csv"
                    )
                elif doctype == "JSON (.json)":
                    file = result_df.to_json(orient="records")
                    st.download_button(
                        "Download", data=file, file_name="streamlit_download.json"
                    )
