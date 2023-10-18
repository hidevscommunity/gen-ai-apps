import streamlit as st
import assemblyai as aai

# Set the page title and icon
st.set_page_config(
    page_title="Audio to Text Converter",
    page_icon="🎤",
    layout="centered",
)

def speech_to_text(url="https://storage.googleapis.com/aai-web-samples/espn-bears.m4a"):
    # Your API token is already set here
    aai.settings.api_key = "e07462fd4cdb4f7e9438eca3a14b8de9"

    # Create a transcriber object.
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(url)

    # After the transcription is complete, the text is returned.
    return transcript.text

# Define the Streamlit app
def main():
    st.title("Audio to Text Converter")

        # Summary message explaining the functionality
    st.markdown(
        """
        This web app allows you to convert audio to text using AssemblyAI's automatic speech recognition (ASR) technology.
        Simply enter the URL of the audio you'd like to convert, click the "Convert" button, and the app will transcribe 
        the audio and display the text.
        """
    )
    
    # Text input for audio URL
    audio_url = st.text_input("Enter Audio URL:", "https://storage.googleapis.com/aai-web-samples/espn-bears.m4a")
    
    # Button to trigger text conversion
    if st.button("Convert"):
        with st.spinner("Converting..."):
            converted_text = speech_to_text(url=audio_url)
        
        st.success("Conversion complete!")  # Show a success message
        
        if audio_url and converted_text != None:
            # Display the converted text
            st.subheader("Converted Text:")
            st.write(converted_text)
        else:
            st.warning("Please enter an audio URL.")

if __name__ == "__main__":
    main()
