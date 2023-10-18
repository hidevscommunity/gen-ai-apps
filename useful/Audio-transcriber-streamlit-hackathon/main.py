import streamlit as st
import moviepy.editor as mp
from pytube import YouTube
from gtts import gTTS  # Import gTTS
from google.cloud import translate_v2 as translate
from pytube.exceptions import VideoUnavailable
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor

tran_api_key = "AIzaSyDcwA_3udNOCN1H88sxixc5R8sTeCnm2Xw"
translate_client = translate.Client.from_service_account_json("streamlit_hackathon.json")
import os
import assemblyai as aai
import tempfile


from textblob import TextBlob
import plotly.express as px
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

nltk.download('punkt')
nltk.download('stopwords')
# Streamlit app title and description
st.title("🔊Audio Transcriber 🖹 and Analysis Tool")
api_key= "aa664212223b421daca86e3ba24013dc"
aai.settings.api_key = api_key
st.markdown(
    " &#160; &#160; &#160;Made by Animesh | [LinkedIn](https://www.linkedin.com/in/animesh-singh11)| [website](https://share.streamlit.io/app/animesh11portfolio/)")

st.sidebar.image("Screenshot 2023-09-19 201338.png")
st.sidebar.header("About this App")
st.sidebar.write(
    """
    Welcome to the Audio Transcription and Analysis App. This tool uses LLM model to effortlessly transcribe audio content and analyze it..
    """
)
with st.sidebar.expander("Features💡"):
    st.write("""
        **Features:**

        - Transcript: Supports various audio formats. or upload video or upload audio file
        - Translation-text translation into any language
        - Listen Audio -Listen to transcribed text.
        - Text Summarization: summarize  text into concise content
        -  Sentiment Analysis: analyze sentiment of text  and get insights

        """)
with st.sidebar.expander("How it works  ❓️"):
    st.write("""
        **How it works ❓️**

        - Transcript the audio of video/audio file into text by using **LLM** assembly AI
        - Text translation into any language by using google Translate
        - Listen Audio -Listen to transcribed text.
        - summarize  text using pysummarization
        - analyze sentiments of text  and get insights using **textBlob** ,**nltk**


        """)
st.sidebar.markdown("<p style='color:red;'>*"
                    "Disclaimer: The accuracy of the transcription may vary depending on the audio quality and clarity of the video.*</p>"
                    , unsafe_allow_html=True
                    )


# Function to get a list of supported languages
def get_supported_languages():
    languages = translate_client.get_languages()
    language_dict = {lang['name']: lang['language'] for lang in languages}
    return language_dict


# Load the spaCy model
def keywords(text):
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalnum()]
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words and len(word) > 3]
    filtered_tokens = set(filtered_tokens)
    return filtered_tokens


supported_languages = get_supported_languages()


def text_to_speech(text):
    tts = gTTS(text)
    tts.save("audio.mp3")


# Function to perform sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    sentiment = analysis.sentiment
    return sentiment


# Function to visualize sentiment
def visualize_sentiment(sentiment):
    fig = px.bar(
        x=["Polarity", "Subjectivity"],
        y=[sentiment.polarity, sentiment.subjectivity],
        labels={"x": "Sentiment Metric", "y": "Value"},
        title="Sentiment Analysis Details",
        color_discrete_sequence=["blue", "red"],
    )
    return fig


def transcript_summar_voice(text):
    st.header("Transcription")
    # st.write(text)
    transcript_text = text
    try:
        # Translate the transcribed text to the target language
        translation = translate_client.translate(transcript_text,
                                                 target_language=supported_languages[target_language])
        translated_text = translation['translatedText']

        # Display the translated text
        st.write(translated_text)

        keywords_list = set(keywords(translated_text))

        # Combine transcript text and keywords into a single string
        combined_text = f"Transcript Text:\n{translated_text}\n\nKeywords:\n{', '.join(keywords_list)}"

        # Save the combined text to a temporary file
        with open("transcript_and_keywords.txt", "w", encoding="utf-8") as output_file:
            output_file.write(combined_text)

        # Create a download button for the combined transcript and keywords
        st.download_button(
            label="Download Transcript",
            data=combined_text.encode("utf-8"),
            file_name="transcript_and_keywords.txt",
            key="download_transcript_and_keywords",
        )
        st.header("Transcription keywords")
        st.warning("Note: Transcription keywords works well good in English")

        st.write(", ".join(keywords_list))
        st.header("Listen ")
        try:
            with st.spinner("Loading Audio"):
                text_to_speech(translated_text)
        except Exception as e:
            st.error("No Audio received: plz check if it has audio ")

        st.audio("audio.mp3")

        # Object of automatic summarization.
        try:
            auto_abstractor = AutoAbstractor()
            # Set tokenizer.
            auto_abstractor.tokenizable_doc = SimpleTokenizer()
            # Set delimiter for making a list of sentence.
            auto_abstractor.delimiter_list = [".", "\n"]
            # Object of abstracting and filtering document.
            abstractable_doc = TopNRankAbstractor()
            abstractable_doc.n = 2  # Set the number of sentences you want in the summary
            # Summarize document.
            result_dict = auto_abstractor.summarize(text, abstractable_doc)

            # Output result.
            lst = []
            for sentence in result_dict["summarize_result"]:
                lst.append(sentence)
            x = ''.join(lst)
            st.header("Summary")
            st.write(x)
            st.write(len(x))

            st.header("Sentiment Analysis")
            sentiment = analyze_sentiment(text)

            # Display sentiment analysis details with a plotly bar chart
            sentiment_fig = visualize_sentiment(sentiment)
            st.plotly_chart(sentiment_fig)

            # Provide a more detailed sentiment interpretation
            if sentiment.polarity > 0.2:
                st.write("😃 Very Positive Sentiment")
            elif 0.1 <= sentiment.polarity <= 0.2:
                st.write("🙂 Slightly Positive Sentiment")
            elif -0.2 <= sentiment.polarity < 0.1:
                st.write("😐 Neutral Sentiment")
            elif -0.2 <= sentiment.polarity < -0.1:
                st.write("🙁 Slightly Negative Sentiment")
            else:
                st.write("😔 Very Negative Sentiment")

            # Display subjectivity
            st.subheader("Subjectivity:")
            if sentiment.subjectivity >= 0.5:
                st.write("Highly Subjective")
            else:
                st.write("Somewhat Objective")
        except Exception as e:
            st.error("No text, make sure it has audio")
    except Exception as e:
        st.error("No text received make sure there is audio  " + str(e))
        st.success("")


def validate_youtube_link(link):
    try:
        yt = YouTube(link)
        video = yt.title
        return True
    except VideoUnavailable as e:
        st.warning(f"The YouTube video link is valid but the video is no longer available. Error: {str(e)}")
        return False
    except Exception as e:
        st.error(f"An error occurred while validating the YouTube link: {str(e)}")
        return False

option = st.selectbox("Select an option:",
                      ["Upload Audio File", "Upload Video to Extract Audio"])

if option == "Download from YouTube":
    # Input field for the YouTube video URL
    video_url = st.text_input("Enter YouTube video URL:")
    target_language = st.selectbox("Select target language for translation:", list(supported_languages.keys()))


    # Function to download the audio
    # Function to download the audio
    def download_audio(video_url):
        try:
            st.spinner("Downloading audio...")
            with st.spinner(text="Downloading audio..."):

                yt = YouTube(video_url)
                audio_stream = yt.streams.filter(only_audio=True).first()
                # Define the output directory and file name
                output_directory = "downloads"
                output_file_name = "sample.mp3"
                output_file_path = os.path.join(output_directory, output_file_name)

                audio_stream.download(output_path=output_directory, filename=output_file_name)

            st.spinner("Transcribing...")
            with st.spinner(text="Transcribing..."):
                transcriber = aai.Transcriber()
                transcript = transcriber.transcribe(output_file_path)

            if transcript and transcript.text:
                st.success("Transcription complete!")
                return transcript.text
            else:
                st.warning("Transcription resulted in an empty transcript.")

        except Exception as e:
            st.error("No Audio received: plz check if video has audio ")
            # Add additional logging if needed
            # Raise the exception for further debugging


    if st.button("Transcribe"):

        if validate_youtube_link(video_url):

            text = download_audio(video_url)
            transcript_summar_voice(text)


        else:
            st.warning("Please enter a valid YouTube video URL.")


elif option == "Upload Audio File":
    # File uploader for audio files
    uploaded_file = st.file_uploader("Upload an MP3 audio file:", type=["mp3"])
    target_language = st.selectbox("Select target language for translation:", list(supported_languages.keys()))


    # Function to save the uploaded audio file
    def save_uploaded_audio(uploaded_file):
        if uploaded_file:
            file_path = os.path.join("downloads", "sample.mp3")
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            # Show a spinner while transcription is in progress
            try:
                with st.spinner(text="Transcribing..."):
                    transcriber = aai.Transcriber()
                    transcript = transcriber.transcribe(file_path)
            except Exception as e:
                st.error("No text: plz check if file has audio ")
                if transcript and transcript.text:
                    st.success("Transcription complete!")
                    return transcript.text
                else:
                    st.error("No text: plz check if file has audio ")
                    return None
        else:
            return st.error("plz upload file")


    # Save button for uploaded audio
    if st.button("Transcribe "):
        text = save_uploaded_audio(uploaded_file)
        transcript_summar_voice(text)


else:
    # File uploader for video files
    uploaded_video = st.file_uploader("Upload a video to extract audio (MP4 format recommended):", type=["mp4"])
    target_language = st.selectbox("Select target language for translation:", list(supported_languages.keys()))


    # Function to extract audio from uploaded video
    def extract_audio_from_video(uploaded_video):
        if uploaded_video:
            temp_dir = tempfile.TemporaryDirectory()
            temp_path = os.path.join(temp_dir.name, uploaded_video.name)

            # Save the uploaded video file to the temporary location
            with open(temp_path, "wb") as temp_file:
                temp_file.write(uploaded_video.read())

            # Use moviepy to extract audio
            video_clip = mp.VideoFileClip(temp_path)
            audio_clip = video_clip.audio
            # Save the extracted audio as an MP3 file
            audio_path = os.path.join(temp_dir.name, "extracted_audio.mp3")
            audio_clip.write_audiofile(audio_path)

            st.spinner("Transcribing...")
            with st.spinner(text="Transcribing..."):
                transcriber = aai.Transcriber()
                transcript = transcriber.transcribe(audio_path)

            if transcript and transcript.text:
                st.success("Transcription complete!")
                st.success(transcript.text)

                return transcript.text
            else:
                st.warning("Transcription resulted in an empty transcript.")
        else:
            return st.error("plz upload file")


    # Extract button for uploaded video
    if st.button("Extract Audio from Uploaded Video"):
        text = extract_audio_from_video(uploaded_video)
        transcript_summar_voice(text)
