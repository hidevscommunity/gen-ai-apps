import streamlit as st
from streamlit_lottie import st_lottie
from textblob import TextBlob
import requests
import json
import base64

# =============================================================================
# SVG BOOTSTRAP ICONS
# =============================================================================  
download_icon = """<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">
  <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
  <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
</svg>
"""

balloon_heart_icon = """
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-balloon-heart" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="m8 2.42-.717-.737c-1.13-1.161-3.243-.777-4.01.72-.35.685-.451 1.707.236 3.062C4.16 6.753 5.52 8.32 8 10.042c2.479-1.723 3.839-3.29 4.491-4.577.687-1.355.587-2.377.236-3.061-.767-1.498-2.88-1.882-4.01-.721L8 2.42Zm-.49 8.5c-10.78-7.44-3-13.155.359-10.063.045.041.089.084.132.129.043-.045.087-.088.132-.129 3.36-3.092 11.137 2.624.357 10.063l.235.468a.25.25 0 1 1-.448.224l-.008-.017c.008.11.02.202.037.29.054.27.161.488.419 1.003.288.578.235 1.15.076 1.629-.157.469-.422.867-.588 1.115l-.004.007a.25.25 0 1 1-.416-.278c.168-.252.4-.6.533-1.003.133-.396.163-.824-.049-1.246l-.013-.028c-.24-.48-.38-.758-.448-1.102a3.177 3.177 0 0 1-.052-.45l-.04.08a.25.25 0 1 1-.447-.224l.235-.468ZM6.013 2.06c-.649-.18-1.483.083-1.85.798-.131.258-.245.689-.08 1.335.063.244.414.198.487-.043.21-.697.627-1.447 1.359-1.692.217-.073.304-.337.084-.398Z"/>
</svg>
"""

# =============================================================================
# HTML / CSS STYLING OF FLIPCARD
# =============================================================================   
def img_to_html(img_url):
    response = requests.get(img_url)
    encoded = base64.b64encode(response.content).decode()
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(encoded)
    return img_html

def create_flipcard(image_path_front_card=None, image_path_back=None, font_size_back='10px', my_header='', **kwargs):
    # Convert the image URLs to HTML image elements
    front_image_html = img_to_html(image_path_front_card)
    back_image_html = img_to_html(image_path_back)

    # Create empty list that will keep the HTML code needed for each card with header+text
    card_html = []

    # Append HTML code to list
    card_html.append(f"""
        <div class="flashcard">
            <div class='front'>
                {front_image_html}
            </div>
            <div class="back">
                {back_image_html}
                <style>
                /* Apply Open Sans font to paragraphs and lists */
                .back p, .back ul, .back ol, .back li, .back h2 {{
                    font-family: 'Open Sans', sans-serif;
                }}
                </style>
                <h2>Claudio - Audio to Text Transcript Application</h2>
                <p><strong>Description:</strong> Claudio is a user-friendly application for converting audio files to text transcripts. It is hosted using Streamlit and relies on the AssemblyAI API for audio transcription. Claudio provides additional functionalities, including text summarization, question and answer text corpus, and sentiment analysis.</p>
                <br>
                <h2>Key Features:</h2>
                <ul>
                    <li><strong>Audio Upload:</strong> Users can upload audio files in MP3 format for transcription.</li>
                    <li><strong>Transcription:</strong> The application sends the audio file to the AssemblyAI API for transcription, displaying the transcript.</li>
                    <li><strong>Sentiment Analysis:</strong> Claudio provides sentiment analysis for the transcribed text, showing the emotional tone.</li>
                    <li><strong>Text Summarization:</strong> Users can generate a summary of the transcribed text, making it easier to grasp the content.</li>
                    <li><strong>Question and Answer:</strong> Users can ask questions about the transcribed text, and Claudio attempts to provide relevant answers.</li>
                    <li><strong>API Key:</strong> Users need to enter their AssemblyAI API key to use the transcription feature.</li>
                </ul>
                <h2>How to Use:</h2>
                <ol>
                    <li>Enter your AssemblyAI API key (or retrieve one from the <a href="https://www.assemblyai.com">AssemblyAI website</a>).</li>
                    <li>Upload an MP3 audio file for transcription.</li>
                    <li>Claudio will transcribe the audio and display the text in real-time.</li>
                    <li>Explore additional features like sentiment analysis, text summarization, and question-answering.</li>
                </ol>
                <h2>Special Thanks</h2>
                <p>I would like to express my heartfelt appreciation to the <b>Streamlit</b>, <b>AssemblyAI</b>, and <b>Hugging Face</b> teams and communities for their exceptional platforms. In particular <b>Misra Turp</b> and <b>Chanin Nantasenamat</b> for their invaluable knowledge sharing {balloon_heart_icon}</p>
            </div>
        </div>
    """)
    # Join all the HTML code for each card and join it into a single HTML code with carousel wrapper
    carousel_html = "<div class='flipcard_stats'>" + "".join(card_html) + "</div>"
    # Display the carousel in Streamlit
    st.markdown(carousel_html, unsafe_allow_html=True)
    # Create the CSS styling for the carousel
    st.markdown(
        f"""
        <style>
        .flipcard_stats {{
          display: flex;
          justify-content: center;
          overflow-x: auto;
          scroll-snap-type: x mandatory;
          scroll-behavior: smooth;
          -webkit-overflow-scrolling: touch;
          width: 100%;
        }}
        .flashcard {{
          width: 600px;
          height: 600px;
          background-color: white;
          border-radius: 0px;
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
          perspective: 100px;
          margin-bottom: 10px;
          scroll-snap-align: center;
        }}
        .front, .back {{
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          border-radius: 0px;
          backface-visibility: hidden;
          font-family: 'Ysabeau SC', sans-serif;
          text-align: center;
        }}
        .front {{
          color: white;
          transform: rotateY(0deg);
        }}
        .front img, .back img {{
          max-width: 100%;
          max-height: 100%;
          object-fit: contain; /* Ensure the image fits without distortion */
        }}
        .back {{
          color: #333333;
          background-color: #fdda57;
          transform: rotateY(180deg);
          display: block;
          justify-content: flex-start;
          margin: 0;
          padding: 60px;
          text-align: left;
          text-justify: inter-word;
          overflow: auto;
        }}
        .back h2 {{
          margin-bottom: 0px;
          margin-top: 0px;
        }}
        .flashcard:hover .front {{
          transform: rotateY(180deg);
        }}
        .flashcard:hover .back {{
          transform: rotateY(0deg);
        }}
        .back p {{
          margin: -10px 0;
          font-size: {font_size_back};
        }}
        footer {{
          text-align: left;
          margin-top: 20px;
          font-size: 12px;
          margin-bottom: 20px;
        }}
        </style>
        """, unsafe_allow_html=True)

# =============================================================================
# FUNCTIONS FOR STREAMLIT
# =============================================================================   
def vertical_spacer(n):
    for i in range(n):
        st.write("")
        
def show_lottie_animation(url, key, reverse=False, height=400, width=400, speed=1, loop=True, quality='high', col_sizes=[1, 3, 1], margin_before = 0, margin_after = 0):
    with open(url, "r") as file:
        animation_url = json.load(file)

    col1, col2, col3 = st.columns(col_sizes)
    with col2:
        vertical_spacer(margin_before)
        
        st_lottie(animation_url,
                  reverse=reverse,
                  height=height,
                  width=width,
                  speed=speed,
                  loop=loop,
                  quality=quality,
                  key=key
                  )
        vertical_spacer(margin_after)
        
# Function to convert seconds to hh:mm:ss format
def seconds_to_hhmmss(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    
# =============================================================================
# Sentiment Analysis Test
# =============================================================================
def get_sentiment(text):
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity
    return sentiment_score
    
def read_file(filename):
    CHUNK_SIZE = 5242880
    with open(filename, 'rb') as _file:
        while True:
            
            data = _file.read(CHUNK_SIZE)
            if not data:
                break
            yield data
            
# =============================================================================
# AssemblyAI
# =============================================================================
# Function to save audio data in session state
def save_audio_data(audio_data):
    st.session_state.audio_data = audio_data
    
# Function to get audio data from session state
def get_audio_data():
    return st.session_state.get("audio_data", None)
    
    
def read_file(filename):
    CHUNK_SIZE = 5242880
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(CHUNK_SIZE)
            if not data:
                break
            yield data
            
def upload_audio_to_assemblyai(api_key, audio_file):
    transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
    upload_endpoint = 'https://api.assemblyai.com/v2/upload'
    headers = {
        "authorization": api_key
    }

    # Upload audio file to AssemblyAI
    try:
        #upload_response = requests.post(upload_endpoint, headers=headers, data = uploaded_file[0].read())
        upload_response = requests.post(upload_endpoint, headers=headers, data = audio_data)
        audio_url = upload_response.json()['upload_url']
        return audio_url
    except:
        pass
        
        
        
        