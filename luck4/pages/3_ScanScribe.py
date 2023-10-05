import json
import requests
import streamlit as st
import time
import elasticsearch
from langchain import OpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
# from download_file import list_shared_urls_in_bucket, generate_presigned_url
from streamlit.components.v1 import html



####### ------- streamlit ------- ########
##hide
cloud_id = st.secrets["ELASTIC_CLOUD_ID"]
username =  st.secrets["ELASTIC_USER_NAME"]
password = st.secrets["ELASTIC_PASSWORD"]
endpointurl=  st.secrets["LAMBDA_ENDPOINT_URL_3"]
openai_api_key = st.secrets["openapi_key"]

## 


# 버튼을 클릭했을 때 파일 다운로드를 수행하는 함수
# def download_file_from_url(url, file_name):
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(file_name, "wb") as f:
#             f.write(response.content)
#         st.success(f"파일이 다운로드되었습니다: {file_name}")
#     else:
#         st.error("파일 다운로드에 실패했습니다.")



st.title("💨 Search For IR DECK")
st.info("'ScanScribe' is a project that aims to revolutionize the way of managing documents and data . This project integrates OCR technology, creating an all-in-one solution for efficient document handling. We have efficiently improved the time to “search” and understand IR materials.", icon="📃")

with st.expander("EXAMPLES that you can try"):
    st.write("'Summarizing IR' & '10 Taggings for IR'[copy and paste] >> 광진기업")
    st.write("'Search Startups with Keywords' [copy and paste] >> 식품")

# st.info("EXMAPLES that you can try for 'Summarizing IR'&'10 Taggings for IR'[copy and paste] >> 광진기업", icon="🔗")
# st.info("The 'Investment Firm Search Engine' service is an online tool that leverages the latest investment firm information to help investors quickly and efficiently find the investment firms they are looking for. This service provides various keyword and filter options to search for and compare investment firms. Here are the key features of this service:", icon="📃")
# st.info("EXAMPLES that you can try : 한국투자액셀러레이터 / 카카오벤처스 / 윤민창의투자재단 / Becky / Aaron / AI / ML ", icon="🔗")

classification = st.selectbox(
    'What Do You Want To Know',
    ('Summarizing IR', '10 Taggings for IR', 'Search Startups with Keywords')
)
# text button

if classification != "Search Startups with Keywords":
    startup = st.text_input(label="Which Startup do you want to know", value="")
else:
    startup = st.text_input(label="Which Keyword do you want to search with", value="")





if st.button("Search"):
    
    # if classification == "Download IR Deck":
    #     shared_url = list_shared_urls_in_bucket('luck4-ir-bucket', startup)
    #     # print("shared_url")
    #     print(shared_url)
    #     st.markdown(
    #         f'<a href="{shared_url}" download="downloaded_file.zip"><button style="background-color:White;">Download</button></a>',
    #         unsafe_allow_html=True,
    #     )
    
    if classification =="Summarizing IR":
        headers ={
            "Content-Type": "application/json; charset=utf-8"
            
        }
        
        body = {
          "keyword": f"{startup}",
          # "scope": f"{str(nation)}",
          "classification":f"{classification}"
        }
        print(startup)
        print(classification)
        # params = {"keyword": f"{str(input_user_name)}"}
        response = requests.get(endpointurl, headers=headers, json=body)
        keywordlist = json.loads(response.text)
        
        print(f"summarize{keywordlist}")
        
        ### 요약하는 함수 호출 ### 
        
        direct_texts = ""
        
        for key in keywordlist:
            direct_texts += key
            direct_texts += " "
        
        #### ----------- 지피티 요약 기능--------- ####   
        summary =""
        llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
        # Split text
        # keywords 리스트를 하나의 문자열로 변환
        keywords_text = " ".join(direct_texts)
        
        text_splitter = CharacterTextSplitter()
        texts = text_splitter.split_text(keywords_text)
        
        # Create multiple documents
        docs = [Document(page_content=t) for t in texts]
        # Text summarization
        chain = load_summarize_chain(llm, chain_type='map_reduce')
        # result=chain.run(docs)
        
        summary = chain.run(docs)
        
        
        print(summary)
        
        st.subheader("Summary of this Startup IR")
        st.write(summary)
      
      
      
        

    
    else:
  
      headers ={
            "Content-Type": "application/json; charset=utf-8"
            
      }
    
      body = {
          "keyword": f"{startup}",
          # "scope": f"{str(nation)}",
          "classification":f"{classification}"
      }
    
    
      print(startup)
      print(classification)
      # params = {"keyword": f"{str(input_user_name)}"}
      response = requests.get(endpointurl, headers=headers, json=body)
      result = json.loads(response.text)
      
      
      print(result)
      
      ###----- TAGGING -----###
    
      st.subheader(f"10 Tagging for {startup}")
        
    
      for i in result:
        st.write(f"💡 {i}")
  
