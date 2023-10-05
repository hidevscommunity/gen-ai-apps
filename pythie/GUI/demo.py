import importlib


# import GUI.utils
# importlib.reload(GUI.utils)
from GUI.utils import get_youtube_transcripts, save_transcripts, build_transcripts, delete_transcripts, get_comments

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain, TransformChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chat_models import AzureChatOpenAI
from dotenv import load_dotenv

from threading import Thread
import streamlit as st

import os
import re
import json
import time
import logging

load_dotenv()

logging.getLogger().setLevel(logging.INFO)

root_path = os.getcwd()

likes_dislikes_lang = {
                        'fr': {"Likes": "Points forts",
                            "Dislikes": "Points faibles"},
                        'en': {"Likes": "Likes",
                            "Dislikes": "Dislikes"},
                      }

with open(root_path + '/GUI/prompts.json', 'r') as file:
    prompts_dict = json.load(file)


def get_transcripts(
        query: str,
        max_video: int,
        top_videos: str,
        lang: str,
        path: str,
        ext_path: str
    ) -> int:
    logging.info('Started videos download')
    logging.info('Started transcripts download')
    first_start_time = time.time()
    videos_info = get_youtube_transcripts(query=query, vid_nb=20, top_videos=top_videos, lang=lang)
    logging.info(f'Finished transcripts download: {round(time.time() - first_start_time, 3)}s')

    logging.info('Started comments download')
    start_time = time.time()
    all_comments = get_comments(videos_info)
    logging.info(f'Finished comments download: {round(time.time() - start_time, 3)}s')

    logging.info('Started transcripts build')
    start_time = time.time()
    videos_transcripts = build_transcripts(videos_info)
    logging.info(f'Finished transcripts build: {round(time.time() - start_time, 3)}s')

    logging.info('Started old transcripts deletion')
    start_time = time.time()
    delete_transcripts(path, ext_path)
    logging.info(f'Finished old transcripts deletion: {round(time.time() - start_time, 3)}s')

    logging.info('Started transcripts saving')
    start_time = time.time()
    num_transcripts, analyzed_vids = save_transcripts(videos_transcripts, max_video, path, ext_path)
    logging.info(f'Finished transcripts saving: {round(time.time() - start_time, 3)}s')
    logging.info(f'Finished videos download: {round(time.time() - first_start_time, 3)}s')
    return analyzed_vids, all_comments

def get_global_overview(splitted_transcripts, videos_info, query, llm_model, lang):
    # chunk chain
    my_bar = st.progress(0, text="Analyzing videos in progress. Please wait.")
    logging.info('Started main product chunk chain')
    start_time = time.time()
    chunk_chain = build_chunk_chain(llm_model, lang)
    chunk_chain_results = run_chunk_chain(chunk_chain, splitted_transcripts, query)
    logging.info(f'Finished main product chunk chain: {round(time.time() - start_time, 3)}s')
    my_bar.progress(20, text="Analyzing videos in progress. Please wait.")

    # video chain
    logging.info('Started video chain')
    start_time = time.time()
    video_chain = build_video_chain(llm_model, lang)
    video_chain_results = run_video_chain(video_chain, chunk_chain_results, query, lang)
    logging.info(f'Finished video chain: {round(time.time() - start_time, 3)}s')
    my_bar.progress(40, text="Analyzing videos in progress. Please wait.")

    # topics chain
    logging.info('Started topics chain')
    start_time = time.time()
    topics_chain = build_topics_chain(llm_model, lang)
    topics_chain_results = topics_chain({"video_chain_output": video_chain_results, "product": query, "lang_code": lang})
    logging.info(f'Finished topics chain: {round(time.time() - start_time, 3)}s')
    my_bar.progress(70, text="Analyzing videos in progress. Please wait.")

    # condensing chain
    logging.info('Started condensing chain')
    start_time = time.time()
    condensing_chain = build_condensing_chain(llm_model, lang)
    condensing_chains_results = run_condensing_chains(condensing_chain, topics_chain_results, query, len(videos_info), lang)
    logging.info(f'Finished condensing chain: {round(time.time() - start_time, 3)}s')
    my_bar.progress(85, text="Analyzing videos in progress. Please wait.")

    # global overview chain
    logging.info('Started global overview chain')
    start_time = time.time()
    global_overview_chain = build_global_overview_chain(llm_model, lang)
    global_summary_chain_results = global_overview_chain({"local_summary_chains_results": condensing_chains_results,
                                                          "topics_chain_results": topics_chain_results,
                                                          "product": query,
                                                          "lang_code": lang})
    logging.info(f'Finished global overview chain: {round(time.time() - start_time, 3)}s')
    my_bar.progress(100, text="Analyzing videos in progress. Please wait.")
    my_bar.empty()
    return chunk_chain_results, topics_chain_results, condensing_chains_results, global_summary_chain_results

def get_competitors_overview(splitted_transcripts, query, llm_model, lang):
    my_bar = st.progress(0, text="Analyzing videos in progress. Please wait.")
    logging.info('Started competitors chunk chain')
    start_time = time.time()
    chunk_competitors_chain = build_chunk_competitors_chain(llm_model, lang)
    my_bar.progress(10, text="Analyzing videos in progress. Please wait.")
    chunk_competitors_chain_results = run_chunk_competitors_chain(chunk_competitors_chain, splitted_transcripts, query)
    logging.info(f'Finished competitors chunk chain: {round(time.time() - start_time, 3)}s')

    logging.info('Started competitors summary chain')
    start_time = time.time()
    my_bar.progress(50, text="Analyzing videos in progress. Please wait.")
    competitors_summary_chain = build_competitors_summary_chain(llm_model, lang)
    my_bar.progress(70, text="Analyzing videos in progress. Please wait.")
    competitors_summary_chain_results = competitors_summary_chain({"chunk_competitors_chain_results": chunk_competitors_chain_results,
                                                                   "product": query,
                                                                   "lang_code": lang})
    logging.info(f'Finished competitors summary chain: {round(time.time() - start_time, 3)}s')
    my_bar.progress(100, text="Analyzing videos in progress. Please wait.")
    my_bar.empty()
    return competitors_summary_chain_results

def get_comparison(product, splitted_transcripts, main_product, main_product_chunk_chain_results, llm_model, lang):
    my_bar = st.progress(0, text="Analyzing videos in progress. Please wait.")
    logging.info('Started product chunk chain')
    start_time = time.time()
    chunk_chain = build_chunk_chain(llm_model, lang)
    my_bar.progress(10, text="Analyzing videos in progress. Please wait.")
    product_chunk_chain_results = run_chunk_chain(chunk_chain, splitted_transcripts, product)
    logging.info(f'Finished product chunk chain: {round(time.time() - start_time, 3)}s')
    my_bar.progress(50, text="Analyzing videos in progress. Please wait.")

    logging.info('Started comparison chain')
    start_time = time.time()
    comparison_chain = build_comparison_chain(llm_model, lang)
    my_bar.progress(70, text="Analyzing videos in progress. Please wait.")
    comparison_chain_results = comparison_chain({"chunk_chain_output_main_product": main_product_chunk_chain_results,
                                                 "chunk_chain_output_product": product_chunk_chain_results,
                                                 "main_product": main_product,
                                                 "product": product})
    logging.info(f'Finished comparison chain: {round(time.time() - start_time, 3)}s')
    my_bar.progress(100, text="Analyzing videos in progress. Please wait.")
    my_bar.empty()
    return comparison_chain_results

def get_topics_ratings(topics_chain_results, condensing_chains_results, query, llm_model, lang):
    logging.info('Started rating topics chain')
    start_time = time.time()
    rating_topics_chain = build_rating_topics_chain(llm_model, lang)
    rating_topics_chain_results = rating_topics_chain({"assigned_topics_list": topics_chain_results['assigned_topics_list'],
                                                       "topics_list_w_others": topics_chain_results['topics_str'],
                                                       "condensing_chains_results": condensing_chains_results,
                                                       "topics_chain_results": topics_chain_results,
                                                       "product": query,
                                                       "lang_code": lang})
    logging.info(f'Finished rating topics chain: {round(time.time() - start_time, 3)}s')
    
    return rating_topics_chain_results

def get_suggested_questions(global_summary_chain_results, query, llm_model, lang):
    logging.info('Started suggested questions chain')
    start_time = time.time()
    questions_generation_chain = build_questions_generation(llm_model, lang)
    questions_generation_chain_results = questions_generation_chain({"global_summary": global_summary_chain_results['global_summary'], "product": query})
    logging.info(f'Finished suggested questions chain: {round(time.time() - start_time, 3)}s')
    return questions_generation_chain_results

def split_transcripts(videos_info: list, path: str, ext_path: str) -> list:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=50)
    folder_path = path + ext_path
    file_count = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
    transcripts_chunks = []
    for k in range(file_count):
        loader = TextLoader(root_path + ext_path + "video_{id}.txt".format(id=videos_info[k]['id']))
        doc = loader.load()
        chunks = text_splitter.split_documents(doc)
        video_chunks = dict({"video_id": videos_info[k]['id'], "chunks": chunks})
        transcripts_chunks.append(video_chunks)
    return transcripts_chunks

###############################################
############ Globale overview chain ###########
###############################################

########### Chunk chain ############
def build_chunk_chain(llm_model, lang):
    llm = llm_model
    summary_prompt_template = PromptTemplate(input_variables=["transcript_chunk", "product"],
                                             template=prompts_dict[lang]["summary_template"])
    summary_chain = LLMChain(llm=llm, prompt=summary_prompt_template, output_key="chunk_summary")

    chain = SequentialChain(chains=[summary_chain],
                                    input_variables=["transcript_chunk", "product", "video_id"],
                                    output_variables=["chunk_summary"],
                                    verbose=False)
    return chain

def run_chunk_chain(chain, transcript_chunks, product) -> list:
    threads = []
    results = []

    for k in range(len(transcript_chunks)):
        video_id = transcript_chunks[k]['video_id']
        for j in range(len(transcript_chunks[k]['chunks'])):
            chunk = transcript_chunks[k]['chunks'][j].page_content
            thread = Thread(target=call_api_chunk, args=(chain, chunk, product, video_id, results))
            threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    
    return results

def call_api_chunk(chain, docu, product, video_id, chain_result):
    results = chain({"transcript_chunk": docu, "product": product, "video_id": video_id})
    chain_result.append(results)

########### Video chain ############
def concat_chunk_summaries(inputs: dict) -> dict:
    chunk_results = inputs['chunk_chain_output']
    video_id = inputs['video_id']
    key = "video_id"
    value = video_id
    filtered_dicts = [d for d in chunk_results if d.get(key) == value]
    chunks_summaries = ""
    for chunk_info in filtered_dicts:
        chunks_summaries += chunk_info['chunk_summary']
        chunks_summaries += " "
    return {"combined_chunks_summary": chunks_summaries}

def format_video_likes_dislikes(inputs: dict) -> dict:
    raw_likes_dislikes = inputs['video_raw_likes_dislikes']
    lang_code = inputs['lang_code']
    likes_dislikes = raw_likes_dislikes.split('\n\n')
    video_likes_dislikes = ""
    if len(likes_dislikes) == 2:
        likes = likes_dislikes[0]
        dislikes = likes_dislikes[1]

        phrases = re.findall(r'-\s(.+)', likes)
        video_likes_dislikes += likes_dislikes_lang[lang_code]['Likes'] + ":\n"
        for phrase in phrases:
            video_likes_dislikes += "- " + phrase + "\n"
        
        video_likes_dislikes += "\n"
        video_likes_dislikes += likes_dislikes_lang[lang_code]['Dislikes'] + ":\n"
        phrases = re.findall(r'-\s(.+)', dislikes)
        for phrase in phrases:
            video_likes_dislikes += "- " + phrase + "\n"
    else:
        video_likes_dislikes = likes_dislikes_lang[lang_code]['Likes'] + ":\n\n" + likes_dislikes_lang[lang_code]['Dislikes']
    video_likes_dislikes.rstrip()
    return {"video_likes_dislikes": video_likes_dislikes}

def build_video_chain(llm_model, lang):
    llm = llm_model

    # TransformChain
    concat_summaries_chain = TransformChain(input_variables=["chunk_chain_output", "video_id"],
                                            output_variables=["combined_chunks_summary"],
                                            transform=concat_chunk_summaries)

    # LLMChain
    video_likes_dislikes_prompt_template = PromptTemplate(input_variables=["combined_chunks_summary", "product"],
                                                          template=prompts_dict[lang]["video_likes_dislikes_prompt"])
    video_likes_dislikes_chain = LLMChain(llm=llm,
                                          prompt=video_likes_dislikes_prompt_template,
                                          output_key="video_raw_likes_dislikes")
    
    # TransformChain
    format_video_likes_dislikes_chain = TransformChain(input_variables=["video_raw_likes_dislikes", "lang_code"],
                                                       output_variables=["video_likes_dislikes"],
                                                       transform=format_video_likes_dislikes)

    chain = SequentialChain(chains=[concat_summaries_chain,
                                    video_likes_dislikes_chain,
                                    format_video_likes_dislikes_chain],
                            input_variables=["chunk_chain_output", "product", "video_id", "lang_code"],
                            output_variables=["video_likes_dislikes", "combined_chunks_summary"],
                            verbose=False)
    return chain

def run_video_chain(chain, chunk_output, product, lang_code) -> list:
    threads = []
    results = []

    for id in {d['video_id'] for d in chunk_output}:
        thread = Thread(target=call_api_video, args=(chain, chunk_output, product, id, lang_code, results))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    
    return results

def call_api_video(chain, chunk_output, product, video_id, lang_code, chain_result):
    results = chain({"chunk_chain_output": chunk_output, "product": product, "video_id": video_id, "lang_code": lang_code})
    chain_result.append(results)


########### Topics chain ############
def transform_string(input_string, lang_code):
    likes = []
    dislikes = []
    current_list = likes

    for line in input_string.split("\n"):
        line = line.strip()
        if line == likes_dislikes_lang[lang_code]['Likes'] + ":":
            current_list = likes
        elif line == likes_dislikes_lang[lang_code]['Dislikes'] + ":":
            current_list = dislikes
        elif line != "":
            current_list.append(line)

    transformed_string = likes_dislikes_lang[lang_code]['Likes'] + ":\n"
    transformed_string += "\n".join(likes)
    transformed_string += "\n\n" + likes_dislikes_lang[lang_code]['Dislikes'] + ":\n"
    transformed_string += "\n".join(dislikes)

    return transformed_string

def concat_videos_likes_dislikes(inputs: dict) -> dict:
    video_results = inputs['video_chain_output']
    lang_code = inputs['lang_code']
    video_summaries = ""
    for video_info in video_results:
        video_summaries += video_info['video_likes_dislikes']
        video_summaries += "\n\n"
    video_summaries = video_summaries.rstrip()
    video_summaries = transform_string(video_summaries, lang_code)
    return {"combined_likes_dislikes": video_summaries}

def get_videos_likes_dislikes_bullet_points(inputs: dict) -> dict:
    likes_dislikes_bullet_points = ""
    text = inputs['combined_likes_dislikes']
    phrases = re.findall(r'-\s(.+)', text)
    for phrase in phrases:
        likes_dislikes_bullet_points += phrase + " "
    return {"likes_dislikes_bullet_points": likes_dislikes_bullet_points}

def check_generated_topics(inputs: dict) -> dict:
    raw_topics_llm = inputs['topics_list']
    lang_code = inputs['lang_code']
    raw_topics = re.findall(r'-\s(.+)', raw_topics_llm)
    good_topics = []
    for i, raw_topic in enumerate(raw_topics):
        if len(raw_topic.split(" ")) > 3:
            continue
        good_topics.append(raw_topic)
    topics = good_topics[:10]
    topics_str = ""
    for i in range(len(topics)):
        topics_str += "- " + topics[i] + "\n"
    if lang_code == "fr":
        topics_str += "- " + "Autre" + "\n"
    else:
        topics_str += "- " + "Other" + "\n"
    topics_str = topics_str.rstrip()
    return {"topics": topics, "topics_str": topics_str}

def extract_summary_topics(text, possible_topics) -> dict:
    pattern = r'\(([^)]+)\)$'
    matches = re.findall(pattern, text, re.MULTILINE)
    topics = []
    for detected in matches:
        words = detected.split(',')
        good_words = [word.strip() for word in words]
        topics.extend(good_words)
    unique_topics = list(set(topics))
    unique_topics = [item for item in unique_topics if item in possible_topics]
    if "Other" in unique_topics:
        unique_topics.remove("Other")
    if "Autre" in unique_topics:
        unique_topics.remove("Autre")
    return unique_topics

def get_likes_dislikes_topics(inputs: dict) -> dict:
    assigned_topics_list = inputs['assigned_topics_list']
    lang_code = inputs['lang_code']
    possible_topics = inputs['topics']
    try:
        likes, dislikes = assigned_topics_list.split(likes_dislikes_lang[lang_code]['Dislikes'] + ":")
        likes_topics = extract_summary_topics(likes, possible_topics)
        dislikes_topics = extract_summary_topics(dislikes, possible_topics)
        likes_dislikes_topics = {"likes_topics": likes_topics, "dislikes_topics": dislikes_topics}
    except:
        print('ENTERED EXCEPTION')
        likes_dislikes_topics = {"likes_topics": possible_topics, "dislikes_topics": possible_topics}
    return {"likes_dislikes_topics": likes_dislikes_topics}

def build_topics_chain(llm_model, lang):
    llm = llm_model
    
    # TransformChain
    concat_likes_dislikes_chain = TransformChain(input_variables=["video_chain_output", "lang_code"],
                                                 output_variables=["combined_likes_dislikes"],
                                                 transform=concat_videos_likes_dislikes)
    
    # TransformChain
    likes_dislikes_bullet_points_chain = TransformChain(input_variables=["combined_likes_dislikes"],
                                            output_variables=["likes_dislikes_bullet_points"],
                                            transform=get_videos_likes_dislikes_bullet_points)
    
    # LLMChain
    topics_generation_prompt_template = PromptTemplate(input_variables=["likes_dislikes_bullet_points", "product"],
                                                       template=prompts_dict[lang]["topics_generation_prompt"])
    topics_generation_chain = LLMChain(llm=llm,
                                       prompt=topics_generation_prompt_template,
                                       output_key="topics_list")
    
    # TransformChain
    check_generated_topics_chain = TransformChain(input_variables=["topics_list", "lang_code"],
                                                 output_variables=["topics", "topics_str"],
                                                 transform=check_generated_topics)
    
    # LLMChain
    topics_assignement_prompt_template = PromptTemplate(input_variables=["combined_likes_dislikes", "topics_str", "product"],
                                                        template=prompts_dict[lang]["assign_specific_topics"])
    topics_assignement_chain = LLMChain(llm=llm,
                                        prompt=topics_assignement_prompt_template,
                                        output_key="assigned_topics_list")

    # TransformChain
    get_likes_dislikes_topics_chain = TransformChain(input_variables=["assigned_topics_list", "topics", "lang_code"],
                                            output_variables=["likes_dislikes_topics"],
                                            transform=get_likes_dislikes_topics)
    
    
    chain = SequentialChain(chains=[concat_likes_dislikes_chain,
                                    likes_dislikes_bullet_points_chain,
                                    topics_generation_chain,
                                    check_generated_topics_chain,
                                    topics_assignement_chain,
                                    get_likes_dislikes_topics_chain,
                                    ],
                                    input_variables=["video_chain_output", "product", "lang_code"],
                                    output_variables=["topics_list",
                                                      "topics_str",
                                                      "assigned_topics_list",
                                                      "likes_dislikes_topics",
                                                      ],
                                    verbose=False)
    return chain

########### Condensing chain ############
def extract_topic_points(inputs: dict) -> dict:
    topic = inputs['topic']
    context = inputs['context']
    lang_code = inputs['lang_code']
    if context == "likes_topics":
        input_string = inputs['assigned_topics_list'].split(likes_dislikes_lang[lang_code]['Dislikes'] + ":")[0]
    elif context == "dislikes_topics":
        input_string = inputs['assigned_topics_list'].split(likes_dislikes_lang[lang_code]['Dislikes'] + ":")[1]
    pattern = r'- (.*?) \(' + topic + r'\)'
    bullet_points = re.findall(pattern, input_string)
    related_points = ""
    for bullet_point in bullet_points:
        related_points += "- "
        related_points += bullet_point
        related_points += "\n"
    related_points = related_points.rstrip()
    return {"related_points": related_points}

def get_count(inputs: dict) -> dict:
    nb_vids = inputs['nb_vids']
    string = inputs['combined_points']
    pattern = r"\((\d+)\)$"
    bullet_points_count = []
    for point in string.split("\n"):
        if point.startswith("- "):
            matches1 = re.findall(pattern, point)
            if len(matches1) > 0:
                modified_point = point.replace(" (" + matches1[0] + ")", "")
                if int(matches1[0]) > nb_vids:
                    matches1[0] = nb_vids
                bullet_points_count.append({"bullet_point" : point,
                                            "modified_bullet_point" : modified_point,
                                            "count" : int(matches1[0]),
                                            "count_percentage": str(round(100 * int(matches1[0]) / nb_vids)) + "%"})
            else:
                bullet_points_count.append({"bullet_point" : point,
                                            "modified_bullet_point" : point,
                                            "count" : 1,
                                            "count_percentage": str(round(100 * 1 / nb_vids)) + "%"})
    bullet_points_count = sorted(bullet_points_count, key=lambda x: x['count'], reverse=True)
    return {"bullet_points_count": bullet_points_count}

def build_condensing_chain(llm_model, lang):
    llm = llm_model

    # TransformChain
    extract_topic_points_chain = TransformChain(input_variables=["assigned_topics_list", "topic", "context", "lang_code"],
                         output_variables=["related_points"],
                         transform=extract_topic_points)
    
    # LLMChain
    condense_points_template = PromptTemplate(input_variables=["related_points", "product", "topic"],
                                              template=prompts_dict[lang]["condense_points"])
    condense_points_chain = LLMChain(llm=llm,
                                     prompt=condense_points_template,
                                     output_key="combined_points")
    
    # TransformChain
    get_count_chain = TransformChain(input_variables=["combined_points", "nb_vids"],
                                     output_variables=["bullet_points_count"],
                                     transform=get_count)

    chain = SequentialChain(chains=[extract_topic_points_chain, condense_points_chain, get_count_chain],
                            input_variables=["assigned_topics_list", "product", "topic", "context", "nb_vids", "lang_code"],
                            output_variables=["combined_points", "bullet_points_count", "related_points"],
                            verbose=False)

    return chain

def run_condensing_chains(chain, topics_chain_results, product, nb_vids, lang_code) -> list:
    threads = []
    results = []

    for context in topics_chain_results['likes_dislikes_topics']:
        for topic in topics_chain_results['likes_dislikes_topics'][context]:
            thread = Thread(target=call_api_condensing, args=(chain, topics_chain_results['assigned_topics_list'], topic, product, context, nb_vids, lang_code, results))
            threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    
    return results

def call_api_condensing(chain, assigned_topics_list, topic, product, context, nb_vids, lang_code, chain_result):
    results = chain({"assigned_topics_list": assigned_topics_list, "topic": topic, "product": product, "context": context, "nb_vids": nb_vids, "lang_code": lang_code})
    chain_result.append(results)

########### Global overview chain ############
def create_local_summary(inputs: dict) -> dict:
    local_summary_chains_results = inputs["local_summary_chains_results"]
    lang_code = inputs["lang_code"]
    likes = likes_dislikes_lang[lang_code]['Likes'] + ":\n"
    dislikes = likes_dislikes_lang[lang_code]['Dislikes'] + ":\n"
    for k in local_summary_chains_results:
        if k['context'] == "likes_topics":
            for l in k['bullet_points_count']:
                likes += l['modified_bullet_point']
                likes += "\n" 
        elif k['context'] == "dislikes_topics":
            for l in k['bullet_points_count']:
                dislikes += l['modified_bullet_point']
                dislikes += "\n"
    local_summary = likes + "\n" + dislikes
    return {"local_summary": local_summary}

def build_global_overview_chain(llm_model, lang):
    llm = llm_model

    create_local_summary_chain = TransformChain(input_variables=["local_summary_chains_results", "lang_code"],
                                                output_variables=["local_summary"],
                                                transform=create_local_summary)
    
    global_summary_template = PromptTemplate(input_variables=["local_summary", "product"],
                                             template=prompts_dict[lang]["global_summary"])
    global_summary_creation_chain = LLMChain(llm=llm,
                                             prompt=global_summary_template,
                                             output_key="global_summary")
    
    chain = SequentialChain(chains=[create_local_summary_chain,
                                    global_summary_creation_chain,
                                    ],
                            input_variables=["local_summary_chains_results",
                                             "topics_chain_results",
                                             "product",
                                             "lang_code"],
                            output_variables=["local_summary",
                                              "global_summary",
                                            ],
                            verbose=False)

    return chain

###############################################
############## Competitors chain ##############
###############################################

########### Chunk competitors chain ############
def build_chunk_competitors_chain(llm_model, lang):
    llm = llm_model
    chunk_competitors_prompt_template = PromptTemplate(input_variables=["transcript_chunk", "product"],
                                                       template=prompts_dict[lang]["chunk_competitors_prompt"])
    chunk_competitors_chain = LLMChain(llm=llm, prompt=chunk_competitors_prompt_template, output_key="chunk_competitors_summary")

    chain = SequentialChain(chains=[chunk_competitors_chain],
                                    input_variables=["transcript_chunk", "product"],
                                    output_variables=["chunk_competitors_summary"],
                                    verbose=False)
    return chain

def run_chunk_competitors_chain(chain, transcript_chunks, product) -> list:
    threads = []
    results = []

    for k in range(len(transcript_chunks)):
        for j in range(len(transcript_chunks[k]['chunks'])):
            chunk = transcript_chunks[k]['chunks'][j].page_content
            thread = Thread(target=call_api_chunk_competitors, args=(chain, chunk, product, results))
            threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    
    return results

def call_api_chunk_competitors(chain, docu, product, chain_result):
    results = chain({"transcript_chunk": docu, "product": product})
    chain_result.append(results)

########### Competitors summary chain ############
def concat_chunk_competitors_results(inputs: dict) -> dict:
    chunk_competitors_chain_results = inputs['chunk_competitors_chain_results']
    lang_code = inputs['lang_code']
    concat_results = ""
    for k in range(len(chunk_competitors_chain_results)):
        if lang_code == "fr":
            if chunk_competitors_chain_results[k]['chunk_competitors_summary'] != 'Aucune information comparative trouvée':
                concat_results += chunk_competitors_chain_results[k]['chunk_competitors_summary']
                concat_results += " "
        else:  
            if chunk_competitors_chain_results[k]['chunk_competitors_summary'] != 'No comparison informations found':
                concat_results += chunk_competitors_chain_results[k]['chunk_competitors_summary']
                concat_results += " "
    concat_results = re.sub(r'\n+', ' ', concat_results)
    return {"concat_competitors_info": concat_results}

def transform_string_to_list(inputs: dict) -> dict:
    string = inputs['detected_competitors_products']
    products = string.strip().split('\n')
    products = [product.strip().lstrip('- ') for product in products]
    products = products[:2]
    return {"detected_products_list": products}

def build_competitors_summary_chain(llm_model, lang):
    llm = llm_model
    
    # TransformChain
    concat_chunk_competitors_results_chain = TransformChain(input_variables=["chunk_competitors_chain_results", "lang_code"],
                                                            output_variables=["concat_competitors_info"],
                                                            transform=concat_chunk_competitors_results)
    
    # LLMChain
    # competitors_summary_prompt_template = PromptTemplate(input_variables=["concat_competitors_info", "product"], template=competitors_summary_prompt)
    # competitors_summary_chain = LLMChain(llm=llm,
    #                                      prompt=competitors_summary_prompt_template,
    #                                      output_key="competitors_summary")
    
    # LLMChain
    competitors_products_detection_prompt_template = PromptTemplate(input_variables=["concat_competitors_info", "product"],
                                                                    template=prompts_dict[lang]["competitors_products_detection_prompt"])
    competitors_products_detection_chain = LLMChain(llm=llm,
                                         prompt=competitors_products_detection_prompt_template,
                                         output_key="detected_competitors_products")
    
    # TransformChain
    transform_string_to_list_chain = TransformChain(input_variables=["detected_competitors_products"],
                                                            output_variables=["detected_products_list"],
                                                            transform=transform_string_to_list)
    
    chain = SequentialChain(chains=[concat_chunk_competitors_results_chain,
                                    competitors_products_detection_chain,
                                    transform_string_to_list_chain],
                            input_variables=["chunk_competitors_chain_results", "product", "lang_code"],
                            output_variables=["detected_competitors_products", "detected_products_list"],
                            verbose=False)

    return chain

###############################################
################ Ratings chain ################
###############################################

########### Topics ratings chain ############
def remove_other_topics(inputs: dict) -> dict:
    topics_list = inputs['topics_list_w_others']
    lang_code = inputs['lang_code']
    if lang_code == "fr":
        topics_list = topics_list.replace("- Autre", "")
    else:
        topics_list = topics_list.replace("- Other", "")
    topics_list = topics_list.replace("\n\n", "\n")
    return {"topics_list": topics_list}

def structure_ratings(inputs: dict) -> dict:
    text = inputs['topics_rating']
    lines = text.split("\n")
    structured_ratings = []
    for line in lines:
        line = line.strip()
        if line.startswith("- "):
            line = line[2:]
        topic, rating = line.split(": ")
        structured_ratings.append({"topic": topic.strip(), "rating": rating})
    return {"structured_ratings": structured_ratings}

def get_topics_likes_dislikes(inputs: dict) -> dict:
    condensing_chains_results = inputs["condensing_chains_results"]
    lang_code = inputs["lang_code"]
    topics_chain_results = inputs["topics_chain_results"]
    topics_list = [topic.replace("- ", "").rstrip().lstrip() for topic in topics_chain_results['topics_list'].split("\n")]
    topics_likes_dislikes = {}
    for topic in topics_list:
        filtered_dicts = [d for d in condensing_chains_results if d.get('topic') == topic]
        likes = likes_dislikes_lang[lang_code]['Likes'] + ":\n"
        dislikes = likes_dislikes_lang[lang_code]['Dislikes'] + ":\n"
        for k in filtered_dicts:
            if k['context'] == "likes_topics":
                for l in k['bullet_points_count']:
                    likes += l['modified_bullet_point']
                    if lang_code == "fr":
                        likes += " - *Mentionné par: "
                    else:
                        likes += " - *Mentioned by: "
                    likes += l['count_percentage']
                    likes += "*"
                    likes += "\n" 
            elif k['context'] == "dislikes_topics":
                for l in k['bullet_points_count']:
                    dislikes += l['modified_bullet_point']
                    if lang_code == "fr":
                        dislikes += " - *Mentionné par: "
                    else:
                        dislikes += " - *Mentioned by: "
                    dislikes += l['count_percentage']
                    dislikes += "*"
                    dislikes += "\n"
        if likes == likes_dislikes_lang[lang_code]['Likes'] + ":\n" and dislikes != likes_dislikes_lang[lang_code]['Dislikes'] + ":\n":
            local_summary = dislikes
        elif likes != likes_dislikes_lang[lang_code]['Likes'] + ":\n" and dislikes == likes_dislikes_lang[lang_code]['Dislikes'] + ":\n":
            local_summary = likes
        elif likes == likes_dislikes_lang[lang_code]['Likes'] + ":\n" and dislikes == likes_dislikes_lang[lang_code]['Dislikes'] + ":\n":
            local_summary = ""
            continue
        else:
            local_summary = likes + "\n" + dislikes
        topics_likes_dislikes[topic] = local_summary
    return {"topics_likes_dislikes": topics_likes_dislikes}

def build_rating_topics_chain(llm_model, lang):
    llm = llm_model

    # TransformChain
    remove_other_topic_chain = TransformChain(input_variables=["topics_list_w_others", "lang_code"],
                                             output_variables=["topics_list"],
                                             transform=remove_other_topics)

    # LLMChain
    rate_topics_template = PromptTemplate(input_variables=["assigned_topics_list", "topics_list", "product"],
                                          template=prompts_dict[lang]["rate_topics_prompt"])
    rate_topics_chain = LLMChain(llm=llm,
                                 prompt=rate_topics_template,
                                 output_key="topics_rating")

    # TransformChain
    structure_ratings_chain = TransformChain(input_variables=["topics_rating"],
                                             output_variables=["structured_ratings"],
                                             transform=structure_ratings)
    
    # TransformChain
    get_topics_likes_dislikes_chain = TransformChain(input_variables=["condensing_chains_results",
                                                                      "topics_chain_results",
                                                                      "lang_code"],
                                                     output_variables=["topics_likes_dislikes"],
                                                     transform=get_topics_likes_dislikes)
    
    chain = SequentialChain(chains=[remove_other_topic_chain, 
                                    rate_topics_chain, 
                                    structure_ratings_chain, 
                                    get_topics_likes_dislikes_chain],
                            input_variables=["assigned_topics_list",
                                             "topics_list_w_others",
                                             "product",
                                             "condensing_chains_results",
                                             "topics_chain_results",
                                             "lang_code"],
                            output_variables=["structured_ratings", "topics_likes_dislikes"],
                            verbose=False)

    return chain

###############################################
################### Chatbot ###################
###############################################

def check_suggested_questions(inputs: dict) -> dict:
    raw_suggested_questions = inputs['raw_suggested_questions']
    product = inputs['product']
    suggested_questions = raw_suggested_questions.split("\n")
    suggested_questions = [suggested_question.split(": ", 1)[1].strip() for suggested_question in suggested_questions if suggested_question.strip()]
    if len(suggested_questions) < 3:
        suggested_questions = ['Generate a SEO blog paragraph, that showcase the features of the ' + product + '.',
                               'Generate 3 ad-copies showcasing the' + product + ', with headlines and bodies, and include long-tail keywords on which I can bid on.',
                               'Make an advertising script about the ' + product + '.']
    return {"suggested_questions": suggested_questions}

def build_questions_generation(llm_model, lang):
    llm = llm_model
    
    # LLMChain
    questions_generation_prompt_template = PromptTemplate(input_variables=["global_summary", "product"],
                                          template=prompts_dict[lang]["questions_generation_prompt"])
    questions_generation_chain = LLMChain(llm=llm,
                                 prompt=questions_generation_prompt_template,
                                 output_key="raw_suggested_questions")
    
    # TransformChain
    check_suggested_questions_chain = TransformChain(input_variables=["raw_suggested_questions", "product"],
                                             output_variables=["suggested_questions"],
                                             transform=check_suggested_questions)
    
    chain = SequentialChain(chains=[questions_generation_chain, check_suggested_questions_chain],
                            input_variables=["global_summary", "product"],
                            output_variables=["raw_suggested_questions", "suggested_questions"],
                            verbose=False)

    return chain

def prepare_docs(files_path: str ,
                 videos_info: list,
                 ext_path: str,
                 embedding_model: str
                 ):
    logging.info('Started building embedding index')
    start_time = time.time()
    loader = DirectoryLoader(files_path + ext_path[:-1], glob=f"*.txt", loader_cls=TextLoader)
    documents = loader.load()
    videos_ids = [documents[k].metadata['source'].split('/')[-1].replace('.txt', '').replace('video_', '') for k in range(len(documents))]
    for i, id in enumerate(videos_ids):
        video_title = [d for d in videos_info if d.get('id') == id][0]['title']
        documents[i].metadata['source'] = video_title + ": https://www.youtube.com/watch?v=" + id
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    texts = [doc.page_content for doc in docs]
    metadata = [doc.metadata for doc in docs]
    embeddings = embedding_model
    docsearch = Chroma.from_texts(texts, embeddings, metadatas=metadata)
    logging.info(f'Finished building embedding index: {time.time() - start_time}s')
    return docsearch


def get_response(question, docsearch, llm_model, lang):
    logging.info('Started generating answer')
    start_time = time.time()
    repsonse_template = prompts_dict[lang]["response_prompts"]
    
    PROMPT = PromptTemplate(template=repsonse_template, input_variables=["summaries", "question"])
    llm = llm_model
    chain = load_qa_with_sources_chain(llm, chain_type="stuff", prompt=PROMPT)
    qa = RetrievalQAWithSourcesChain(combine_documents_chain=chain, retriever=docsearch.as_retriever())
    answer = qa({"question": question}, return_only_outputs=True)
    logging.info(f'Finished generating answer: {time.time() - start_time}s')
    return answer



###############################################
############### Comparison chain ##############
###############################################

def concat_chunk_summaries_main_product(inputs: dict) -> dict:
    chunk_results = inputs['chunk_chain_output_main_product']
    chunks_summaries = ""
    for chunk_info in chunk_results:
        chunks_summaries += chunk_info['chunk_summary']
        chunks_summaries += " "
    return {"combined_chunks_summary_main_product": chunks_summaries}

def concat_chunk_summaries_product(inputs: dict) -> dict:
    chunk_results = inputs['chunk_chain_output_product']
    chunks_summaries = ""
    for chunk_info in chunk_results:
        chunks_summaries += chunk_info['chunk_summary']
        chunks_summaries += " "
    return {"combined_chunks_summary_product": chunks_summaries}

def build_comparison_chain(llm_model, lang):
    llm = llm_model

    # TransformChain
    concat_summaries_chain_main_product = TransformChain(input_variables=["chunk_chain_output_main_product"],
                                            output_variables=["combined_chunks_summary_main_product"],
                                            transform=concat_chunk_summaries_main_product)
    
    # TransformChain
    concat_summaries_chain_product = TransformChain(input_variables=["chunk_chain_output_product"],
                                            output_variables=["combined_chunks_summary_product"],
                                            transform=concat_chunk_summaries_product)

    # LLMChain
    comparison_prompt_template = PromptTemplate(input_variables=["product",
                                                                 "main_product",
                                                                 "combined_chunks_summary_main_product",
                                                                 "combined_chunks_summary_product"],
                                                template=prompts_dict[lang]["comparison_prompt"])
    comparison_chain = LLMChain(llm=llm, prompt=comparison_prompt_template, output_key="comparison_summary")

    chain = SequentialChain(chains=[concat_summaries_chain_main_product,
                                    concat_summaries_chain_product,
                                    comparison_chain],
                                    input_variables=["chunk_chain_output_main_product",
                                                     "chunk_chain_output_product",
                                                     "main_product",
                                                     "product"],
                                    output_variables=["comparison_summary"],
                                    verbose=False)
    return chain

