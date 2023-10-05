import streamlit as st
from streamlit_player import st_player
from pytube import YouTube
from aai import summarize_video, generate_subtitle
from llm_model import init_llama_response
import os


st.set_page_config(
    page_title="ClipInsight",
    page_icon="📺"
)

def download_video(url):
    yt = YouTube(url)
    audio = yt.streams.filter(only_audio=True).first()
    file = audio.download()
    base, ext = os.path.splitext(file)
    file_name = base + '.mp3'
    os.rename(file, file_name)
    return file_name

def get_button_text(start_ms):
    seconds = int((start_ms/1000) % 60)
    minutes = int((start_ms/(1000 * 60)) % 60)
    hours = int((start_ms/(1000 * 60 * 60)) % 24)
    btn_txt = ''
    if hours > 0:
        btn_txt += f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        btn_txt += f'{minutes:02d}:{seconds:02d}'
    return btn_txt

placeholder = st.empty()
def addButton(start_ms, url):
    start_s = start_ms/1000
    if st.button(get_button_text(start_ms)):
        url_time = url + '&t=' + str(start_s) + 's'
        st_player(url_time)

def main():
    st.title("ClipInsight - Video Summarizer 🎥")
    st.markdown('<style>h1{text-align:center;} </style>', unsafe_allow_html=True)
    
    # About Section - tell users what this webapp is all about
    with st.sidebar.expander('**About**'):
        st.markdown("""
            - Introducing our innovative platform, the ultimate companion for YouTube enthusiasts! 🚀 Unlock a world of convenience as you effortlessly access chapter summaries and highlights with precise timestamps, making video navigation a breeze.
            - But that's not all! 📚🕐 Dive deeper into video content with our interactive chat feature, empowering you to uncover hidden gems and engage with the material like never before. 
            - Discover, explore, and enjoy YouTube in a whole new way with our all-in-one YouTube Companion! 🌟""")
    
    # Functionality to generate summary of key chapters/highlights of any video on passing its youtube url
    with st.sidebar.form(key='my_form'):
        st.markdown("**Generate Summary**")
        youtube_url = st.text_input("Youtube Video URL")
        submit_button = st.form_submit_button(label='Go')
    
    if submit_button and youtube_url:
        with st.status("Transcribing Video...", expanded=True) as status:
            st.write('📥 Downloading data...')
            file_path = download_video(youtube_url)
            st.write('🚀 Transcribing underway...Stay with us.')
            transcript, chapters = summarize_video(file_path)
            st.session_state['transcript'] = transcript
            st.session_state['chapters'] = chapters
            st.write("🎤 Ta-da! Transcription's done!")
            st.toast("🎤 Ta-da! Transcription's done!")
            st.session_state.messages.append({"role": "assistant","content":chapters})   
            status.update(label="Transcription completed! 🎉", state="complete", expanded=False) 
    
    # Functionality to generate subtitle file (as .srt)
    # with st.sidebar.expander('**Generate Subtitle**'):
    #     url = st.text_input("Enter Youtube Video URL")
    #     if url:
    #         st.toast("🎙️ Capturing Audio Magic...")
    #         file = download_video(url)
    #         st.toast("🚀 Transcribing Whispers...")
    #         file_path = generate_subtitle(file)
    #         st.toast("✨ Transforming Words into Subtitles...")
    #         read_file = open(file_path,'r')
    #         st.toast("📦 Subtitles Ready for the Spotlight!")
    #         st.download_button(label="Download", data=read_file, file_name= "generated_subtitle.srt",mime='text/plain')
            
    
    # An example youtube url to test the webapp for video summarization
    with st.sidebar.expander('**Example URL**'):
        st.code('https://www.youtube.com/watch?v=R2nr1uZ8ffc')
    
    # clear chat history
    def clear_chat_history():
        st.session_state.messages = []
        st.session_state['chapters'] = []
    st.sidebar.button("Clear Chat History", on_click=clear_chat_history)

    if "chapters" in st.session_state:
        with st.chat_message("assistant"):
            for chapter in st.session_state['chapters']:
                addButton(chapter.start, youtube_url)
                st.subheader(chapter.gist)
                st.markdown(chapter.summary)

    if "messages" not in st.session_state.keys():
        st.session_state.messages = []
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Send your message", disabled=not st.session_state.messages):
        st.session_state.messages.append({"role": "user","content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)        
        
    
    # Generate a new response if last message is not from assistant
    if st.session_state.messages and st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = init_llama_response(st.session_state['transcript'], prompt)
                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)

if __name__ == "__main__":
    main()

