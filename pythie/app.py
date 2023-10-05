import os
import base64

import time
import streamlit as st
import streamlit.components.v1 as components
from streamlit_oauth import OAuth2Component
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

from dotenv import load_dotenv

from PIL import Image
from fpdf import FPDF

from pytrends.request import TrendReq
pytrend = TrendReq()

import matplotlib.pyplot as plt
from annotated_text import annotated_text

from GUI.demo import get_transcripts, split_transcripts, get_global_overview,\
                       get_competitors_overview, get_topics_ratings, prepare_docs, get_response, get_suggested_questions,\
                       get_comparison

from GUI.utils import html_code_generator, get_decriptive_words,get_words_with_scores,\
                      calculate_totals, generate_color,plot_radar_chart, create_report, add_logo_from_local, add_title,\
                        add_subtitle, delete_old_embeddings, header_logo_html, bot_markdown, create_pdf

import logging

logging.getLogger().setLevel(logging.INFO)

load_dotenv()

image = Image.open("resources/pocus-pin.png")

st.set_page_config(
    page_title="Pythie - An Artefact Project",
    page_icon=image,
    layout="wide"
)



main_path = os.getcwd()

with open(main_path + "/resources/youtube_demo_background.jpg", "rb") as f:
    data = f.read()
img = base64.b64encode(data).decode()

page_bg_img = f"""
<style>
.block-container {{
                    padding-top: 1rem;
                    padding-bottom: 5rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }}
[data-testid="stAppViewContainer"] {{
padding-top: 0.1 rem;
background-image: url("data:image/png;base64, {img}");
background-size: cover;
}}
[data-testid="stHeader"] {{
background-color: rgba(0,0,0,0);
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

components.html(header_logo_html())

add_logo_from_local(main_path + "/resources/LogoPythie.png")

add_title("Discover the Truth About Products Instantly")
add_subtitle("Gen AI-Powered YouTube Review Analysis in Seconds!")
st.markdown("<h7 style='text-align: center; color: #d60987;'>*Refresh the page if you wish to try another product*<h7>", unsafe_allow_html=True)


with st.sidebar:
    openai_api_key = st.text_input(label="OpenAI API Key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

with st.form("my_form"):
    st.markdown("<h3 style='color: #070038;'>Pick your product 🔎</h3>", unsafe_allow_html=True)
    max_videos = 5
    top_videos = "relevance"
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.expander("Products examples"):
            st.write("""
            - Beauty:
                - Yves rocher lipikar
                - CHANEL les beiges

            - Tech:
                - Google Pixel 7
                - Xbox Series X
                - Far cry 6

            - Fashion: 
                - Louis Vuitton Alma BB

            - B2B : 
                - Sodexo meal card
            """)

    with col3:
        language = st.radio("Videos Language", ["English", "French"])
    if not openai_api_key:
        disable_inputquery=True
        st.info("Please add your OpenAI API key to continue.")
    else:
        disable_inputquery=False
        llm_model = ChatOpenAI(temperature=0.5, openai_api_key=openai_api_key)
        embedding_model = OpenAIEmbeddings( openai_api_key=openai_api_key)
    query = st.text_input(label="Input your product name",
                          placeholder="Ex: Google pixel 7",
                          disabled=disable_inputquery)
    st.form_submit_button(label="Analyze")

@st.cache_data
def videos_download(query, max_videos, top_videos, language, path, ext_path):
    analyzed_vids, all_comments = get_transcripts(query, max_videos, top_videos, language, path, ext_path)
    return analyzed_vids, all_comments

@st.cache_data
def videos_splitting(videos_info, path, ext_path):
    transcripts_chunks = split_transcripts(videos_info, path, ext_path)
    return transcripts_chunks

@st.cache_data
def global_overview(_transcripts_chunks, analyzed_vids, query, _model_llm, lang):
    chunk_chain_results, topics_chain_results, condensing_chains_results, global_summary_chain_results = \
        get_global_overview(transcripts_chunks, analyzed_vids, query, _model_llm, lang)
    return chunk_chain_results, topics_chain_results, condensing_chains_results, global_summary_chain_results

@st.cache_data
def competitors_comparison(_transcripts_chunks, query, _model_llm, lang):
    competitors_summary_chain_results = get_competitors_overview(transcripts_chunks, query, _model_llm, lang)
    return competitors_summary_chain_results

@st.cache_data
def products_comparison(product, _product_transcripts_chunks, query, main_product_chunk_chain_results, _model_llm, lang):
    #competitors_summary_chain_results = get_competitors_overview(transcripts_chunks, query)
    product_comparison = get_comparison(product.strip(), _product_transcripts_chunks, query, main_product_chunk_chain_results, _model_llm, lang)
    return product_comparison

@st.cache_data
def topics_rating(topics_chain_results, condensing_chains_results, query, _model_llm, lang):
    rating_topics_chain_results = get_topics_ratings(topics_chain_results, condensing_chains_results, query, _model_llm, lang)
    return rating_topics_chain_results

@st.cache_data
def questions_suggestion(global_summary_chain_results, query, _model_llm, lang):
    suggested_questions = get_suggested_questions(global_summary_chain_results, query, _model_llm, lang)
    return suggested_questions

@st.cache_resource
def videos_embedding(path, videos_info, ext_path, _model_embedding):
    delete_old_embeddings(path)
    res = prepare_docs(path, videos_info, ext_path, _model_embedding)
    return res

@st.cache_data
def trends_and_common_words(path, query, all_comments):
    text = get_decriptive_words()
    sorted_words1= get_words_with_scores(text)
    word_freq = {word[0]: word[1] for word in sorted_words1}
    comments = ' '.join(all_comments)
    sorted_words2= get_words_with_scores(comments)
    word_freq = {word[0]: word[1] for word in sorted_words2}
    return sorted_words1, sorted_words2, word_freq, comments, text

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

if language == 'French':
    lang_code = 'fr'
else:
    lang_code = 'en'

if query:
    analyzed_vids, all_comments = videos_download(query, max_videos, top_videos, language, main_path, "/data/videos_transcripts/main_product/")
    total_views, total_likes, total_comments= calculate_totals(analyzed_vids)
    st.markdown("<h5 style='color: #070038;'>Analyzed videos</h5>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total view", total_views, "")
    col2.metric("Total Likes", total_likes, "")
    col3.metric("Total Comments", total_comments, "")

    components.html(html_code_generator(analyzed_vids), height=290, scrolling=True)
    try: 
        sorted_words1, sorted_words2, word_freq, comments, text = trends_and_common_words(main_path, query, all_comments)
        pytrend.build_payload([query], cat=0, timeframe="today 12-m", geo="FR")
        pytrend.interest_over_time()
        graphic = pytrend.interest_over_time()
        
        if not(graphic.empty):
            graphic = graphic.iloc[:, 0]
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<h5 style='color: #070038;'>Interest over time</h5>", unsafe_allow_html=True)
                st.bar_chart(graphic)
            with col2:
                st.markdown("<h5 style='color: #070038;'>People also search for:</h5>", unsafe_allow_html=True)
                subcol1, subcol2= st.columns(2)
                trend_analysis = pytrend.related_topics()
                try:
                    related_topics = trend_analysis.get([query][0]).get("top")
                    topics  = related_topics["topic_title"].values.tolist()
                except AttributeError:
                    topics = []
                except KeyError:
                    topics = []
                with subcol1:
                    for word in topics[:5]:
                        annotated_text((word,"",""))
                with subcol2:
                    for word in topics[5:10]:
                        annotated_text((word,"",""))
    except:
        pass

    transcripts_chunks = videos_splitting(analyzed_vids, main_path, "/data/videos_transcripts/main_product/")
        
    st.markdown("<h3 style='color: #070038;'>Discover reviewers impressions in just few lines</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='color: #d60987;'>Let the AI generate a summary of reviewers opinion about your product</h5>", unsafe_allow_html=True)
    chunk_chain_results, topics_chain_results, condensing_chains_results, global_summary_chain_results = \
        global_overview(transcripts_chunks, analyzed_vids, query, llm_model, lang_code)
    bot_markdown(message_header="Time to spill the tea... Here's what people are saying about your product:",
                message=global_summary_chain_results['global_summary'].strip())

    st.markdown("<h3 style='color: #070038;'>How your product compares to the competition</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='color: #d60987;'>Let the AI generate a comparison between your product and others mentioned in the videos</h5>", unsafe_allow_html=True)
    competitors_summary_chain_results = competitors_comparison(transcripts_chunks, query, llm_model, lang_code)
    if 'comparison_product_1' not in st.session_state:
        st.session_state['comparison_product_1'] = ""
    if 'comparison_product_2' not in st.session_state:
        st.session_state['comparison_product_2'] = ""
    with st.form("form_competitors_products"):
        col1, col2 = st.columns(2)
        with col1:
            try:
                product_1 = st.text_input(label="Product #1", value=competitors_summary_chain_results["detected_products_list"][0])
            except IndexError:
                product_1 = st.text_input(label="Product #1", value="")
        with col2:
            try:
                product_2 = st.text_input(label="Product #2", value=competitors_summary_chain_results["detected_products_list"][1])
            except IndexError:
                product_2 = st.text_input(label="Product #2", value="")
        submitted = st.form_submit_button("Submit")
        if submitted:
            if product_1.strip() != "":
                analyzed_vids_product_1, all_comments_product_1 = videos_download(product_1.strip(), 5, "relevance", language, main_path, "/data/videos_transcripts/product_1/")
                splitted_transcripts_product_1 = videos_splitting(analyzed_vids_product_1, main_path, "/data/videos_transcripts/product_1/")
                st.session_state['comparison_product_1'] = products_comparison(product_1.strip(), splitted_transcripts_product_1, query, chunk_chain_results, llm_model, lang_code)
        if st.session_state['comparison_product_1'] != "":
            st.markdown("<h5 style='color: #d60987;'>" + query + "  VS  " + product_1.strip() + "</h5>", unsafe_allow_html=True)
            st.write(st.session_state['comparison_product_1']['comparison_summary'])

        if submitted:
            if product_2.strip() != "":        
                analyzed_vids_product_2, all_comments_product_2 = videos_download(product_2.strip(), 5, "relevance", language, main_path, "/data/videos_transcripts/product_2/")
                splitted_transcripts_product_2 = videos_splitting(analyzed_vids_product_2, main_path, "/data/videos_transcripts/product_2/")
                st.session_state['comparison_product_2'] = products_comparison(product_2.strip(), splitted_transcripts_product_2, query, chunk_chain_results, llm_model, lang_code)
        if st.session_state['comparison_product_2'] != "":
            st.markdown("<h5 style='color: #d60987;'>" + query + "  VS  " + product_2.strip() + "</h5>", unsafe_allow_html=True)
            st.write(st.session_state['comparison_product_2']['comparison_summary'])
    

    st.markdown("<h3 style='color: #070038;'>How do your product features measure up</h3>", unsafe_allow_html=True)
    st.markdown("<h5 style='color: #d60987;'>Let the AI generate the highlighted product features and their rating</h5>", unsafe_allow_html=True)
    rating_topics_chain_results = topics_rating(topics_chain_results, condensing_chains_results, query, llm_model, lang_code)
    structured_ratings = rating_topics_chain_results['structured_ratings']
    ratings_explanations = rating_topics_chain_results['topics_likes_dislikes']
    bot_markdown(message_header="Drumroll🥁...",
                message="Your product grades are out !")
    if len(structured_ratings) > 2:
        logging.info('Found more than 2 structured_ratings')
        logging.info(structured_ratings)
        logging.info(ratings_explanations)
        n = 2
        cols = st.columns(n)
        for k in range(len(cols)):
            with cols[k]:
                while True:
                    colored_topic = generate_color(structured_ratings[k]["rating"])
                    topic_rating = structured_ratings[k]["topic"] + ": " + structured_ratings[k]["rating"]
                    with st.expander(colored_topic.format(topic_rating=topic_rating)):
                        try:
                            st.write(ratings_explanations[structured_ratings[k]["topic"]])
                        except KeyError:
                            logging.info('Got keyerror')
                            pass
                    k += 2
                    if k > (len(structured_ratings) - 1):
                        break
    else:
        logging.info('Found 2 or less structured_ratings')
        n = len(structured_ratings)
        cols = st.columns(n)
        for k in range(len(cols)):
            with cols[k]:
                while True:
                    colored_topic = generate_color(structured_ratings[k]["rating"])
                    topic_rating = structured_ratings[k]["topic"] + ": " + structured_ratings[k]["rating"]
                    with st.expander(colored_topic.format(topic_rating=topic_rating)):
                        try:
                            st.write(ratings_explanations[structured_ratings[k]["topic"]])
                        except KeyError:
                            pass
                    k += 2
                    if k > (len(structured_ratings) - 1):
                        break

    st.markdown("<h3 style='color: #070038;'>Chat with the AI on your product videos</h3>", unsafe_allow_html=True)

    docsearch = videos_embedding(path=main_path,
                                 videos_info=analyzed_vids,
                                 ext_path="/data/videos_transcripts/main_product/",
                                 _model_embedding=embedding_model)

    questions_generation_chain_results = questions_suggestion(global_summary_chain_results, query, llm_model, lang_code)
    suggested_questions = questions_generation_chain_results['suggested_questions']
    with st.form("chatbot_form"):
        with st.expander(label="**Example questions**"):
            for i in range(len(suggested_questions)):
                st.write("Q" +  str(i+1) + ": " + suggested_questions[i])
        question = st.text_input(label = "Ask me something :", value="")
        submit_button = st.form_submit_button("Ask")

    if 'response' not in st.session_state:
        st.session_state['response'] = ""
    if submit_button :
        with st.spinner('Generating response...'):
            st.session_state['response'] = get_response(question, docsearch, llm_model, lang_code)

    if st.session_state['response'] != "":
        if len(st.session_state['response']["sources"]) > 0:
            st.info("The answer below is generated by AI from only 5 YouTube videos so they might not be accurate", icon="ℹ️")
            bot_markdown(message_header="",
                        message=st.session_state['response']["answer"]+ '\n\n' + "Sources: " + st.session_state['response']["sources"].strip() )
        else:
            st.info("The answer below is generated by AI from only 5 YouTube videos so they might not be accurate", icon="ℹ️")
            bot_markdown(message_header="",
                        message=st.session_state['response']["answer"].strip())
                    
    elif submit_button and st.session_state['response'] == "":
        st.warning('Answer could not be generated, please try a different question.', icon="⚠️")

    st.markdown("<h3 style='color: #070038;'>Download your social listening report</h3>", unsafe_allow_html=True)
    
    email = st.text_input(label="Enter your email address and press Enter", value="")
    if email == "":
        report = ""
        export_as_pdf = st.button("Export Report", disabled=True)
    else:
        report = create_report(email,
                                query,
                                global_summary_chain_results['global_summary'],
                                competitors_summary_chain_results['competitors_summary'],
                                structured_ratings,
                                ratings_explanations)
        export_as_pdf = st.button("Export Report")
        if export_as_pdf:
            pdf = create_pdf(email,
                            query,
                            global_summary_chain_results['global_summary'],
                            competitors_summary_chain_results['competitors_summary'],
                            structured_ratings,
                            ratings_explanations)
            
            html = create_download_link(pdf.output(dest="S").encode("latin-1"), "pythie-report")

            st.markdown(html, unsafe_allow_html=True)

    

    

