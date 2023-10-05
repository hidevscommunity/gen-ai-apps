import websockets
import asyncio
import base64
import json
import pyaudio
import streamlit as st

#import sys
#sys.setrecursionlimit(4000)


if 'run' not in st.session_state:
    st.session_state['run'] = False

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

auth_key = st.secrets["api-key"]

def start_listening():
    st.session_state['run'] = True

def stop_listening():
    st.session_state['run'] = False

st.title('Realtime Transcription')
st.write('*English only')
st.write("Sample Audio [HERE](https://storage.googleapis.com/aai-web-samples/meeting.mp4)")

start, stop = st.columns(2)
start.button('Start Listening', on_click=start_listening)
stop.button('Stop Listening', on_click=stop_listening)

# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

async def send_receive():
    print(f'Connecting websocket to url {URL}')
    async with websockets.connect(
            URL,
            extra_headers=(("Authorization", auth_key),),
            ping_interval=5,
            ping_timeout=20
    ) as _ws:
        # Open PyAudio stream here
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER
        )

        print("Receiving SessionBegins ...")
        session_begins = await _ws.recv()
        print(session_begins)
        print("Sending messages ...")

        async def send():
            while st.session_state['run']:
                try:
                    data = stream.read(FRAMES_PER_BUFFER)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data": str(data)})
                    await _ws.send(json_data)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                await asyncio.sleep(0.01)

        async def receive():
            while st.session_state['run']:
                try:
                    result_str = await _ws.recv()
                    if json.loads(result_str)["message_type"] == 'FinalTranscript':
                        print(convert_text(json.loads(result_str)['text']))
                        st.markdown(convert_text(json.loads(result_str)['text']))
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break

        send_task = asyncio.create_task(send())
        receive_task = asyncio.create_task(receive())

        await asyncio.gather(send_task, receive_task)

        # Close PyAudio stream
        stream.stop_stream()
        stream.close()

        # Terminate PyAudio
        p.terminate()

st.experimental_rerun()
st.experimental_asyncio(send_receive())