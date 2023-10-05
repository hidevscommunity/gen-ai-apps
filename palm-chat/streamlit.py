import streamlit as st
import google.generativeai as palm
# from dotenv import load_dotenv
import os
from gtts import gTTS
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import fonts
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO

# load_dotenv()
api_key = os.getenv("PALM_MODEL_API")
pdfmetrics.registerFont(TTFont('kg-broken-vessels-sketch.regular', 'kg-broken-vessels-sketch.regular.ttf'))

palm.configure(api_key=api_key)

defaults = {
  'model': 'models/chat-bison-001',
  'temperature': 0.95,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
}

context = "You are VoxAura, Please be polite because kid is using for learn, give accurate information, be helpful and explain details."
examples = [
  [
    "what is your name?",
    "my name is VoxAura."
  ],
  [
    "Hi!",
    "Hi, my name is VoxAura."
  ],
  [
    "what is world war 1?",
    "World War I, also known as the First World War, was a global war originating in Europe that lasted from 28 July 1914 to 11 November 1918. Contemporaneously described as \"the war to end all wars,\" it led to the mobilisation of more than 70 million military personnel, including 60 million Europeans, making it one of the largest wars in history. Over 16 million people died, including 9.7 million Europeans, and an additional 7.9 million were wounded. Tens of millions of people died due to genocides (including the Armenian genocide), premeditated death from starvation, massacres, and disease. Aircraft played a major role in the conflict, including in strategic bombing of population centers, the development of tanks, the use of poison gas, and the first large-scale use of aircraft in combat. \r\n\r\nThe assassination of Archduke Franz Ferdinand of Austria by Gavrilo Princip on 28 June 1914 was the trigger that set off a chain of events leading to the war. Serbia's allies, Russia and France, and Austria-Hungary's ally, Germany, were drawn into the conflict. Within weeks, the major powers of Europe were at war. The Central Powers—Germany, Austria-Hungary, the Ottoman Empire, and Bulgaria—became known as the \"Central Powers,\" while the Entente Powers—Russia, France, Britain, Italy, Japan, and the United States—became known as the \"Entente Powers.\"\r\n\r\nThe war ended with the signing of the Armistice of 11 November 1918. The Treaty of Versailles, signed on 28 June 1919, formally ended the war between Germany and the Allied Powers. The war had a profound effect on the course of the 20th century. It led to the collapse of the Austro-Hungarian, Ottoman, and Russian Empires, and the creation of new countries, including Czechoslovakia, Yugoslavia, and Poland. The war also led to the formation of the League of Nations, an international organization dedicated to preventing future wars."
  ]
]

def generate_pdf(messages, question):
    messages = messages.split("\n")
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    custom_style = ParagraphStyle(
        name="CustomStyle",
        fontName="Amble-Regular",  
        fontSize=16,                
        leading=18,                 
        textColor="black"            
    )
    
    custom_style_header = ParagraphStyle(
        name="CustomStyle",
        fontName="kg-broken-vessels-sketch.regular",  
        fontSize=24,                
        leading=18,             
        textColor="black"            
    )

    content = []
    
    content.append(Paragraph(question, custom_style_header))
    content.append(Spacer(1, 12))
    content.append(Paragraph(""))
    content.append(Spacer(1, 12))
    for message in messages:
        if message != "":
          content.append(Paragraph(message))
          content.append(Spacer(1, 12))  

    doc.build(content)
    buffer.seek(0)
    return buffer

if 'messages' not in st.session_state:
    st.session_state['messages'] = []
    
if 'response' not in st.session_state:
    st.session_state['response'] = []

def chat_bot(text):
    st.session_state["messages"] = []
    st.session_state.messages.append({"sender": "user", "message": text})
    # suffix = "Title$$##: [Enter the title of the article] Contains$$##: [Enter the main points or content you want in the article]"
    response = palm.chat(
        **defaults,
        context=context,
        examples=examples,
        messages= [message["message"] for message in st.session_state.messages]  # Pass the messages list, not just the text
    )
    temp = response.last
    st.session_state.messages.append({"sender": "bot", "message": temp})
    return temp

def generate_audio(text):
    mp3_fp = BytesIO()
    tts = gTTS(text, lang='en')
    tts.write_to_fp(mp3_fp)
    return mp3_fp

st.title("AI Chat Bot")

text = st.text_input("Enter your message")


if st.button("Search") or text: st.session_state.response = chat_bot(text)
        

user_messages = [message for message in st.session_state.messages if message["sender"] == "user"]
bot_messages = [message for message in st.session_state.messages if message["sender"] == "bot"]

for user_msg, bot_msg in zip(reversed(user_messages), reversed(bot_messages)):
    with st.chat_message("user"):
        st.write(user_msg['message'])
    with st.chat_message("assistant"):
        st.write(bot_msg['message'])
        if st.session_state.response == bot_msg['message']:
          st.audio(generate_audio(st.session_state.response), format='audio/ogg')
          pdf_buffer = generate_pdf(st.session_state.response, user_msg['message'])
          st.subheader("Download PDF")
          st.write("Click the link below to download the PDF:")
          st.download_button(
              label="Download PDF",
              data=pdf_buffer,
              file_name="generated_pdf.pdf",
              mime="application/pdf")
