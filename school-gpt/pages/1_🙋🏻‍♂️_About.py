import streamlit as st


st.set_page_config(page_title='About School GPT',
                   page_icon='🙋🏻‍♂️',
                )

with st.sidebar:
    st.image('./resources/OIG1.png', use_column_width='always')
    st.info('This app is built as my participation to[Streamlit LLM Hackathon](https://streamlit.io/community/llm-hackathon-2023?referral=banner-hp)', icon="🤗")
    st.info('School GPT 🚸 is powered using Langchain 🦜, Llama-index 🦙 and Claude LLM 🗣️ model offered by [Clarifai](https://www.clarifai.com/) as part of this hackathon', icon="🤝")
    st.info('Post hackathon, School GPT 🚸 will be powered by open models. Please stay tuned !', icon="🚀")

welcome_text = '''
<div class="doOrange">

Powered by Langchain 🦜, Llama-Index 🦙, and Claude LLM 🧠 🧑‍🎨

Are you a teacher in search of a llama-zing chat companion? 🍎 Or perhaps a student looking for answers to life's mysteries? 🤔 Fear not, because this dual-persona bot is here to make your academic journey a wild and woolly ride! 🎢🦙

👩‍🏫 For our dedicated educators, this chatbot is your new BFF (Best Friend Forever). Whether you need lesson plan inspiration, grading advice, or just a good llama joke to lighten the mood, we've got you covered! 🎓📝

👩‍🎓 Calling all students! Do you have burning questions that keep you up at night? Worried about that looming exam? 📚 Let our llama-fied Q&A mode guide you through the maze of knowledge and lead you to the treasure chest of answers! 💡🧐

But wait, there's more! 🌟

📂 Do you have a stash of PDFs gathering virtual dust on your device? No problemo! 📄💨 Upload them here, and we'll whip up a llama-tastic contextual experience for you! 🧙‍♂️✨

📌 Just remember, each PDF should be as light as a llama feather, not exceeding 25MB in size. 🦙🪶

So, what are you waiting for? Dive into the world of education, fun, and fluffy llamas with the Super Llama-Teacher Bot! 🦙🎉

Just type "Start" and let the llama-magic begin! 🚀🦙🪄
</div>
'''

st.title('🌟 👋  :rainbow[Welcome to School GPT] 🚸 🌟')
st.subheader(':rainbow[Your Personalized academia bot] 🦙📚')

st.markdown("""
<style>
.chat-font {
    font-size:100px !important;
    
    color:green;
}

.doGreen {
  font-family:monospace;
  font-size:14px;
  color: green;   
}

.doOrange {
  font-family:monospace;
  font-size:50px;
  color: orange;   
}              

.neonText {
  color: #fff;
  font-family:monospace;
  font-size:20px;
  text-shadow:
      0 0 7px #fff,
      0 0 10px #fff,
      0 0 21px #fff,
      0 0 42px #0fa,
      0 0 82px #0fa,
      0 0 92px #0fa,
      0 0 102px #0fa,
      0 0 151px #0fa;
}
            
.glow {
  font-size: 18px;
  color: #fff;
  font-family:monospace;
  animation: glow 1s ease-in-out infinite alternate;
}

@-webkit-keyframes glow {
  from {
    text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #0fa, 0 0 40px #0fa, 0 0 50px #0fa, 0 0 60px #0fa, 0 0 70px #0fa;
  }
  
  to {
    text-shadow: 0 0 20px #fff, 0 0 30px #ff4da6, 0 0 40px #ff4da6, 0 0 50px #ff4da6, 0 0 60px #ff4da6, 0 0 70px #ff4da6, 0 0 80px #ff4da6;
  }
}
            
</style>
""", unsafe_allow_html=True)

st.markdown(welcome_text, unsafe_allow_html=True)

sw = '''
Please note: \n\n
**School GPT** is powered by a large language model, along with some finetuning. \n
**School GPT** may produce inaccurate information about people, places or facts
'''
st.warning(body=sw, icon="⚠️")
st.error(body='Important Note: \n\n Please refrain from providing any sensitive information', icon="🚨")
st.info('Schoold GPT runs in CPU 💻. We appreciate your **Patience** 🧘🏻 \n as it takes more time to generate the results (especially as Teacher Bot in chat mode)',
        icon="⏳")