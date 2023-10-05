import streamlit as st
from urllib.error import URLError
from communicator import Communicator
from credentials import validate_openai_key
import time
import uuid
from ratelimit import RateLimitException

llm_avatar = 'images/neo4j_icon_white.png'
user_avatar = '👤'

INITIAL_MESSAGE = [
    {
        "role": "assistant",
        "avatar": llm_avatar,
        "content": """
                    Hey there, I'm Agent Neo!
                    What Graph Data Science question can I answer for you?

                    Each visitor will be able to have 25 question & answers per day due to this app being public. We hope this will be
                    enough to get you excited for what the full Agent Neo has to offer!

                    If you're interested in learning more please read our Medium article in the sidebar.
                    """,
    },
]

RESET_MESSAGE = [
    {
        "role": "assistant",
        "avatar": llm_avatar,
        "content": """
                    Our chat history has been reset.
                    What Graph Data Science question can I answer for you?
                    """,
    },
]

with open("ui/sidebar.md", "r") as sidebar_file:
    sidebar_content = sidebar_file.read()

try:
    st.markdown("""
    <style>
    .sidebar-font {
        font-size:14px !important;
        color:#FAFAFA !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Agent Neo")
    st.sidebar.markdown("# Agent Neo")
    st.sidebar.markdown("Read more: [The Practical Benefits to Grounding an LLM in a Knowledge Graph](https://medium.com/@bukowski.daniel/the-practical-benefits-to-grounding-an-llm-in-a-knowledge-graph-919918eb493)")

    # check for openai key
    # if 'user_openai_key_validated' not in st.session_state or not st.session_state['user_openai_key_validated']:
    #     st.session_state['user_openai_key'] = st.text_input('Please enter OpenAI key to use Agent Neo')

    # init session if first visit
    if len(st.session_state.keys()) == 0:
        st.session_state["messages"] = INITIAL_MESSAGE
        st.session_state["history"] = []
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = 's-'+str(uuid.uuid4())

    # give options for llm
    llm = st.sidebar.radio("Select LLM", ("chat-bison 2k", "chat-bison 32k", "GPT-4 8k", "GPT-4 32k"), horizontal=True, index=2, 
                           help="""
                                Selecting a different LLM will reset the chat. Default is GPT-4 8k.
                                """)
    
    # select temperature
    temperature = st.sidebar.slider("Select Temperature", 0.0, 1.0, 0.7, step=0.05, 
                                    help='''
                                         Temperature sets the amount of "creativity" the LLM has 
                                         in developing its responses. Chat must be reset to have an effect.
                                         ''')
    
    # Add slider to select the number of documents to use as context
    use_context = st.sidebar.toggle('Use Grounding?', value=True, help='Use the Neo4j knowledge graph to ground Agent Neo.')
    if use_context:
        st.session_state['num_documents_for_context'] = st.sidebar.slider('Select Number of Context Documents', 1, 10, 10, 
                                                                      help='''
                                                                            More documents could provide better context for a response 
                                                                            at the cost of longer prompts and processing time. This
                                                                            value can vary throughout a conversation.
                                                                            ''',
                                                                            disabled=not use_context)
    else:
        st.session_state['num_documents_for_context'] = 0

    # Add a reset button
    st.sidebar.caption('<p class="sidebar-font">Reset Chat & Memory</p>', unsafe_allow_html=True)
    if st.sidebar.button("Reset", type="primary", 
                         help='''
                              Effectively reset the session. A new Neo4j driver is created and the LLM history is cleared.
                              '''):
        for key in st.session_state.keys():
            if key != 'session_id':
                del st.session_state[key]
        st.session_state["messages"] = RESET_MESSAGE
        st.session_state["history"] = []
        st.session_state['temperature'] = temperature

    # Add buttons to rate most recent LLM repsonse
    if 'communicator' in st.session_state:
        st.sidebar.write('<p class="sidebar-font">Rate Recent LLM Response</p>', unsafe_allow_html=True)
        with st.sidebar:
            good_col, bad_col = st.columns(2)
            with good_col:
                good = st.button(':+1:', on_click=st.session_state['communicator'].rate_message, kwargs={'rating': 'Good'}, disabled=False, key='good_sidebar')
            with bad_col:
                bad = st.button(':-1:', on_click=st.session_state['communicator'].rate_message, kwargs={'rating': 'Bad'}, disabled=False, key='bad_sidebar')

    # display app description in sidebar
    st.sidebar.markdown(sidebar_content)

    #VALIDATE OPENAI KEY after sidebar content has loaded
    # if not st.session_state['user_openai_key']:
    #     st.warning("Please enter your OpenAI key to use Agent Neo.")
    #     st.stop()
    # elif not st.session_state['user_openai_key_validated']:
    #     st.warning("OpenAI key not valid. Try again.")
    #     st.stop()
    
    # # openai key check
    # if 'user_openai_key_validated' not in st.session_state or not st.session_state['user_openai_key_validated']:
    #     st.session_state['user_openai_key_validated'] = validate_openai_key()

    # if not st.session_state['user_openai_key_validated']:
    #     st.session_state['user_openai_key'] = None
    #     st.session_state['user_openai_key_validated'] = False
    #     st.experimental_rerun()

    # init Communicator object
    if 'communicator' not in st.session_state:
        st.session_state['communicator'] = Communicator()

    # Initialize the chat messages history
    if "messages" not in st.session_state:
        st.session_state["messages"] = INITIAL_MESSAGE
        st.chat_message("assistant", avatar=llm_avatar).markdown(INITIAL_MESSAGE['content'])

    # Initialize the LLM conversation
    if "llm_conversation" not in st.session_state:
        st.session_state['temperature'] = temperature
        st.session_state['llm_conversation'] = st.session_state['communicator'].create_conversation(llm)

    # handle llm switching
    if 'prev_llm' not in st.session_state:
        st.session_state['prev_llm'] = llm

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message['avatar']):
            st.markdown(message["content"])

    if st.session_state['prev_llm'] != llm:
        print("switching llm...")
        message = f"Excuse me while I switch to my {llm} brain and wipe my memory..."
        st.chat_message("assistant", avatar=llm_avatar).markdown(message)
        st.session_state.messages.append({"role": "assistant", "avatar": llm_avatar, "content": message})
        # on switch, restart the internal llm conversation history with new llm
        st.session_state['llm_conversation'] = st.session_state['communicator'].create_conversation(llm)
        st.session_state['prev_llm'] = llm

    # Prompt for user input and save and display
    if question := st.chat_input():
        st.session_state.messages.append({"role": "user", "avatar": user_avatar, "content": question})
        st.chat_message("user", avatar=user_avatar).markdown(question)

#       start prompt timer
        prompt_timer_start = time.perf_counter()
        prompt, context_idxs = st.session_state['communicator'].create_prompt(question)
        prompt_timer_response = "\n\nPrompt creation took "+str(round(time.perf_counter() - prompt_timer_start, 4))+" seconds."
        
        # create new log chain in neo4j database if fresh conversation
        # and log first user message
        # if only initial message and user message OR
        # if 2 consecutive assistant followed by new user message in history
        if len(st.session_state['messages']) <= 2 or st.session_state['messages'][-3]['role'] == 'assistant':
            st.session_state['communicator'].log_new_conversation(llm=llm, user_input=question)

        # otherwise log user message to neo4j database
        else:
            st.session_state['communicator'].log_user(user_input=question)


        with st.chat_message('assistant', avatar=llm_avatar):
            message_placeholder = st.empty()
            message_placeholder.status('thinking...')

            # start "thinking" timer
            run_timer_start = time.perf_counter()
            response = st.session_state['llm_conversation'].run(prompt)
            run_timer_response = "\n\nThis thought took "+str(round(time.perf_counter() - run_timer_start, 4))+" seconds."

            message_placeholder.markdown(response+prompt_timer_response+run_timer_response)

            # log LLM response to neo4j database
            st.session_state['communicator'].log_assistant(assistant_output=response, context_indices=context_idxs)

        st.session_state.messages.append({"role": "assistant", 'avatar':llm_avatar, "content": response+prompt_timer_response+run_timer_response})

    # rate buttons appear after each llm response
    if len(st.session_state['messages']) > 2 and st.session_state['messages'][-1]['role'] == 'assistant':
        with st.chat_message('rate', avatar='❓'):
            col1, col2, col3= st.columns([0.1, 0.1, 0.8])
            with col1:
                good = st.button(':+1:', on_click=st.session_state['communicator'].rate_message, kwargs={'rating': 'Good'}, disabled=False, key='good_body')
            with col2:
                bad = st.button(':-1:', on_click=st.session_state['communicator'].rate_message, kwargs={'rating': 'Bad'}, disabled=False, key='bad_body')

except URLError as e:
    st.error(
        """
        **This app requires internet access.**
        Connection error: %s
    """
        % e.reason
    )
except RateLimitException as e:
    print(e)
    st.error(
        """
        Error occurred: %s \n
        You are allowed only so many calls per day. \n 
        Please wait for your rate limit to reset.
        """
        % e
    )
except Exception as e:
    print(e)
    st.error(
        """
        Error occurred: %s
        """
        % e
    )


