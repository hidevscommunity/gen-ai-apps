import os
import streamlit as st
import base64
import logging
import glob
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_comment_downloader import *
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
Max_comments = 40
import numpy as np
import matplotlib.pyplot as plt
from keybert import KeyBERT
kw_extractor = KeyBERT('distilbert-base-nli-mean-tokens')

from dotenv import load_dotenv
load_dotenv()

import torch
from nltk.sentiment import SentimentIntensityAnalyzer
from fpdf import FPDF

from transformers import BertTokenizer, BertModel
from summa import keywords
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('vader_lexicon')


model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)
sid = SentimentIntensityAnalyzer()
stopwords = set(stopwords.words('english'))
root_path = os.getcwd()
logging.getLogger().setLevel(logging.INFO)


def get_youtube_transcripts(query: str, vid_nb: int, top_videos: str, lang: str):
    if lang == "French":
        search_query = query + " avis"
        videos_lang = "fr"
    else:
        search_query = query + " review"
        videos_lang = "en"
    ytb_api_key = st.secrets["youtube_api_key"]

    youtube = build('youtube', 'v3', developerKey=ytb_api_key)
    search_response = youtube.search().list(
        q=search_query,
        type='video',
        part='id,snippet',
        maxResults=vid_nb,
        relevanceLanguage=videos_lang,
        order=top_videos
    ).execute()

    video_ids = [search_result['id']['videoId'] for search_result in search_response.get('items', [])]
    videos = []
    video_ids = [item['id']['videoId'] for item in search_response['items']]

    # Retrieve comments for each video
    my_bar = st.progress(0, text="Videos download in progress. Please wait.")
    for i, video_id in enumerate(video_ids):
        my_bar.progress(int((i + 1)*100 / len(video_ids)), text="Videos download in progress. Please wait.")
        comments = []
        video_response = youtube.videos().list(
            id=video_id,
            part='id,snippet,statistics'
        ).execute()
        video_statistics = video_response['items'][0]['statistics']
        video_title = video_response['items'][0]['snippet']['title']
        video_channel = video_response['items'][0]['snippet']['channelTitle']
        try:
            video_transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[videos_lang])
        except:
            video_transcript = "No transcript available"
        try:
            viewCount = int(video_statistics['viewCount'])
        except KeyError:
            viewCount = 0
        try:
            likeCount = int(video_statistics['likeCount'])
        except KeyError:
            likeCount = 0
        try:
            commentCount = int(video_statistics['commentCount'])
        except KeyError:
            commentCount = 0
        try:
            comments_response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=10
            ).execute()
            for item in comments_response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
        except:
            pass
        videos.append({
            'id': video_id,
            'title': video_title,
            'channel': video_channel,
            'viewCount': int(viewCount),
            'likeCount': int(likeCount),
            'commentCount': int(commentCount),
            'thumbnails': video_response['items'][0]['snippet']['thumbnails']['medium']['url'],
            'transcript': video_transcript,
            'comments' : comments
        })
    my_bar.empty()
    return videos

def get_comments(videos):
    all_comments = []
    for video in videos:
        all_comments+=video["comments"]
    return all_comments

def get_keywords(text, size = 1, k = 10):

    keywords = kw_extractor.extract_keywords(text, keyphrase_ngram_range=(size, size), stop_words='english', nr_candidates=100, top_n=k)
    sorted_words = sorted(keywords, key=lambda x: x[1], reverse=True)
    return sorted_words

   

def build_transcripts(
        videos_list: list
    ) -> list:
    videos_transcripts = []
    for vid in videos_list:
        if vid['transcript'] != 'No transcript available':
            transcript = ""
            for chunk in vid['transcript']:
                transcript += chunk['text']
                transcript += " "
            transcript = transcript.replace('\n', ' ').replace('\xa0', '')
            videos_transcripts.append({"video_info": vid, "transcript": transcript})
    return videos_transcripts

# Delete texts files before generating new ones
def delete_transcripts(
        path: str,
        ext_path: str
    ) -> None:
    folder_path = path + ext_path[:-1]
    files = os.listdir(folder_path)
    if len(files) > 0:
        for file in files:
            file_path = os.path.join(folder_path, file)
            try:
                os.remove(file_path)
            except PermissionError:
                pass

# Saving transcriptions in texts files
def save_transcripts(
        videos_transcripts: list,
        max_videos: int,
        path: str,
        ext_path: str
    ) -> None:
    num_transcripts = 0
    analyzed_vids = []
    for vid_transcript in videos_transcripts:
        if len(vid_transcript['transcript']) > 1000:
            with open(path + ext_path + "video_{id}.txt".format(id=vid_transcript['video_info']['id']), "w") as file:
                logging.info("Saving transcript for video: {id}".format(id=vid_transcript['video_info']['id']))
                file.write(vid_transcript['transcript'])
                analyzed_vids.append(vid_transcript['video_info'])
                num_transcripts += 1
            file.close()
        if num_transcripts == max_videos:
            break
    return num_transcripts, analyzed_vids

def extract_words(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    filtered_words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word.isalpha() and word not in stop_words and nltk.pos_tag([word])[0][1] != 'VB'
    ]
    return filtered_words

def descriptive_words(text):
    text1 = extract_words(text)
    tokens = word_tokenize(' '.join(text1))
    # Perform Part-of-Speech tagging
    pos_tags = pos_tag(tokens)
    # Extract adjectives from the tagged words
    descriptivewords = [word for word, pos in pos_tags if pos.startswith('JJ')]
    return descriptivewords

def get_decriptive_words():
    path = "./data/videos_transcripts/main_product/*"
    files = glob.glob(path)
    results = []
    for file in files:
        with open(file,'rb') as f :
            text = f.read().decode(errors='replace')
            descriptivewords = descriptive_words(text)    
        results+=descriptivewords
    return ' '.join(results)

# def word_cloud(text,file_name = "wordcloud.png"):
#     from wordcloud import WordCloud
#     import matplotlib.pyplot as plt 
#     import nltk
#     from sklearn.feature_extraction.text import TfidfVectorizer

#     vectorizer = TfidfVectorizer()
#     vector = vectorizer.fit_transform([text])
#     words = vectorizer.get_feature_names_out() 
#     scores = vector.toarray()[0]
#     sorted_words = sorted(zip(words, scores), key=lambda x: x[1], reverse=True)
#     wordcloud = WordCloud(max_words=15, background_color='white')
#     wordcloud.generate_from_frequencies(dict(sorted_words))
#     wordcloud.to_file(file_name)
#     return file_name,wordcloud,sorted_words

def plot_radar_chart(sorted_words1, sorted_words2):
    # Common words from video script
    video_words = [word[0] for word in sorted_words1]
    video_scores = [word[1] * 100 for word in sorted_words1]
    
    # Common words from comments
    comment_words = [word[0] for word in sorted_words2]
    comment_scores = [word[1] * 100 for word in sorted_words2]
    
    num_vars = len(video_words)

    # Create an array of angles for the radar chart
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    video_scores += video_scores[:1]
    comment_scores += comment_scores[:1]
    angles += angles[:1]

    # Set the figure size

    fig, ax = plt.subplots(figsize=(4.5, 4), subplot_kw={'polar': True})

    # Plot the video script scores
    ax.plot(angles, video_scores, linewidth=2, label='Video Script')
    ax.fill(angles, video_scores, alpha=0.25)
    
    # Plot the comment scores
    ax.plot(angles, comment_scores, linewidth=2, label='Comments')
    ax.fill(angles, comment_scores, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(video_words, fontsize=10)
    ax.set_ylabel('')
    ax.legend(loc='upper right', prop={'size': 6})
    return plt, video_words, comment_words

# 

def clean_text(comment):
    # Remove HTML tags
    comment = re.sub('<.*?>', '', comment)
    # Remove special characters, symbols, and emojis
    comment = re.sub('[^a-zA-Z0-9\s]', '', comment)
    comment = comment.lower()
    tokens = word_tokenize(comment)
    # Remove stopwords and short words
    filtered_tokens = [token for token in tokens if token not in stopwords and len(token) > 3]
    filtered_tokens = [token for token in filtered_tokens if token.isalpha()]
    filtered_tokens = list(set(filtered_tokens))
    cleaned_comment = ' '.join(filtered_tokens)
    return cleaned_comment

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

def clean_comment(comment):
    tokens = word_tokenize(comment)
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english') and len(token) > 2]
    filtered_tokens = [token for token in filtered_tokens if token.isalpha()]
    cleaned_comment = ' '.join(filtered_tokens)
    return cleaned_comment

def get_words_with_scores(text, limit=10):
    script = clean_comment(text)
    script_tokens = tokenizer.encode(script, add_special_tokens=True, truncation=True, max_length=512, padding='max_length', return_tensors='pt')
    with torch.no_grad():
        outputs = model(script_tokens)
        embeddings = outputs.last_hidden_state

    # Extract keywords using TextRank
    script_text = tokenizer.decode(script_tokens.squeeze(), skip_special_tokens=True)
    extracted_keywords = keywords.keywords(script_text, ratio=0.7)  # Adjust the ratio as needed
    words = word_tokenize(extracted_keywords)  # Convert to list of words

    # Instantiate the VADER sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    # Calculate sentiment scores for each word
    word_scores = []
    for word in words:
        scores = sid.polarity_scores(word)
        word_scores.append((word, scores['compound']))

    # Sort words by their scores
    word_scores.sort(key=lambda x: x[1], reverse=True)

    return word_scores[:limit] if limit > 10 else word_scores


def html_code_generator(videos_info):
    html_topcode = """
    <!DOCTYPE html>
    <html>
    <head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <style>
        .card-container {
        display: flex;
        justify-content: space-between;
        margin: 1px;
        width: 100%;
        }

        .card {
        flex: 0 0 auto;
        width: 15rem;
        height: 16.2rem;
        margin-right: 2px;
        }

         .card-body {
        padding: 0.5rem;
        }

        .card-text {
        font-size: 12px;  /* Decrease the font size */
        margin-bottom: 0;  /* Remove the space between title and image */
        }

        .card img {
        width: 100%;
        height: auto;
        }

        a {
        color: black;
        }

        body {
        background-color: white;
        }
    </style>
    </head>
    <body>
    <div class="card-container">
    """.replace("\n", "")

    html_bottomcode = """
    </div>
    </body>
    </html>
    """.replace("\n", "")

    html_subcode = """
    <div class="card">
    <img src={img_url} class="card-img-top" alt="Image 2">
    <div class="card-body">
    <a href="{video_url}" target="_blank">
        <h8 class="card-text">{video_title}</h8>
        </a>
        <p style="margin-bottom: 0.1em;font-size: 10px">Channel: {channel}</p>
        <p style="margin-bottom: 0.1em;font-size: 10px">Views: {views}</p>
        <p style="margin-bottom: 0.1em;font-size: 10px">Likes: {likes}</p>
        <p style="margin-bottom: 0.1em;font-size: 10px">Comments: {comments}</p>
    </div>
    </div>
    """.replace("\n", "")

    for i in range(len(videos_info)):
        image_url = videos_info[i]['thumbnails']
        if len(videos_info[i]['title']) > 60:
            video_title = videos_info[i]['title'][:60] + '...'
        else:
            video_title = videos_info[i]['title']
        view_count = videos_info[i]['viewCount']
        like_count = videos_info[i]['likeCount']
        comment_count = videos_info[i]['commentCount']
        video_channel = videos_info[i]['channel']
        video_url = "https://www.youtube.com/watch?v=" + videos_info[i]['id']
        vid_subcode = html_subcode.format(img_url=image_url,
                                          video_title=video_title,
                                          views=number_format(view_count),
                                          likes=number_format(like_count),
                                          comments=number_format(comment_count),
                                          video_url=video_url,
                                          channel=video_channel)
        html_topcode += vid_subcode
    html_topcode += html_bottomcode

    return html_topcode


def number_format(number):
    if number >= 1000000000:
        return f"{number / 1000000000:.1f}B"
    if number >= 1000000:
        return f"{number / 1000000:.1f}M"
    elif number >= 1000:
        return f"{number / 1000:.1f}K"
    else:
        return str(number)
    
def calculate_totals(videos_info):
    total_views = 0
    total_likes = 0
    total_comments = 0
    for i in range(len(videos_info)):
        total_views += videos_info[i]['viewCount']
        total_likes += videos_info[i]['likeCount']
        total_comments += videos_info[i]['commentCount']
    str_total_views = number_format(total_views)
    str_total_likes = number_format(total_likes)
    str_total_comments = number_format(total_comments)
    return str_total_views, str_total_likes, str_total_comments

def generate_color(value):
    rating = float(value.split("/")[0])
    if rating < 5:
        return "**:red[{topic_rating}]**"
    elif rating < 8:
        return "**:orange[{topic_rating}]**"
    else:
        return "**:green[{topic_rating}]**"


def add_logo_from_local(logo_path):
    # Center the logo horizontally
    st.markdown(
        """
        <style>
        .logo-container {
            display: flex;
            justify-content: center;
        }
        .logo-container img {
            max-width: 200px; /* Adjust the value as needed */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # Add the logo to the page
    st.markdown(
        f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{get_base64_encoded_image(logo_path)}" alt="Logo">
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Add space below the logo
    st.write("\n")


def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode("utf-8")
    return encoded_string

def add_title(text):
    # add title
    st.markdown(
        """
        <style>
        .title-text {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f'<h1 class="title-text">{text}</h1>', unsafe_allow_html=True)

def add_subtitle(text):
    # add title
    st.markdown(
        """
        <style>
        .title-text {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<h3 class="title-text" style="text-align: center;">{text}</h1>',
        unsafe_allow_html=True,
    )

    
def create_report(email,
                  query,
                  global_summary,
                  competitors_summary,
                  structured_ratings,
                  ratings_explanations):
    

    ratings = ""
    for k in range(len(structured_ratings)):
        try:
            topic_rating_to_save = structured_ratings[k]["topic"] + ": " + structured_ratings[k]["rating"]
            rating_explanation_yo_save = ratings_explanations[structured_ratings[k]["topic"]]
            ratings += topic_rating_to_save
            ratings += "\n"
            ratings += rating_explanation_yo_save
            ratings += "\n\n"
        except:
            pass

    report = """
Email: {email}

Product: {query}

Discover reviewers impressions in just few lines
Let Google GenAI generate a summary of reviewers opinion about your product

{global_summary}

How your product compares to the competition
Let Google GenAI generate a comparison between your product and others mentioned in the videos

{competitors_summary}

How do your product features measure up
Let Google GenAI generate the highlighted product features and their rating

{ratings}
    """.format(email=email,
               query=query,
               global_summary=global_summary,
               competitors_summary=competitors_summary,
               ratings=ratings)

    return report

def create_pdf(email,
               query,
               global_summary,
               competitors_summary,
               structured_ratings,
               ratings_explanations):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    header_global_summary = """
Discover reviewers impressions in just few lines
Let Google GenAI generate a summary of reviewers opinion about your product 
    """
    header_competitors_summary = """
How your product compares to the competition
Let Google GenAI generate a comparison between your product and others mentioned in the videos
    """
    header_ratings = """
How do your product features measure up
Let Google GenAI generate the highlighted product features and their rating
    """
    ratings = ""
    for k in range(len(structured_ratings)):
        try:
            topic_rating_to_save = structured_ratings[k]["topic"] + ": " + structured_ratings[k]["rating"]
            rating_explanation_yo_save = ratings_explanations[structured_ratings[k]["topic"]]
            ratings += topic_rating_to_save
            ratings += "\n"
            ratings += rating_explanation_yo_save
            ratings += "\n\n"
        except:
            pass
    pdf_content = ["Disclaimer: The information in this report are generated by AI from only 5 YouTube videos so they might not be accurate",
                   "Email: " + email,
                   "Product: " + query,
                   header_global_summary,
                   global_summary,
                   header_competitors_summary,
                   competitors_summary,
                   header_ratings, ratings]
    for i, row in enumerate(pdf_content):
        if i in [0, 3, 5, 7]:
            pdf.set_font('Arial', 'B', 16)
            line_height = pdf.font_size
            pdf.multi_cell(0, line_height, row)
            pdf.ln()
        else:
            pdf.set_font('Arial', size=14)
            line_height = pdf.font_size
            pdf.multi_cell(0, line_height, row)
            pdf.ln()  # Move to the next line
    return pdf


def delete_old_embeddings(path):
    folder_path = path + "/.chroma/index"  # Path to the .chroma folder

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Iterate over the files in the folder and delete them
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            os.remove(file_path)
        logging.info("All files within .chroma folder deleted successfully.")
    else:
        logging.info(".chroma folder does not exist.")

def header_logo_html():
    html_string = (
    """
    <script>
    // To break out of iframe and access the parent window
    const streamlitDoc = window.parent.document;

    // Make the replacement
    document.addEventListener("DOMContentLoaded", function(event){
            streamlitDoc.getElementsByTagName("footer")[0].innerHTML = "Made with ♥️ by <a href='https://artefact.com/' target='_blank' class='css-z3au9t egzxvld2'>Artefact</a>";
        });
    document.addEventListener("DOMContentLoaded", function(event){
            streamlitDoc.getElementsByTagName("title")[0].innerHTML = "Pythie - An Artefact Project";
        });

    document.addEventListener("DOMContentLoaded", function(event){
            streamlitDoc.getElementsByTagName("header")[0].getElementsByTagName("div")[0].innerHTML = '<img src=\"data:image/png;base64,"""
        + get_base64_encoded_image("resources/artefact-genai-logo.png")
        + """\" style=\"height:58px; padding: 5px;\" />';
        });

    </script>
    """
    )

    return html_string

def bot_markdown(message_header, message):
    st.markdown(
        """
    <div style="background-color:#fafafa;color:#333;padding:10px;border-radius:5px;font-size:16px">
    <img src="data:image/png;base64,{}" style="height: 25px; width:25px;" /> Pythie:\n\n{}\n\n{}
    </div>
    <br>
    """.format(
            get_base64_encoded_image("resources/pocus-pin.png"), message_header, message
        ),
        unsafe_allow_html=True,
    )
