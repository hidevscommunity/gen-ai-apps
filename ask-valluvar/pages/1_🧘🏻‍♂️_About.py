import streamlit as st

st.set_page_config(
    page_title="About Ask Valluvar",
    page_icon="🧘🏻‍♂️",
)

with st.sidebar:
    st.image('./resources/vv.png', use_column_width='always')
    st.info('This app is built as my participation to[Streamlit LLM Hackathon](https://streamlit.io/community/llm-hackathon-2023?referral=banner-hp)', icon="🤗")
    st.info('Valluvar AI is powered using GPT-4 LLM and Speech Synthesis models offered by [Clarifai](https://www.clarifai.com/) as part of this hackathon', icon="🤝")
    st.info('Post hackathon, Valluvar AI will be powered by open models. Please stay tuned !', icon="🚀")

welcome_text = '''
<div class="doOrange">

Step into the realm of timeless wisdom and enlightenment, where the great sage Tiruvalluvar's teachings come to life through our AI companion. 📜💬

🌿 Are you seeking guidance, clarity, or inspiration?
🤔 Got questions that need profound answers?
💭 Seeking advice for life's labyrinthine twists and turns?

Look no further! Tiruvalluvar AI is here to illuminate your path with pearls of ancient wisdom from the sacred Tirukural. 🌠

🌞 Embrace the serenity of Tiruvalluvar's insights.
🌏 Explore the vast realm of knowledge and virtue.
🌱 Let's embark on a journey of self-discovery and enlightenment together.

Unearth the treasures of Tirukural and let its wisdom transform your world! 🌌✨

Type your questions, share your thoughts, and let the sage's words guide you towards a brighter future. 🌅

Welcome, seeker of knowledge and truth! 🙏🕊️
</div>
'''

st.title('🌟 Welcome to the Wisdom Oasis: Chat with Tiruvalluvar AI! 🌟')

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
**Ask Valluvar** is powered by a large language model, along with some finetuning. \n
**Ask Valluvar** may produce inaccurate information about people, places or facts
'''
st.warning(body=sw, icon="⚠️")
st.error(body='Important Note: \n\n Please refrain from providing any sensitive information', icon="🚨")
st.info('Thiruvalluvar appreciate your **Patience** 🧘🏻 \n as sometimes it takes more time to generate the results...',
        icon="⏳")