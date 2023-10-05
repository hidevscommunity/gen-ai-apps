# Streamlit Widget Components
import streamlit as st
from streamlit_webrtc import webrtc_streamer
from st_audiorec import st_audiorec

# Python built-in modules
from collections import Counter
from io import BytesIO
import threading
import os

# Computer Vision and Image Processing
import cv2
from deepface import DeepFace # emotion recognition

# TTS and STT
from gtts import gTTS # text to speech
import assemblyai as aai # speech to text

# LLMs
from langchain.llms import Clarifai # GPT-4
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chains import LLMChain

# Heart Metric Calculation
from helpers import HeartMetricsCalculator

# TURN Server for StreamlitWebRTC
from twilio.rest import Client



# Load Prompt Templates and Instructions
with open('text/system_role.txt', 'r') as f:
    system_role = f.read()

with open('text/human_template.txt', 'r') as f:
    human_template = f.read()

with open('text/instructions.txt', 'r') as f:
    instructions = f.read()

llm_prompt = ChatPromptTemplate.from_messages([
    ("system", system_role),
    ("human", human_template),
])

# Initialize Objects
llm_model = Clarifai(pat=st.secrets['ClarifaiToken'], user_id='openai', 
                   app_id='chat-completion', model_id='GPT-4')

llm_chain = LLMChain(llm=llm_model, prompt=llm_prompt, verbose=True)

aai.settings.api_key = st.secrets['AssemblyAIToken']
transcriber = aai.Transcriber()

heart_calculator = HeartMetricsCalculator()

# Connect TURN Server
client = Client(st.secrets['TwilioAccountSID'], st.secrets['TwilioAuthToken'])
token = client.tokens.create()

# Initialize threading and session states
lock = threading.Lock()
img_container = {'image': None}

if 'tracker' not in st.session_state:
    st.session_state.tracker = {'roi_frames': [], 'emotion': []}

if 'report' not in st.session_state:
    st.session_state.report = {'emotion': {}, 'heart': {}}

# video feed subthread
def process_feed(frame):
    with lock:
        img_container['image'] = frame.to_ndarray(format="bgr24")
    return frame

# generate emotion report
def count_percent(labels):
    label_counts = Counter(labels)
    total_labels = len(labels)
    label_percent = {}

    for label, count in label_counts.items():
        percentage = (count / total_labels) * 100
        label_percent[label] = round(percentage)

    return label_percent

# display tracking reports
def display_emotion_report():
    emotion_report = st.session_state.report['emotion']
    st.subheader('Percentage of different emotions observed during monitoring')

    cols = st.columns(len(emotion_report.keys()))
    for i, (emo, percent) in enumerate(emotion_report.items()):
        cols[i].metric(emo, f'{percent}%')

def display_heart_report():
    heart_report = st.session_state.report['heart']
    st.subheader('Heart Metric Report')

    st.write(f"Estimated Heart Rate: **{heart_report['heart_rate']}** BPM")
    st.write(f"HRV: **{heart_report['sdnn']}**: A measure of heart rate variability, indicating the overall variability in heartbeats")
    st.write(f"RMSSD: **{heart_report['rmssd']}**: A measure of parasympathetic nervous system activity")
    st.write(f"Baevsky Stress Index (BSI): **{heart_report['bsi']}**: Stress level based on heart rate variability.")
    st.write(f"LF/HF Ratio: **{heart_report['lf_hf_ratio']}**: Balance between sympathetic and parasympathetic nervous system activity.")
    st.write(f"Click counseling tab above to get detailed report")

# Build UI
st.set_page_config('EmoPulse')
st.title('EmoPulse')

with st.expander('Instructions'):
    st.write(instructions)

monitor_tab, counsel_tab = st.tabs(['Monitoring', 'Counseling'])

with monitor_tab:
    st.info('Record for minimum 1 min. Emotion Recognition and Pulse Signal Processing are still in BETA stage, so it may present some inaccuracies')
    stream = webrtc_streamer(key="stream", video_frame_callback=process_feed,
                            media_stream_constraints={'video': True, 'audio': False},
                            rtc_configuration={"iceServers": token.ice_servers}
                            )
    
    # Live UI output
    display = st.empty()

    while stream.state.playing:
        # Get image from subthread
        with lock:
            image = img_container['image']
        if image is not None:
            try: 
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # Run Emotion Recognition
                faces = DeepFace.analyze(img_path = image, actions = ['emotion'],
                                        detector_backend='ssd', silent=True)

                if len(faces) == 1:
                    box = faces[0]['region']
                    emo = faces[0]['dominant_emotion']

                    x1, y1, w, h = box['x'], box['y'], box['w'], box['h']
                    x2, y2 = x1 + w, y1 + h

                    # Calculate forehead region coordinates
                    roi_y1 = y1 + (h // 8)
                    roi_y2 = y1 + (h // 4)
                    roi_x1 = x1 + (w // 3)
                    roi_x2 = x2 - (w // 3)

                    # Extract green channel
                    forehead = image[roi_y1:roi_y2, roi_x1:roi_x2, 1]

                    # Cropping and annotation for display
                    cv2.rectangle(image, (roi_x1, roi_y1), (roi_x2, roi_y2), (255, 0, 0), 2)
                    face = image[y1:y2, x1:x2]

                    display.image(image=face, caption=emo)

                    # Track emotion and save forehead frames for post-processing
                    st.session_state.tracker['roi_frames'].append(forehead)
                    st.session_state.tracker['emotion'].append(emo)

                else:
                    display.warning('Multiple Faces Detected!')
            
            except ValueError:
                display.warning('No Face Detected!')

    # Generate and save reports if data is sufficient
    if st.session_state.tracker['roi_frames']:
        emo_percent = count_percent(st.session_state.tracker['emotion'])
        st.session_state.report['emotion'] = emo_percent
        try:
            avg_heart_rate, sdnn, rmssd, bsi, lf_hf_ratio = heart_calculator.estimate_heart_rate(st.session_state.tracker['roi_frames'])
            st.session_state.report['heart'] = {
                                                    "heart_rate": round(avg_heart_rate, 2),
                                                    "sdnn": round(sdnn, 2),
                                                    "rmssd": round(rmssd, 2),
                                                    "bsi": round(bsi, 2),
                                                    "lf_hf_ratio": round(lf_hf_ratio, 2)
                                                }
        except ValueError:
            st.warning('Heart Metrics cannot be generated due to lack of Pulse Data')
    
    if st.session_state.report['emotion']:
        display_emotion_report()
        
    if st.session_state.report['heart']:
        display_heart_report()


with counsel_tab:
    # User can choose what data to include in LLM prompt
    if st.session_state.report['heart']:
        useHeart = st.toggle('Send Heart Metrics Report?')
        with st.expander('Heart Metrics Report'):
            display_heart_report()
    else:
        useHeart = False
        st.info('Heart Metrics Report not Available!')

    if st.session_state.report['emotion']:
        useEmotion = st.toggle('Send Emotion Tracking Report?')
        with st.expander('Emotion Tracking Report'):
            display_emotion_report()
    else:
        useEmotion = False
        st.info('Emotion Tracking Report not Available!')
    
    personalize = st.toggle('Personalize information?')
    if personalize:
        with st.expander('Personalization'):
            name = st.text_input('Name')
            age = st.number_input('Age', 1, 100)
            gender = st.radio('Gender', ['Male', 'Female'], horizontal=True)

        p_info = f'Name: {name}; Age: {age}; Gender: {gender}'

    tell = st.toggle("Tell me what's on your mind?")
    user_input = "" 
    if tell:
        with st.expander('User Input'):
            mode = st.radio('Mode', ['Speak', 'Type'])
            if mode == 'Speak':
                # Build custom audio recorder widget
                audio_bytes = st_audiorec()
                if audio_bytes:
                    file_name = 'temp_transcript.wav'
                    # Save audio to temp file
                    with open(file_name, "wb") as f:
                        f.write(audio_bytes)
                    
                    # speech to text
                    user_input = transcriber.transcribe(file_name).text
                    st.write(user_input)
                    os.remove(file_name)

            else:
                user_input = st.text_area('Text to Analyze')

    # If minimum options selected
    if useEmotion or useHeart or tell:
        counsel = st.button('Counsel')
        if counsel:
            wait = st.empty()
            wait.info("We are working on your report... your patience is highly appreciated.")

            # Await response from LLM
            response = llm_chain.run(
                emotion_report=st.session_state.report['emotion'] if useEmotion else None,
                heart_report=st.session_state.report['heart'] if useHeart else None,
                p_info=p_info if personalize else None,
                thoughts=user_input if tell else None,
            )
            
            wait.empty()
            st.write(response)

            # Text to Speech
            speech_bytes = BytesIO()
            tts = gTTS(response)
            tts.write_to_fp(speech_bytes)
            st.audio(speech_bytes)
