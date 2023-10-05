import streamlit as st
from image_to_text import image2text
from story_generation import generate_story
from text_to_speech import text2speech

def main():
    st.set_page_config(page_title="Visual Story Generator", page_icon="🧊", layout="centered", initial_sidebar_state="expanded")

    with st.sidebar:
        st.header("API Credentials")
        st.markdown("[Get a Hugging Face API Key](https://huggingface.co/Salesforce/blip-image-captioning-base)")
        hugging_face_key = st.text_input("Hugging Face API Key", type="password")
        st.markdown("[Get an OpenAI API Key](https://platform.openai.com/account/api-keys)")
        openai_key = st.text_input("OpenAI API Key", type="password")

    if not hugging_face_key or not openai_key:
        st.warning("Please enter valid API keys for both Hugging Face and OpenAI to proceed.")
        return

    st.header("Your Image into Audio Roast")
    uploaded_file = st.file_uploader("Choose an image...", type="jpg")

    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        st.image(bytes_data, caption='Uploaded Image.', use_column_width=True)

        # Save the uploaded image locally as a temporary file
        temp_image_path = "temp_uploaded_image.jpg"
        with open(temp_image_path, "wb") as f:
            f.write(bytes_data)

        with st.spinner("Converting image to text..."):
            scenario = image2text(temp_image_path)
        
        with st.spinner("Generating story..."):
            story = generate_story(scenario, openai_key)

        with st.spinner("Converting text to speech..."):
            text2speech(story, hugging_face_key)

        with st.expander("Scenario"):
            st.write(scenario)
        with st.expander("Story"):
            st.write(story)

        st.audio("audio.flac")

if __name__ == "__main__":
    main()
