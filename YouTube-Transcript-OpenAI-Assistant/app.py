import streamlit as st
import utility_settings as util_set  # Python file with utilities
from llama_ytb import LlamaContext  # Python file with utilities
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import os
import time


def f_init_session():
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["I'm your transcript assistant, How may I help you?"]
    if 'past' not in st.session_state:
        st.session_state['past'] = ['Hi!']

    if 'openai_api_key_valid' not in st.session_state:
        st.session_state['openai_api_key_valid'] = False
    if 'open_ai_key_status' not in st.session_state:
        st.session_state['open_ai_key_status'] = 'OpenAI API key is not valid'
    if 'openai_api_key_err' not in st.session_state:
        st.session_state['openai_api_key_err'] = None
    if 'embedded' not in st.session_state:
        st.session_state['embedded'] = False
    if 'ytb_content' not in st.session_state:
        st.session_state['ytb_content'] = ''
    if 'ytb_content_valid' not in st.session_state:
        st.session_state['ytb_content_valid'] = False
    if 'billed_status' not in st.session_state:
        st.session_state['billed_status'] = ''
    if 'index_status' not in st.session_state:
        st.session_state['index_status'] = 'Index is empty.'


def f_extract_text(_youtube_link):
    if st.session_state['sel_GPTVectorStoreIndex']:
        path = st.session_state['sel_path'] + st.session_state['sel_ytb_name']
    else:
        path = ''

    lct = LlamaContext(path=path, ytb_link=_youtube_link)
    lct.extract_ytb()
    st.session_state['ytb_content'] = lct.ytb_content
    st.session_state['ytb_content_valid'] = lct.ytb_content_valid
    st.session_state['lct'] = lct
    st.session_state['embedded'] = False  # Embed Transcript status
    st.session_state['index_status'] = 'Index is empty.'
    f_estimate_costs()


def f_clear_button():
    st.session_state['input'] = ''
    st.session_state['generated'] = ["I'm your transcript assistant, How may I help you?"]
    st.session_state['past'] = ['Hi!']


def f_get_text():
    if st.session_state['embedded'] and st.session_state['openai_api_key_valid']:
        input_text_disabled = False
    else:
        input_text_disabled = True

    input_text = st.text_input("You: ", "", key="input", disabled=input_text_disabled)
    return input_text


def f_generate_response(question):
    lct = st.session_state['lct']
    lct.post_question(question)
    _response = lct.response
    return _response


def f_validate_password(_api_key):
    if util_set.openai_psw_check(_api_key)[0]:  # password valid
        os.environ["OPENAI_API_KEY"] = _api_key
        st.session_state['openai_api_key_valid'] = True
        st.session_state['openai_api_key_err'] = None
        st.session_state['open_ai_key_status'] = 'OpenAI API key is valid'
    else:
        st.session_state['openai_api_key_valid'] = False
        st.session_state['openai_api_key_err'] = util_set.openai_psw_check(_api_key)[1]
        st.session_state['open_ai_key_status'] = 'OpenAI API key is not valid'


def f_embed_button():
    if st.session_state['openai_api_key_valid']:  # password valid
        lct = st.session_state['lct']

        if st.session_state['sel_GPTVectorStoreIndex']:
            lct.load_index()  # lct.index.vector_index.to_dict() - view content
            st.session_state['index_status'] = 'Index is loaded.'
        else:
            lct.create_vector_store()
            st.session_state['index_status'] = 'Index is created.'

        if lct.index is not None:
            st.session_state['embedded'] = True

        lct.start_query_engine()


def f_estimate_costs():
    lct = st.session_state['lct']
    lct.estimate_cost()
    st.session_state['total_cost_davinci'] = lct.total_cost_davinci
    if st.session_state['sel_GPTVectorStoreIndex']:
        st.session_state['billed_status'] = '(index is already created, no costs)'
    else:
        st.session_state['billed_status'] = '(index will be created and billed with "Embed transcript")'


def f_download_button_chat():
    _obj_save_chat = util_set.SaveChat(st.session_state['past'], st.session_state['generated'])
    _obj_save_chat.generate_json_text_files()
    return _obj_save_chat


f_init_session()

selector = util_set.SelectionValueGetter(util_set.data)
button = st.sidebar.selectbox("Select an option", selector.buttons)

sel_ytb_link = selector.get_selection_value(button, 'ytb_link')
sel_path = selector.get_selection_value(button, 'path')
sel_ytb_name = selector.get_selection_value(button, 'ytb_name')
sel_GPTVectorStoreIndex = selector.get_selection_value(button, 'GPTVectorStoreIndex')
sel_text_state_ytb_link_disabled = selector.get_selection_value(button, 'text_input_ytb_link_disabled')

st.session_state['sel_ytb_link'] = selector.get_selection_value(button, 'ytb_link')
st.session_state['sel_path'] = selector.get_selection_value(button, 'path')
st.session_state['sel_ytb_name'] = selector.get_selection_value(button, 'ytb_name')
st.session_state['sel_GPTVectorStoreIndex'] = selector.get_selection_value(button, 'GPTVectorStoreIndex')
# st.session_state['sel_text_state_ytb_link_disabled'] = \
# selector.get_selection_value(button, 'text_input_ytb_link_disabled')

# >>> Title
st.title("Youtube transcript OpenAI Assistant")
# st.write(time.strftime('%Y-%m-%d %H:%M:%S'))
add_vertical_space(1)
# <<< Title
# >>> sidebar
with st.sidebar:
    youtube_link = st.text_input(label="Enter YouTube Link with transcript",
                                 value=sel_ytb_link,
                                 disabled=sel_text_state_ytb_link_disabled)

    api_key = st.text_input("Enter your OpenAI API key here", type="password")
    st.button("Validate API key", on_click=f_validate_password, args=(api_key,), key='k_valid_psw')

    if st.session_state['openai_api_key_valid']:
        st.success(st.session_state['open_ai_key_status'], icon='✅')
    else:
        st.warning(st.session_state['open_ai_key_status'], icon='⚠️')
        if st.session_state['openai_api_key_err'] is not None:
            st.warning(st.session_state['openai_api_key_err'], icon='⚠️')

    clear_button = st.button("Clear Chat", key="clear", on_click=f_clear_button)
    add_vertical_space(1)
    st.markdown('📖 Read the [blog](https://blogs.sap.com/2023/07/14/building-trust-in-ai-youtube-transcript-openai-assistant/)')
# <<< sidebar
try:
    st.video(youtube_link, start_time=0)
    st.session_state['youtube_link_valid'] = True
except Exception as e:
    st.session_state['youtube_link_valid'] = False
    st.error(str(e))

st.markdown(youtube_link, unsafe_allow_html=True)
st.button("Extract transcript", on_click=f_extract_text, args=(youtube_link,), key='bt_extract',
          disabled=not (st.session_state['youtube_link_valid']))

content_txt = st.text_area("Transcript", height=300, value=st.session_state['ytb_content'], disabled=True)

file_data = content_txt.encode("utf-8")
file_name_transcript = f"transcript_{time.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
st.download_button(label="Download transcript", data=file_data, file_name=file_name_transcript)

if 'total_cost_davinci' in st.session_state:
    st.write(
        f"Estimated tokens costs : {st.session_state['lct'].total_cost_davinci} {st.session_state['billed_status']}")
else:
    st.write("Costs were not estimated.")

if st.session_state['ytb_content_valid'] and st.session_state['openai_api_key_valid']:
    button_embed_disabled = False
else:
    button_embed_disabled = True

embed_button = st.button("Embed transcript", key="embed", on_click=f_embed_button, disabled=button_embed_disabled)
# debug
# st.write(f"button_embed_disabled: {button_embed_disabled}")
# st.write(f"ytb_content_valid: {st.session_state['ytb_content_valid'] }")
# st.write(f"openai_api_key_valid: {st.session_state['openai_api_key_valid']}")
# if 'lct' in st.session_state:
#     if st.session_state['lct'].index is not None:
#         st.write(f"index size: {st.session_state['lct'].index.vector_store}")
#         st.write(f"index size: {sys.getsizeof(st.session_state['lct'].index.vector_store.to_dict())}")

if st.session_state['embedded']:
    st.write(f"Transcript is embedded. {st.session_state['index_status']}")
else:
    st.write(f"Transcript is not embedded. {st.session_state['index_status']}")

# Layout of input/response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-70')
obj_save_chat = f_download_button_chat()

col1, col2, = st.columns(2)
with col1:
    st.download_button(label="Download chat TEXT",
                       data=obj_save_chat.text_chat,
                       file_name=obj_save_chat.text_chat_file)

with col2:
    st.download_button(label="Download chat JSON",
                       data=obj_save_chat.json_chat,
                       file_name=obj_save_chat.json_chat_file)

response_container = st.container()

# Applying the user input box
with input_container:
    user_input = f_get_text()
# debug
# st.write(f"embedded: {st.session_state['embedded']}")
# st.write(f"openai_api_key_valid: {st.session_state['openai_api_key_valid']}")

# Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        if st.session_state['embedded'] and st.session_state['openai_api_key_valid']:
            response = f_generate_response(user_input)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(response)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))

# debug
# try:
#     st.write(f"sel_GPTVectorStoreIndex: {sel_GPTVectorStoreIndex}")
# except:
#     pass
#
# try:
#     st.write(st.session_state['lct'].index.vector_store)
# except:
#     pass
#
# try:
#     st.write(sel_path + sel_ytb_name)
# except:
#     pass
#
# st.write(st.session_state)
# st.write(user_input)

# if 'lct' not in st.session_state:
#     st.write(vars(st.session_state['lct']))
