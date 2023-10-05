import streamlit as st
import time
from prompt import LLM_Hander
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(page_title='School GPT',
                   page_icon='🚸',
                )

if 'trainingCompleted' not in st.session_state:
    st.session_state.trainingCompleted = False

if 'botHandler' not in st.session_state:
    st.session_state.botHandler = None

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'fnames' not in st.session_state:
    st.session_state.fnames = []

if 'user_cf_key' not in st.session_state:
    st.session_state.user_cf_key = ""

def getKB():
    idx = 0
    kb = ""
    for f in st.session_state.fnames:
        idx += 1
        kb += f'{idx}. {f} \n'
    return kb

def retrain():
    st.session_state.trainingCompleted = False

def doTraining(flist):
    with st.status(label='Crunching the data 🏋🏻‍♀️🏋🏻‍♀️🏋🏻‍♀️🏋🏻‍♀️🏋🏻‍♀️🏋🏻‍♀️', expanded=True):
        st.session_state.botHandler.loadData(flist)
        st.write('📑 Loaded the docs ✅')
        st.session_state.botHandler.prepareIndex()
        st.write('📇 Created indexes ✅')
        st.session_state.botHandler.prepareIndex()
        st.write('👩🏻‍🏫 Created teacher bot ✅')            
        st.write('👨🏻‍🎓 Created student bot ✅')
        st.session_state.botHandler.prepareBots()
    st.session_state.trainingCompleted = True

def resetChat():
    st.session_state.botHandler.clearHistory()
    st.session_state.messages.clear()

def glow(raw):
    s = f"""
      <p class="glow"> {raw}</p>
    """
    return s

def glow2(raw):
    s = f"""
      <p class="neonText"> {raw}</p>
    """
    return s

def decideGlow(raw, role):
    if role == 'assistant':
        return doGreen(raw)
    else:
        return doOrange(raw)

def doGreen(raw):
    s = f"""
      <div class="doGreen"> {raw}</div>
    """
    return s

def doOrange(raw):
    s = f"""
      <p class="doOrange"> {raw}</p>
    """
    return s

def getAvatar(role):
    if role == 'Teacher Bot':
        return "👩🏻‍🏫"
    if role == 'Student Bot':
        return "👨🏻‍🎓"
    else :
        return ""


with st.sidebar:
    st.image('./resources/OIG2.png')
    #st.markdown("## :rainbow[If you would like to use your own Clarifai PAT, enter it here]", unsafe_allow_html=True)
    #st.session_state.user_cf_key = st.text_input(label='user pat',
    #                                             type='password',
    #                                             placeholder="Your Clarifai PAT",
    #                                             label_visibility='hidden')
    #if st.session_state.user_cf_key != "":
    #    st.success('Your PAT is loaded', icon="✅")

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
  font-size:14px;
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

st.markdown('# :rainbow[School GPT] 🚸', unsafe_allow_html=True)
st.markdown('### :rainbow[A personalized chatbot] 🤖')
st.markdown('powered by :rainbow[Lanngchain]🦜 :rainbow[Llama-index] 🦙 :rainbow[and Claude LLM through Clarifai] 🗣️')
st.markdown('## :rainbow[For Teachers] 👩🏻‍🏫 :rainbow[& Students] 👨🏻‍🎓')
with st.expander(label=':rainbow[By using this site, you are explicitly agreeing to following terms]',
                 expanded=False):
    sw = '''
    Please note: \n\n
    **School GPT** is powered by a large language model, along with some finetuning. \n
    **School GPT** may produce inaccurate information about people, places or facts
    '''
    st.warning(body=sw, icon="⚠️")
    st.error(body='Important Note: \n\n Please refrain from providing any sensitive information', icon="🚨")
    st.info('Schoold GPT runs in CPU 💻. We appreciate your **Patience** 🧘🏻 \n as it takes more time to generate the results (especially as Teacher Bot in chat mode)',
            icon="⏳")

if not st.session_state.trainingCompleted:
    st.markdown('#### Step 1️⃣ 👉🏻 Build a knowledge base')
    flist = st.file_uploader(label='Upload 1 or more PDF file(s) to act as a knowledge base',
                    accept_multiple_files=True,
                    type=['pdf'],
                    )
    st.markdown(':rainbow[Yours file(s) are NOT] 🙅🏻‍♂️ :rainbow[stored anywhere . Uploaded files are immediately parsed as binary data] 😎 \n :rainbow[You data is safe] 🤝')
    st.markdown("""
                <style>
div.row-widget.stRadio > div {
 flex-direction: row;
 align-items: stretch;
                font-size=8px;
}

div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"]  {
 background-color: #9AC5F4;
 padding-right: 10px;
 padding-left: 4px;
 padding-bottom: 3px;
 margin: 4px;
}
                </style>
                """, unsafe_allow_html=True)

    if st.session_state.botHandler == None:
        st.session_state.botHandler = LLM_Hander()

    if len(flist) > 0:
        st.markdown('#### Step 2️⃣ 👉🏻 If you are done adding files, click below to train')
        b = st.button('Train 🚀 the school bot 🤖', use_container_width=True, type='primary', on_click=doTraining, args=[flist])
        

if st.session_state.trainingCompleted:
    st.success(f'😎 Ready to serve you based on the knowledge 🧠 I gathered from: \n\n {getKB()}')
    colb1, colb2 = st.columns([1.5,2])
    with colb1:
        st.markdown('### :rainbow[Changed your mind?] 🤔')
    with colb2:
        st.button('#### Step 3️⃣ 👉🏻 Click me to re-train 🧠', use_container_width=True, type='primary', on_click=retrain)
    colb1, colb2, colb3, col4 = st.columns([0.5,1.5,2,0.5])
    with colb3:
        st.markdown('### :rainbow[OR]')
    colb1, colb2, colb3 = st.columns([0.5,4,0.5])
    with colb2:
        st.markdown('### Step 4️⃣ 👇🏻 :rainbow[Choose your bot role to work with!]')
    BotOption = st.radio(
        "Available Bots 🤖",
        ["Student Bot", "Teacher Bot"],
        captions=["👨🏻‍🎓 Q&A bot for answering questions",
                "👩🏻‍🏫 Chat bot for teacher assistant tasks"],
                horizontal=True
    )
    if BotOption == "Teacher Bot":
        st.info(' I run on CPU 💻. We appreciate your **Patience** 🧘🏻 \n as it takes more time to generate the results',
        icon="⏳")
        bm = """
Please note this is an _**experimental effort**_ to force a LLM to use the uploaded context.
Sometimes the model hallucinates and would not provide any response. In such cases, kindly retry 🙏.

If you are a nerd 🤓 who wants to understand how to power a LLM with custom index, 👈🏻 head out to the architecture page 📐 to learn more 👓

"""
        st.warning(bm, icon="⚠️")
        with st.chat_message(name="assistant"):
            st.markdown('Chat with me')
        for message in st.session_state.messages:
            with st.chat_message(name=message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("How may I help you?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message(name='assistant'):
                message_placeholder = st.empty()
                full_response = ""
                with st.spinner(text="Thinking... 💭💭💭"):
                    if st.session_state.botHandler != None:
                        raw = st.session_state.botHandler.firePrompt('teacher', st.session_state.messages[-1]['content'])
                        response = str(raw)
                        # Simulate stream of response with milliseconds delay
                        for chunk in response.split():
                            full_response += chunk + " "
                            time.sleep(0.05)
                            # Add a blinking cursor to simulate typing
                            message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)
                        message_placeholder.markdown(full_response, unsafe_allow_html=True)
                        st.session_state.messages.append({"role": "Teacher Bot", "content": full_response})
                    else:
                        message_placeholder.error('Bot not initialized')
                st.button('Reset Chat 🗑️', use_container_width=True, on_click=resetChat)

    if BotOption == "Student Bot":
        with st.chat_message(name="assistant"):
            st.markdown('Ask a question')
        if prompt := st.chat_input('ask....'):
            m = {"role" : "user", "content" : prompt}
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message(name='assistant'):
                with st.spinner('Thinking'):
                    if st.session_state.botHandler != None:
                        r = st.session_state.botHandler.firePrompt('student', prompt)
                        st.markdown(str(r))
                    else:
                        st.error('Bot not initialized')


