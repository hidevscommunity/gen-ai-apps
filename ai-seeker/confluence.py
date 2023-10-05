from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth
import run_localGPT

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

def transcript(page_id, atlassian_username, atlassian_password):

    url = f"https://srikanthnm.atlassian.net/wiki/rest/api/content/{page_id}?expand=body.storage"  # Replace with the actual URL you want to access
    username = atlassian_username
    password = atlassian_password


    response = requests.get(url, auth=HTTPBasicAuth(username, password))

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Process the response data (if applicable)
        data = response.json()
    else:
        data = f"Error: Unable to access the URL. Status code: {response.status_code}"

    soup = BeautifulSoup(data['body']['storage']['value'],"html.parser")

    page_content = soup.get_text()
    page_content_cleaned = page_content.replace('\xa0',' ')
    page_content_cleaned

    with open('SOURCE_DOCUMENTS/confluence.txt', 'w') as outfile:
        outfile.write(page_content_cleaned[:1998])

    return page_content_cleaned[:1998]

def summarize():
    from langchain import PromptTemplate, LLMChain
    from langchain.text_splitter import CharacterTextSplitter
    from langchain.chains.mapreduce import MapReduceChain
    from langchain.prompts import PromptTemplate

    model_id = "TheBloke/Llama-2-7B-Chat-GGML"
    model_basename = "llama-2-7b-chat.ggmlv3.q4_0.bin"

    llm = run_localGPT.load_model(device_type='cpu', model_id=model_id, model_basename=model_basename)

    text_splitter = CharacterTextSplitter()

    with open("SOURCE_DOCUMENTS/confluence.txt") as f:
        file_content = f.read()
    texts = text_splitter.split_text(file_content)

    from langchain.docstore.document import Document

    docs = [Document(page_content=t) for t in texts]

    from langchain.chains.summarize import load_summarize_chain

    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)

    return summary