from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
import json
import ingest
import run_localGPT
import utils

def audio_to_transcript(video_id):
    sub = YouTubeTranscriptApi.get_transcript(video_id)
    formatted_subs = JSONFormatter().format_transcript(transcript=sub)
    with open("transcript.json", "w") as outfile:
        json.dump(sub, outfile)
    lstTexts = []
    for dct in sub:
        lstTexts.append(dct['text'])
    strResult = ' '.join(lstTexts)
    with open('SOURCE_DOCUMENTS/transcript.txt', 'w') as outfile:
        outfile.write(strResult)
    transcript = ' '.join(lstTexts)

    utils.calculate_ends('transcript.json','transcript_end.json')
    utils.create_chunks('transcript_end.json','chunks.json')

    return transcript

def start_training():
    training_status = ingest.main()
    return training_status

def replace_substring_and_following(input_string, substring):
    index = input_string.find(substring)
    if index != -1:
        return input_string[:index]
    else:
        return input_string

def ask_question(strQuestion):
    answer = run_localGPT.main(device_type='cpu', strQuery=strQuestion)
    answer_cleaned = replace_substring_and_following(answer, "Unhelpful Answer")
    return answer_cleaned

def summarize():

    from langchain.text_splitter import CharacterTextSplitter
    from langchain.chains.mapreduce import MapReduceChain
    from langchain.prompts import PromptTemplate

    model_id = "TheBloke/Llama-2-7B-Chat-GGML"
    model_basename = "llama-2-7b-chat.ggmlv3.q4_0.bin"

    llm = run_localGPT.load_model(device_type='cpu', model_id=model_id, model_basename=model_basename)

    text_splitter = CharacterTextSplitter()

    with open("SOURCE_DOCUMENTS/transcript.txt") as f:
        file_content = f.read()
    texts = text_splitter.split_text(file_content)

    from langchain.docstore.document import Document

    docs = [Document(page_content=t) for t in texts]

    from langchain.chains.summarize import load_summarize_chain

    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)
    return summary

