import pyaudio
import streamlit as st
st.title('available audio device')
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    st.write(f"Device {i}: {info['name']}")
