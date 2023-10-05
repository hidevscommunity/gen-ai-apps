import os
import streamlit as st
import weaviate
import openai
from pipelines import generate_index, generate_sample_index, generation_pipeline
from utils.file_helper import create_download_link, load_sample_job

def generate_letter():
    with st.spinner("The AI is working hard for you, please come back in about a minute!"):
        w_client = weaviate.Client(embedded_options=weaviate.embedded.EmbeddedOptions(),
                                   additional_headers={ 'X-OpenAI-Api-Key': st.session_state.openai_api_key})
        
        # Avoid duplicated file index in the current experimental stage
        for class_name in ["User", "Company"]:
            current_schema = w_client.schema.get()
            class_exists = any(cls['class'] == class_name for cls in current_schema['classes'])
            if class_exists:
                w_client.schema.delete_class(class_name)
                print(f"Class '{class_name}' has been deleted")
        
        if st.session_state.use_sample:
            index_user, index_company = generate_sample_index(w_client)
        else:
            index_user, index_company = generate_index(st.session_state.personal_docs, st.session_state.company_docs, w_client)

        letter = generation_pipeline(st.session_state.name,
                                    st.session_state.title,
                                    st.session_state.company,
                                    st.session_state.job_description,
                                    index_user,
                                    index_company)
        st.session_state.done = True
        st.session_state.letter = letter
        st.session_state.loading = False
        print("loading state is:")
        print(st.session_state.loading)


def validate_form():
    text_fields = ["name", "company", "title", "job_description"]

    for field in text_fields:
        if st.session_state[field].strip() == "":
            st.warning("Please fill in all the text fields")
            return False
    if len(st.session_state.personal_docs) == 0 and not st.session_state.use_sample:
        st.warning("Please upload at least one resume or personal statement") 
        return False
    return True


def disable_fields():
    if validate_form():
        st.session_state.loading = True


def validate_and_run():
    if validate_form():
        os.environ["OPENAI_API_KEY"] = openai.api_key = st.session_state.openai_api_key
        generate_letter()


st.set_page_config(
    page_title="coverLit",
    page_icon="📝"
)

with st.sidebar:
    st.session_state.openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    "[Get your OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("📄💡coverLit")
st.caption("Fully customized cover letter is just a minute")

if "letter" not in st.session_state:
    st.session_state.letter = None
if "loading" not in st.session_state:
    st.session_state.loading = False

st.session_state.use_sample = st.checkbox("Use sample data", value=False, disabled=st.session_state.loading)
    
with st.form(key="my_form"):
    # Apply custom CSS to adjust the height of textarea
    with open("ui/styles.md", "r") as styles_file:
        styles_content = styles_file.read()
    st.markdown(styles_content, unsafe_allow_html=True)

    st.session_state.name = st.text_input('Your name',
                                          value="Sammy Sloan" if st.session_state.use_sample else "",
                                          disabled=st.session_state.use_sample)
    
    st.session_state.company = st.text_input('Company name',
                                             value="Whitbread" if st.session_state.use_sample else "",
                                             disabled=st.session_state.use_sample)
    
    st.session_state.title = st.text_input('Job title',
                                           value="Data Science Lead" if st.session_state.use_sample else "",
                                           disabled=st.session_state.use_sample)
    
    st.session_state.job_description = st.text_area('Job description',
                                                    value=load_sample_job() if st.session_state.use_sample else "",
                                                    disabled=st.session_state.use_sample)
    
    st.session_state.personal_docs = st.file_uploader("Upload you resume or personal statements",
                                                      type=['pdf', 'docx'],
                                                      accept_multiple_files=True,
                                                      disabled=st.session_state.use_sample)
    
    if st.session_state.use_sample:
        download_link_1 = create_download_link(os.path.join("sample", "cv.txt"), "View sample resume")
        download_link_2 = create_download_link(os.path.join("sample", "personal_statement.txt"), "View sample personal statement")
        st.markdown(download_link_1, unsafe_allow_html=True)
        st.markdown(download_link_2, unsafe_allow_html=True)

    st.session_state.company_docs = st.file_uploader("Upload related company information (optional)",
                                                     type=['pdf', 'docx'],
                                                     accept_multiple_files=True,
                                                     disabled=st.session_state.use_sample)
    
    
    if st.session_state.use_sample:
        download_link_3 = create_download_link(os.path.join("sample", "company_info_1.txt"), "View sample company information 1")
        download_link_4 = create_download_link(os.path.join("sample", "company_info_2.txt"), "View sample company information 2")
        st.markdown(download_link_3, unsafe_allow_html=True)
        st.markdown(download_link_4, unsafe_allow_html=True)

    start_btn = st.form_submit_button('Generate you personalized cover letter!',
                                      disabled=st.session_state.loading,
                                      on_click=disable_fields)
    if start_btn:
        validate_and_run()

if st.session_state.letter:
    display_text = st.session_state.letter
    disable_letter = False
else:
    display_text = "You cover letter will display here"
    disable_letter = True
st.text_area("cover letter", value=display_text, height=500, key="cover_letter_area", label_visibility="hidden" ,disabled=disable_letter)