import json
import requests
import streamlit as st
import time
import elasticsearch

##hide
cloud_id = st.secrets["ELASTIC_CLOUD_ID"]
username =  st.secrets["ELASTIC_USER_NAME"]
password = st.secrets["ELASTIC_PASSWORD"]
endpointurl=  st.secrets["LAMBDA_ENDPOINT_URL_2"]
## 

####### ------- streamlit ------- ########

st.title("💨 Fast Investor Search️")
st.info("The 'Investment Firm Search Engine' service is an online tool that leverages the latest investment firm information to help investors quickly and efficiently find the investment firms they are looking for. This service provides various keyword and filter options to search for and compare investment firms. Here are the key features of this service:", icon="📃")

with st.expander("EXAMPLES that you can try for"):
    st.write("👉🏻'korea' 'name' >> 한국투자액셀러레이터 , 카카오벤처스 , 윤민창의투자재단, 유한양행")
    st.write("👉🏻'korea' 'category' >> 커머스, 바이오, 콘텐츠/예술, 푸드/농업")
    st.write("👉🏻'korea' 'tags' >> 금융/보험/핀테크, 바이오, seed, 게임")

    st.write("👉🏻'global' 'name' >> Becky, Aaron, B, C")
    st.write("👉🏻'global' 'category' >> AI / ML , Fintech, Industrial, Climate/Sustainability, Crypto/Blockchain")
    st.write("👉🏻'global' 'tags' >> Series A, Series B , Series C")




nation = st.selectbox(
    '위치',
    ('global', 'korea')
)
    
classification = st.selectbox(
    '검색종류',
    ('name', 'category','tags')
)
    
# text button
input_user_name = st.text_input(label="Name", value="")

if input_user_name:
    print(input_user_name)
    print(str(nation))
    
    
    headers ={
        "Content-Type": "application/json; charset=utf-8"
        
    }

    body = {
        "keyword": f"{input_user_name}",
        "scope": f"{str(nation)}",
        "classification":f"{str(classification)}"
    }


    res = requests.get(url="https://ul5vohj1z8.execute-api.ap-northeast-2.amazonaws.com/default/luck4_search_engine", headers=headers, json=body)
    
    print(res)
    result = res.text.encode('utf-8').decode('unicode_escape')
    print(result)
    
    res_dict = json.loads(res.text)
    
    print(res_dict)
    
    ########## 밑에 칼럼 ############

    i = 0
    industries_text =""
    
    if str(nation) == 'global':
        
        num_columns = len(res_dict)
        
        if num_columns:
            columns = st.columns(num_columns)
            
            for col in columns:
                
                name = res_dict[i]['name'].replace('\n', " ")
                # name = res_dict[i]['name']
                
                
                print(name)
                
    
    
    
                st.header(f"{name}")
                
                with st.expander("See more"):
                    st.write(f"📍 Type: {res_dict[i]['type']}")
                    st.write(f"📍 Role: {res_dict[i]['role']}")
                    st.write(f"📍 Bio: {res_dict[i]['bio']}")
                    st.write(f"📍 Stages: {res_dict[i]['stages']}")
                    st.write(f"📍 Geography: {res_dict[i]['geography']}")
                    if 'industries' in res_dict[i]:
                        for industry in res_dict[i]['industries']:
                            # print(industry)
                            industries_text += str(industry) +"/"
                        st.write(f"📍 Industries: {industries_text[:-1]}")
                    if 'checkrange' in res_dict[i]:
                        st.write(f"📍 Checkrange: {res_dict[i]['checkrange']}")   
                    if 'aboutinvest' in res_dict[i]:
                        st.write(f"📍 Aboutinvest: {res_dict[i]['aboutinvest']}")   
                    if 'linkedinlink' in res_dict[i]:
                        st.write(f"🔗 Linkedinlink: {res_dict[i]['linkedinlink']}")   
                    if 'fundlink' in res_dict[i]:
                        st.write(f"🔗 Fundlink: {res_dict[i]['fundlink']}")  
                    if 'email' in res_dict[i]:
                        email = res_dict[i]['email'].replace('\n', " ")
                        st.write(f"🔗 Email: {email}")
    
    
                
                i = i +1 
        
        else:
            st.header("검색결과가 없습니다.")
            
            
    elif str(nation) == 'korea':
        num_columns = len(res_dict)
        
        
        if num_columns:
            
            columns = st.columns(num_columns)
            
            for col in columns:
                name = res_dict[i]['투자사 이름']
                st.header(f"{name}")
            
        
                with st.expander("See more"):
                    st.write(f"📍 투자 기업수: {res_dict[i]['투자 기업수']}")
                    st.write(f"📍 총 투자 횟수: {res_dict[i]['총 투자 횟수']}")
                    st.write(f"📍 선호 투자 관계: {res_dict[i]['선호 투자 단계']}")
                    st.write(f"📍 스타트업이 첫 투자: {res_dict[i]['스타트업이 첫  투자']}")
                    st.write(f"📍 창업 3년미만기업: {res_dict[i]['창업 3년미만기업']}")
                    
                    # res_dict[i]['주요 투자분야']
                    res_arr = json.loads(res_dict[i]['주요 투자분야'].replace("'", '"'))
                    print(res_arr)
                    st.write(f"📍 주요 투자분야:")
    
                    for res in res_arr:
                        category = res['category']
                        count = res['count']
                        st.write("- "+str(category)+":"+ count)
                    
                   
    
                i = i + 1
        else:
            st.header("검색결과가 없습니다.")
