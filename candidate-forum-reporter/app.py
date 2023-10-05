import assemblyai as aai
import pandas as pd
import streamlit as st
import yt_dlp

aai.settings.api_key = st.secrets.assembly_ai.token

### If not using secrets, use this code to have user enter their own API key
# # If the user hasn't set their API key in the secrets.toml file, ask them to enter it
# if not aai.settings.api_key:
#     with st.sidebar:
#         aai.settings.api_key = st.text_input(
#             label="Paste your AssemblyAI API key here", type="password"
#         )


### Functions ###
def download_yt_audio(url, output_filename):
    """Download a local copy of the mp3 from a YouTube video"""
    ydl_opts = {
        "format": "bestaudio/best",
        "verbose": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": output_filename,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(url)
        return error_code


def transcribe_audio(audio_file):
    """Take audio file that has been downloaded locally
    and send it to AssemblyAI to be transcribed into a transcript.
    Transcript returned includes the summary and categories.
    """
    config = aai.TranscriptionConfig(
        summarization=True,
        summary_model=aai.SummarizationModel.informative,
        summary_type=aai.SummarizationType.bullets_verbose,
        iab_categories=True,
        #  dual_channel=True,
    )
    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(audio_file)
    return transcript


######


### Streamlit UI Flow

st.title(":ledger: Candidate Forum Reporter")
st.write("Elections are coming up!  Missed your city government forum last night?")
st.markdown(
    """
    * Get a summary of the meeting
    * Understand quickly which local issues are being discussed 
    * Read a full transcript of the meeting
    """
)
st.header("")

st.caption("Paste the forum's URL from YouTube")

# User inputs the YouTube video URL and video gets displayed
default_url = "https://www.youtube.com/watch?v=HsbwLxBKrLk"
forum_url = st.text_input(
    label="Paste the YouTube URL",
    label_visibility="collapsed",
    value=default_url,
)

if forum_url:
    st.video(forum_url)

if st.button(
    label="Summarize the meeting",
    type="primary",
):
    # Download the audio from the YouTube video
    # If successful, transcribe the meeting and create a summary
    with st.spinner("Analyzing the video..."):
        error_code = download_yt_audio(forum_url, "downloaded_audio")
        print(error_code)
        if error_code == 0:
            transcript = transcribe_audio("downloaded_audio.mp3")
            if transcript:
                print(transcript)
                st.caption("Meeting summary:")
                st.write(transcript.summary)
                st.caption("Top issues covered:")
                # Create a dataframe of the top 10 issues discussed
                category_df = pd.DataFrame.from_dict(
                    transcript.iab_categories.summary,
                    orient="index",
                    columns=["relevance"],
                )[:10]
                st.table(category_df)
                with st.expander("Transcript"):
                    st.write(transcript.text)
            else:
                st.error("That video isn't available. Try a different one.")
        else:
            st.error("That video isn't available. Try a different one.")

st.divider()

# Show information about how to vote
link = "https://vote.gov/"
st.markdown(
    f'<a href="{link}" style="display: inline-block; padding: 12px 20px; background-color: #428bca; color: white; text-align: center; text-decoration: none; font-size: 16px; border-radius: 4px;">Find out more about voting</a>',
    unsafe_allow_html=True,
)
