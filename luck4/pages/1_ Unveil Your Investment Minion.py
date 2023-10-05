import json
import requests
import streamlit as st
import time
from elasticsearch import Elasticsearch
from PIL import Image
import time

##hide
cloud_id = st.secrets["ELASTIC_CLOUD_ID"]
username =  st.secrets["ELASTIC_USER_NAME"]
password = st.secrets["ELASTIC_PASSWORD"]
endpointurl=  st.secrets["LAMBDA_ENDPOINT_URL_1"]
## 

st.title("📒 FIND Investor Tendency & MINIONS")
st.info("Decode your investment preferences into 4-letter codes derived from the latest investment data and visualize them with adorable Minion characters! Discover your investment personality effortlessly through our service and tailor your investment strategies accordingly. \n Let our Minion characters playfully illustrate your investment style.", icon="📃")
st.info("EXAMPLES that you can try : 한국투자액셀러레이터 / 카카오벤처스 / 윤민창의투자재단 / 킹고투자파트너스 / 우신벤처투자 / 우리은행 / 신한캐피탈 ", icon="🔗")



input_user_name = st.text_input(label="INVESTOR NAME", value="")

if st.button("What TENDENCY & Minions they have?") or input_user_name:
  
  headers ={
        "Content-Type": "application/json; charset=utf-8"
        
  }

  body = {
      "keyword": f"{input_user_name}"
      # "scope": f"{str(nation)}",
      # "classificaion":f"{str(classificaion)}"
  }


  #   res = requests.get(url="https://ul5vohj1z8.execute-api.ap-northeast-2.amazonaws.com/default/luck4_search_engine", headers=headers, json=body)
   
  print(input_user_name)
  # params = {"keyword": f"{str(input_user_name)}"}
  response = requests.get(endpointurl, headers=headers, json=body)

  result = json.loads(response.text)
  
  mbti = result['result_mbti']
  mbti_1_percent_exp = result["mbti_1_percent_exp"]
  mbti_2_percent_exp = result["mbti_2_percent_exp"]
  mbti_3_percent_exp = result["mbti_3_percent_exp"]
  mbti_4_percent_exp = result["mbti_4_percent_exp"]

  
  
  # mbti = "ENFJ"
  
  
  print("response.text:", response.text)
  print("mbti", mbti)
  
  
  if response.text != '{"error": "list index out of range"}':
  
    st.subheader(f"🍌 THE TENDENCY CODE IS … '{mbti}'")
    # 게이지 바의 개수
    num_bars = 4
    
    # 게이지 바와 프로그레스 텍스트를 담을 리스트 생성
    progress_bars = [st.empty() for _ in range(num_bars)]
    progress_text = ["Minimal / Substantial / Considerable / Huge / Excessive","Nuturing / Slight","Twice / Fleeting","Judicious / Peril"]
    progress_percent_complete=[mbti_1_percent_exp,mbti_2_percent_exp,mbti_3_percent_exp,mbti_4_percent_exp]
    
    for i in range(num_bars):
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bars[i].progress( percent_complete + 1, text=f"{progress_text[i]}")
            if percent_complete == int(progress_percent_complete[i]):
                break


  
  if mbti =="MNTJ":
    
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/tim.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### M(Minimal)")
      st.write("This investment firm primarily invests in seed-stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … TIM")
    st.write("TIM is a strategic and careful player in the startup investment landscape. They prefer to tread lightly but with purpose, supporting promising seed-stage startups and nurturing them for success while maintaining a judicious and stable approach to their investment portfolio.")

  elif mbti == "MNTP":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/steve.png')
      st.image(image, width=250)
    
    with col2:
      st.markdown("##### M(Minimal)")
      st.write("M(Minimal) : This investment firm primarily invests in seed-stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("N(Nurturing) : The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("T(Twice) :  This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("P(Peril) : This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … STEVE")
    st.write("STEVE embodies the traits of forming long-lasting friendships, being generous, helping others, and taking on a leadership role among his friends. Steve enjoys nurturing deep and enduring relationships with his fellow Minions, often showing generosity by sharing resources and assistance when needed. He naturally takes on the role of a leader within the Minion group, guiding and supporting his friends on their adventures.")

    

  elif mbti == "MNFJ":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/bob.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### M(Minimal)")
      st.write("This investment firm primarily invests in seed-stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … BOB")
    st.write("BOB is a strategic and careful player in the startup investment landscape. They prefer to tread lightly but with purpose, supporting promising seed-stage startups and nurturing them for success while maintaining a judicious and stable approach to their investment portfolio.")



  elif mbti == "MNFP":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/jerry.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### M(Minimal)")
      st.write("M(Minimal) : This investment firm primarily invests in seed-stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … JERRY")
    st.write("JERRY is a pioneering and influential player in the investment landscape. Their primary focus on seed-stage companies, nurturing investment trend, and preference for one-time investments demonstrate their commitment to early-stage innovation. They actively contribute to the success of their portfolio companies while maintaining an aggressive and strategic approach to their investment portfolio, making them pioneers of innovation in the world of venture capital.")

  elif mbti == "MSTJ":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/phil.png')
      st.image(image, width=350)
    
    with col2:
      st.markdown("##### M(Minimal)")
      st.write("This investment firm primarily invests in seed-stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … Phil")
    st.write("PHIL possesses a personality that cares for those around him, adding a layer of warmth and charm to his character. He tends to make stable and considerate choices while valuing long-lasting friendships and relationships. (")


  elif mbti == "MSTP":
  
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/stuart.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### M(Minimal)")
      st.write("This investment firm primarily invests in seed-stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … STAURT")
    st.write("STAURT is an aggressive seed-stage investment firm with a strong focus on early-stage startups (P). They exhibit a slightly above-average recent investment trend and have a tendency to invest multiple times in the same startup, emphasizing their commitment to nurturing and supporting the growth of these companies.")


  elif mbti == "MSFJ":
  
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/nobert.png')
      st.image(image, width=250)
    
    with col2:
      st.markdown("##### M(Minimal)")
      st.markdown("This investment firm primarily invests in seed-stage companies.", unsafe_allow_html=True)
      st.markdown("##### S(Slight)")
      st.markdown("The recent investment trend of this investment firm is above the average trend.", unsafe_allow_html=True)
      st.markdown("##### F(Fleeting)")
      st.markdown("This investment firm tends to make one-time investments in startups.", unsafe_allow_html=True)
      st.markdown("##### J(Judicious)")
      st.markdown("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.", unsafe_allow_html=True)
    st.subheader("🍌 MATCHING MINION CHARACTER IS … NOBERT")
    st.write("Norbert is an investment firm with a seed-stage focus, specializing in early-stage startup investments. They provide essential funding and support to help startups take off, emphasizing the nurturing of young companies. Their strategy involves taking calculated risks on innovative startups, prioritizing long-term potential over short-term trends. Norbert's portfolio is likely to be diverse, consisting of startups with substantial long-term growth potential.")

    
  elif mbti == "MSFP":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/mel.png')
      st.image(image, width=250)
    
    with col2:
      st.markdown("##### M(Minimal)")
      st.write("This investment firm primarily invests in seed-stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … MEL")
    st.write("MEL This individual possesses a bold personality, finding enjoyment in their pursuits and making decisions with ease. They follow their instincts and often take an aggressive approach towards their goals. This person relishes new challenges and is willing to take on high risks in pursuit of substantial rewards. ")

    
    
    
    
  elif mbti == "SNTJ":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/tim.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### S(Substantial)")
      st.write("This investment firm primarily invests in pre-stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … TIM")
    st.write("TIM is a strategic and careful player in the startup investment landscape. They prefer to tread lightly but with purpose, supporting promising seed-stage startups and nurturing them for success while maintaining a judicious and stable approach to their investment portfolio.")


  elif mbti == "SNTP":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/steve.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### S(Substantial)")  
      st.write("This investment firm primarily invests in pre-stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … STEVE")
    st.write("STEVE embodies the traits of forming long-lasting friendships, being generous, helping others, and taking on a leadership role among his friends. Steve enjoys nurturing deep and enduring relationships with his fellow Minions, often showing generosity by sharing resources and assistance when needed. He naturally takes on the role of a leader within the Minion group, guiding and supporting his friends on their adventures.")


  elif mbti == "SNFJ":
    
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/bob.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### S(Substantial)")  
      st.write("This investment firm primarily invests in pre-stage companies.")
      st.markdown("##### N(Nurturing)")  
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")  
      st.write("This investment firm tends to make one-time investments in startups.")
      st.markdown("##### J(Judicious)")  
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … BOB")
    st.write("BOB is a distinctive and patient player in the investment landscape. Their specialization in pre-stage companies, commitment to nurturing startups below market trends, and preference for one-time investments demonstrate their unique approach to fostering innovation. While they embrace the early stages of startups, they do so with a judicious and stable perspective, contributing to the long-term success of their portfolio companies.")

    
  elif mbti == "SNFP":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/jerry.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### S(Substantial)")  
      st.write("This investment firm primarily invests in pre-stage companies.")
      st.markdown("##### N(Nurturing)")  
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")  
      st.write("This investment firm tends to make one-time investments in startups.")
      st.markdown("##### P(Peril)")  
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … JERRY")
    st.write("JERRY is a pioneering and influential player in the investment landscape. Their primary focus on pre-stage companies, nurturing investment trend, and preference for one-time investments demonstrate their commitment to early-stage innovation. They actively contribute to the success of their portfolio companies while maintaining an aggressive and strategic approach to their investment portfolio, making them enablers of entrepreneurial potential in the world of venture capital.")

  elif mbti == "SSTJ":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/phil.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### S(Substantial)")  
      st.write("This investment firm primarily invests in pre-stage companies.")
      st.markdown("##### S(Slight)")  
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")  
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")  
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … PHIL")
    st.write("PHIL possesses a personality that cares for those around him, adding a layer of warmth and charm to his character. He tends to make stable and considerate choices while valuing long-lasting friendships and relationships. (")



  elif mbti == "SSTP":
   
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/stuart.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### S(Substantial)")  
      st.write("This investment firm primarily invests in pre-stage companies.")
      st.markdown("##### S(Slight)")  
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")  
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")  
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … STAURT")
    st.write("STAURT is an aggressive seed-stage investment firm with a strong focus on early-stage startups (P). They exhibit a slightly above-average recent investment trend and have a tendency to invest multiple times in the same startup, emphasizing their commitment to nurturing and supporting the growth of these companies.")


  elif mbti == "SSFJ":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/nobert.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### S(Substantial)")  
      st.write("This investment firm primarily invests in pre-stage companies.")
      st.markdown("##### S(Slight)")  
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")  
      st.write("This investment firm tends to make one-time investments in startups.")
      st.markdown("##### J(Judicious)")  
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … Nobert")
    st.write("Minions is an investment firm that specializes in seed-stage investments, primarily targeting early-stage startups. They offer vital funding and support to help these startups establish themselves. Minions' investment approach is marked by a commitment to nurturing the growth of these young companies and taking calculated risks on innovative startups. They prioritize long-term potential over short-term trends and typically maintain a diverse portfolio of startups with substantial growth prospects.")

    
  elif mbti == "SSFP":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/mel.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### S(Substantial)")
      st.write("This investment firm primarily invests in pre-stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … MEL")
    st.write("MEL possesses a bold personality, finding enjoyment in their pursuits and making decisions with ease. They follow their instincts and often take an aggressive approach towards their goals. This person relishes new challenges and is willing to take on high risks in pursuit of substantial rewards. ")

    
  
  
  
  
  
  
  elif mbti == "CNTJ":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/frank.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### C(Considerable)")
      st.write("This investment firm primarily invests in series A to series C stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … FRANK")
    st.write("FRANK is a thoughtful and influential player in the investment landscape. Their primary focus on series A to series C stage companies, nurturing investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them stewards of sustainable growth in the world of venture capital.")
  elif mbti == "CNTP":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/john.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### C(Considerable)")
      st.write("This investment firm primarily invests in series A to series C stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … JOHN")
    st.write("JOHN  is a strategic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, nurturing investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining an aggressive and strategic approach to their investment portfolio, making them catalysts of growth in the world of venture capital.")

  elif mbti == "CNFJ":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/lance.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### C(Considerable)")
      st.write("This investment firm primarily invests in series A to series C stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")   
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … LANCE")
    st.write("LANCE is a compassionate and influential player in the investment landscape. Their excessive support, nurturing investment trend, and preference for one-time investments demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them sustained supporters of the entrepreneurial ecosystem.")
    
  elif mbti == "CNFP":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/darwin.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### C(Considerable)")
      st.write("This investment firm primarily invests in series A to series C stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")   
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … DARWIN")
    st.write("DARWIN is a strategic player in the investment landscape. Their primary focus on series A to series C stage companies, nurturing investment trend, and preference for one-time investments demonstrate their commitment to long-term growth and innovation. They are not afraid to take calculated risks and actively contribute to the success of their portfolio companies, positioning themselves as early innovators in the world of venture capital.")
  elif mbti == "CSTJ":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/kevin.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### C(Considerable)")
      st.write("This investment firm primarily invests in series A to series C stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … KEVIN")
    st.write("KEVIN is a dynamic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, above-average investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to strategic growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them valuable growth partners in the world of venture capital.")

  elif mbti == "CSTP":

    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/carl.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### C(Considerable)")
      st.write("This investment firm primarily invests in series A to series C stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … CARL")
    st.write("CARL is a dynamic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, above-average investment trends, and willingness to invest in startups multiple times position them as catalysts for growth in the startups they support. They are not afraid to take calculated risks and actively contribute to the success of their portfolio companies.")

  elif mbti == "CSFJ":

    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/dave.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### C(Considerable)")
      st.write("This investment firm primarily invests in series A to series C stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … DAVE")
    st.write("DAVE is a dynamic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, above-average investment trend, and preference for one-time investments demonstrate their commitment to strategic growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio.")


  elif mbti == "CSFP":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/ken.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### C(Considerable)")
      st.write("This investment firm primarily invests in series A to series C stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")   
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")

    st.subheader("🍌 MATCHING MINION CHARACTER IS … KEN")
    st.write("KEN iis a dynamic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, above-average investment trend, and preference for one-time investments demonstrate their commitment to strategic growth and innovation. They actively contribute to the success of their portfolio companies while maintaining an aggressive and strategic approach to their investment portfolio, making them pioneers of innovation in the world of venture capital.")






  elif mbti == "HNTJ":

    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/frank.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### H(Huge)")
      st.write("This investment firm primarily invests in series D to series G stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")

    st.subheader("🍌 MATCHING MINION CHARACTER IS … FRANK")
    st.wtire("FRANK s a strategic and influential player in the investment landscape. Their primary focus on series D to series G stage companies, nurturing investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them sustainers of sustainable growth in the world of venture capital.")

  elif mbti == "HNTP":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/john.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### H(Huge)")
      st.write("This investment firm primarily invests in series D to series G stage companies..")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … JOHN")
    st.write("JOHN is a strategic and influential player in the investment landscape. Their primary focus on series D to series G stage companies, nurturing investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining an aggressive and strategic approach to their investment portfolio, making them titans of growth in the world of venture capital.")

  elif mbti == "HNFJ":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/lance.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### H(Huge)")
      st.write("This investment firm primarily invests in series D to series G stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … LANCE")
    st.write("LANCE is a compassionate and influential player in the investment landscape. Their excessive support, nurturing investment trend, and preference for one-time investments demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them sustained supporters of the entrepreneurial ecosystem.")
    
  elif mbti == "HNFP":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/darwin.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### H(Huge)")
      st.write("This investment firm primarily invests in series D to series G stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … DARWIN")
    st.write("DARWIN is a forward-thinking player in the investment landscape. Their primary focus on series D to series G stage companies, nurturing investment trend, and preference for one-time investments demonstrate their commitment to long-term growth and innovation. They are not afraid to take calculated risks and actively contribute to the success of their portfolio companies, positioning themselves as vanguards of growth in the world of venture capital.")


  elif mbti == "HSTJ":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/kevin.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### H(Huge)")
      st.write("This investment firm primarily invests in series D to series G stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … KEVIN")
    st.write("KEVIN is a dynamic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, above-average investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to strategic growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them valuable growth partners in the world of venture capital.")

  elif mbti == "HSTP":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/carl.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### H(Huge)")
      st.write("This investment firm primarily invests in series D to series G stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … CARL")
    st.write("CARL is a powerhouse in the investment landscape, known for their focus on series D to series G stage companies, consistently above-average investment trends, and their unique commitment to investing in startups multiple times. They thrive on taking calculated risks and actively contributing to the growth and success of their portfolio companies, setting them apart as maestros of growth in the world of venture capital.")
    

  elif mbti == "HSFJ":

    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/dave.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### H(Huge)")
      st.write("This investment firm primarily invests in series D to series G stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … DAVE")
    st.write("DAVE is a dynamic and influential player in the investment landscape. Their primary focus on series D to series G stage companies, above-average investment trend, and preference for one-time investments demonstrate their commitment to strategic growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio.")



  elif mbti == "HSFP":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/ken.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### H(Huge)")
      st.write("This investment firm primarily invests in series D to series G stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")

    st.subheader("🍌 MATCHING MINION CHARACTER IS … KEN")
    st.write("KEN is a dynamic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, above-average investment trend, and preference for one-time investments demonstrate their commitment to strategic growth and innovation. They actively contribute to the success of their portfolio companies while maintaining an aggressive and strategic approach to their investment portfolio, making them pioneers of innovation in the world of venture capital.")

    
    
    
    
    
    
  elif mbti == "ENTJ":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/frank.png')
      st.image(image, width=250)
    
    with col2:
      st.markdown("##### E(Excessive)")
      st.write("These investment firms frequently provide grants and support in their investments.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … FRANK")
    st.write("FRANK is a compassionate and influential player in the investment landscape. Their excessive support, nurturing investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them sustained benefactors of the entrepreneurial ecosystem.")
   


  elif mbti == "ENTP":
    
    col1, col2 = st.columns(2)
    
    
    with col1:
      image = Image.open('minion_img/john.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### E(Excessive)")
      st.write("These investment firms frequently provide grants and support in their investments.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice))")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … JOHN")
    st.write("is a compassionate and influential player in the investment landscape. Their excessive support, nurturing investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining an aggressive and strategic approach to their investment portfolio, making them innovators in both investment and philanthropy.")
    
    
  elif mbti == "ENFJ":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/lance.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### E(Excessive)")
      st.write("These investment firms frequently provide grants and support in their investments.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … LANCE")
    st.write("LANCE is a compassionate and influential player in the investment landscape. Their excessive support, nurturing investment trend, and preference for one-time investments demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them sustained supporters of the entrepreneurial ecosystem.")
    
  elif mbti == "ENFP":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/darwin.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### E(Excessive)")
      st.write("These investment firms frequently provide grants and support in their investments.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … DARWIN")
    st.write("DARWIN is a unique and compassionate player in the investment landscape. Their excessive support, nurturing investment trend, and preference for one-time investments demonstrate their commitment to the long-term success of the startups they back. While they embrace the early stages of startups, they do so with a calculated and benevolent approach, contributing to the innovation ecosystem with both financial and mentoring support.")

  elif mbti == "ESTJ":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/kevin.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### E(Excessive)")
      st.write("These investment firms frequently provide grants and support in their investments.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … KEVIN")
    st.write("KEVIN is a dynamic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, above-average investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to strategic growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them valuable growth partners in the world of venture capital.")

  elif mbti == "ESTP":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/carl.png')
      st.image(image, width=250)
    
    with col2:
      st.markdown("##### E(Excessive)")
      st.write("These investment firms frequently provide grants and support in their investments.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … CARL")
    st.write("CARL is a trailblazer in the investment landscape, known for their excessive support, above-average investment trends, and their unique commitment to investing in startups multiple times. They are generous not only with capital but also with their time and resources, actively nurturing the startups they back and contributing to their long-term success.")

  elif mbti == "ESFJ":
    
    col1, col2 = st.columns(2)


    with col1:
      image = Image.open('minion_img/dave.png')
      st.image(image, width=250)
    
    with col2:
      st.markdown("##### E(Excessive)")
      st.write("These investment firms frequently provide grants and support in their investments.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … DAVE")
    st.write("DAVE is a dynamic and influential player in the investment landscape. Their excessive support, above-average investment trend, and preference for one-time investments demonstrate their commitment to nurturing innovation and philanthropy. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them innovators in both investment and philanthropy.")


  elif mbti == "ESFP":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/ken.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### E(Excessive)")
      st.write("These investment firms frequently provide grants and support in their investments.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … KEN")
    st.write("KEN iis a dynamic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, above-average investment trend, and preference for one-time investments demonstrate their commitment to strategic growth and innovation. They actively contribute to the success of their portfolio companies while maintaining an aggressive and strategic approach to their investment portfolio, making them pioneers of innovation in the world of venture capital.")

      
else:
  st.write('No result found')
  

















st.title("📒 SEARCH Investor Tendency")
st.info("Description", icon="📃")
st.info("Description2", icon="🔗")
styled_text = """
<div style="background-color: rgba(247, 204, 111, 0.5); padding: 10px; border-radius: 5px;">
    <p style="color: black;">이것은 투명한 노란색 배경으로 변경된 정보입니다.</p>
</div>
"""
# st.markdown()을 사용하여 스타일이 적용된 텍스트 출력
st.markdown(styled_text, unsafe_allow_html=True)

input_user_name = st.text_input(label="Name", value="")

if st.button("What minion are you") or input_user_name:
  
  headers ={
        "Content-Type": "application/json; charset=utf-8"
        
  }

  body = {
      "keyword": f"{input_user_name}"
      # "scope": f"{str(nation)}",
      # "classificaion":f"{str(classificaion)}"
  }


  #   res = requests.get(url="https://ul5vohj1z8.execute-api.ap-northeast-2.amazonaws.com/default/luck4_search_engine", headers=headers, json=body)
   
  print(input_user_name)
  # params = {"keyword": f"{str(input_user_name)}"}
  response = requests.get(endpointurl, headers=headers, json=body)

  result = json.loads(response.text)
  
  mbti = result['result_mbti']
  mbti_1_percent_exp = result["mbti_1_percent_exp"]
  mbti_2_percent_exp = result["mbti_2_percent_exp"]
  mbti_3_percent_exp = result["mbti_3_percent_exp"]
  mbti_4_percent_exp = result["mbti_4_percent_exp"]

  
  
  # mbti = "ENFJ"
  
  
  print("response.text:", response.text)
  print("mbti", mbti)
  
  
  if response.text != '{"error": "list index out of range"}':
  
    st.subheader(f"🍌 THE TENDENCY CODE IS … '{mbti}'")
    # 게이지 바의 개수
    num_bars = 4
    
    # 게이지 바와 프로그레스 텍스트를 담을 리스트 생성
    progress_bars = [st.empty() for _ in range(num_bars)]
    progress_text = ["Minimal / Substantial / Considerable / Huge / Excessive","Nuturing / Slight","Twice / Fleeting","Judicious / Peril"]
    progress_percent_complete=[mbti_1_percent_exp,mbti_2_percent_exp,mbti_3_percent_exp,mbti_4_percent_exp]
    
    for i in range(num_bars):
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bars[i].progress( percent_complete + 1, text=f"{progress_text[i]}")
            if percent_complete == int(progress_percent_complete[i]):
                break


  
  if mbti =="MNTJ":
    
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/tim.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### M(Minimal)")
      st.write("This investment firm primarily invests in seed-stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … TIM")
    st.write("TIM is a strategic and careful player in the startup investment landscape. They prefer to tread lightly but with purpose, supporting promising seed-stage startups and nurturing them for success while maintaining a judicious and stable approach to their investment portfolio.")

  elif mbti == "MNTP":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/steve.png')
      st.image(image, width=250)
    
    with col2:
      st.markdown("##### M(Minimal)")
      st.write("M(Minimal) : This investment firm primarily invests in seed-stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("N(Nurturing) : The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("T(Twice) :  This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("P(Peril) : This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … STEVE")
    st.write("STEVE embodies the traits of forming long-lasting friendships, being generous, helping others, and taking on a leadership role among his friends. Steve enjoys nurturing deep and enduring relationships with his fellow Minions, often showing generosity by sharing resources and assistance when needed. He naturally takes on the role of a leader within the Minion group, guiding and supporting his friends on their adventures.")

    

  elif mbti == "MNFJ":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/bob.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### M(Minimal)")
      st.write("This investment firm primarily invests in seed-stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … BOB")
    st.write("BOB is a strategic and careful player in the startup investment landscape. They prefer to tread lightly but with purpose, supporting promising seed-stage startups and nurturing them for success while maintaining a judicious and stable approach to their investment portfolio.")



  elif mbti == "MNFP":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/jerry.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### M(Minimal)")
      st.write("M(Minimal) : This investment firm primarily invests in seed-stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … JERRY")
    st.write("JERRY is a pioneering and influential player in the investment landscape. Their primary focus on seed-stage companies, nurturing investment trend, and preference for one-time investments demonstrate their commitment to early-stage innovation. They actively contribute to the success of their portfolio companies while maintaining an aggressive and strategic approach to their investment portfolio, making them pioneers of innovation in the world of venture capital.")

  elif mbti == "MSTJ":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/phil.png')
      st.image(image, width=350)
    
    with col2:
      st.markdown("##### M(Minimal)")
      st.write("This investment firm primarily invests in seed-stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … Phil")
    st.write("PHIL possesses a personality that cares for those around him, adding a layer of warmth and charm to his character. He tends to make stable and considerate choices while valuing long-lasting friendships and relationships. (")


  elif mbti == "MSTP":
  
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/stuart.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### M(Minimal)")
      st.write("This investment firm primarily invests in seed-stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … STAURT")
    st.write("STAURT is an aggressive seed-stage investment firm with a strong focus on early-stage startups (P). They exhibit a slightly above-average recent investment trend and have a tendency to invest multiple times in the same startup, emphasizing their commitment to nurturing and supporting the growth of these companies.")


  elif mbti == "MSFJ":
  
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/nobert.png')
      st.image(image, width=250)
    
    with col2:
      st.markdown("##### M(Minimal)")
      st.markdown("This investment firm primarily invests in seed-stage companies.", unsafe_allow_html=True)
      st.markdown("##### S(Slight)")
      st.markdown("The recent investment trend of this investment firm is above the average trend.", unsafe_allow_html=True)
      st.markdown("##### F(Fleeting)")
      st.markdown("This investment firm tends to make one-time investments in startups.", unsafe_allow_html=True)
      st.markdown("##### J(Judicious)")
      st.markdown("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.", unsafe_allow_html=True)
    st.subheader("🍌 MATCHING MINION CHARACTER IS … NOBERT")
    st.write("Norbert is an investment firm with a seed-stage focus, specializing in early-stage startup investments. They provide essential funding and support to help startups take off, emphasizing the nurturing of young companies. Their strategy involves taking calculated risks on innovative startups, prioritizing long-term potential over short-term trends. Norbert's portfolio is likely to be diverse, consisting of startups with substantial long-term growth potential.")

    
  elif mbti == "MSFP":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/mel.png')
      st.image(image, width=250)
    
    with col2:
      st.markdown("##### M(Minimal)")
      st.write("This investment firm primarily invests in seed-stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … MEL")
    st.write("MEL This individual possesses a bold personality, finding enjoyment in their pursuits and making decisions with ease. They follow their instincts and often take an aggressive approach towards their goals. This person relishes new challenges and is willing to take on high risks in pursuit of substantial rewards. ")

    
    
    
    
  elif mbti == "SNTJ":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/tim.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### S(Substantial)")
      st.write("This investment firm primarily invests in pre-stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … TIM")
    st.write("TIM is a strategic and careful player in the startup investment landscape. They prefer to tread lightly but with purpose, supporting promising seed-stage startups and nurturing them for success while maintaining a judicious and stable approach to their investment portfolio.")


  elif mbti == "SNTP":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/steve.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### S(Substantial)")  
      st.write("This investment firm primarily invests in pre-stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … STEVE")
    st.write("STEVE embodies the traits of forming long-lasting friendships, being generous, helping others, and taking on a leadership role among his friends. Steve enjoys nurturing deep and enduring relationships with his fellow Minions, often showing generosity by sharing resources and assistance when needed. He naturally takes on the role of a leader within the Minion group, guiding and supporting his friends on their adventures.")


  elif mbti == "SNFJ":
    
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/bob.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### S(Substantial)")  
      st.write("This investment firm primarily invests in pre-stage companies.")
      st.markdown("##### N(Nurturing)")  
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")  
      st.write("This investment firm tends to make one-time investments in startups.")
      st.markdown("##### J(Judicious)")  
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … BOB")
    st.write("BOB is a distinctive and patient player in the investment landscape. Their specialization in pre-stage companies, commitment to nurturing startups below market trends, and preference for one-time investments demonstrate their unique approach to fostering innovation. While they embrace the early stages of startups, they do so with a judicious and stable perspective, contributing to the long-term success of their portfolio companies.")

    
  elif mbti == "SNFP":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/jerry.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### S(Substantial)")  
      st.write("This investment firm primarily invests in pre-stage companies.")
      st.markdown("##### N(Nurturing)")  
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")  
      st.write("This investment firm tends to make one-time investments in startups.")
      st.markdown("##### P(Peril)")  
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … JERRY")
    st.write("JERRY is a pioneering and influential player in the investment landscape. Their primary focus on pre-stage companies, nurturing investment trend, and preference for one-time investments demonstrate their commitment to early-stage innovation. They actively contribute to the success of their portfolio companies while maintaining an aggressive and strategic approach to their investment portfolio, making them enablers of entrepreneurial potential in the world of venture capital.")

  elif mbti == "SSTJ":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/phil.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### S(Substantial)")  
      st.write("This investment firm primarily invests in pre-stage companies.")
      st.markdown("##### S(Slight)")  
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")  
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")  
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … PHIL")
    st.write("PHIL possesses a personality that cares for those around him, adding a layer of warmth and charm to his character. He tends to make stable and considerate choices while valuing long-lasting friendships and relationships. (")



  elif mbti == "SSTP":
   
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/stuart.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### S(Substantial)")  
      st.write("This investment firm primarily invests in pre-stage companies.")
      st.markdown("##### S(Slight)")  
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")  
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")  
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … STAURT")
    st.write("STAURT is an aggressive seed-stage investment firm with a strong focus on early-stage startups (P). They exhibit a slightly above-average recent investment trend and have a tendency to invest multiple times in the same startup, emphasizing their commitment to nurturing and supporting the growth of these companies.")


  elif mbti == "SSFJ":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/nobert.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### S(Substantial)")  
      st.write("This investment firm primarily invests in pre-stage companies.")
      st.markdown("##### S(Slight)")  
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")  
      st.write("This investment firm tends to make one-time investments in startups.")
      st.markdown("##### J(Judicious)")  
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … Nobert")
    st.write("Minions is an investment firm that specializes in seed-stage investments, primarily targeting early-stage startups. They offer vital funding and support to help these startups establish themselves. Minions' investment approach is marked by a commitment to nurturing the growth of these young companies and taking calculated risks on innovative startups. They prioritize long-term potential over short-term trends and typically maintain a diverse portfolio of startups with substantial growth prospects.")

    
  elif mbti == "SSFP":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/mel.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### S(Substantial)")
      st.write("This investment firm primarily invests in pre-stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … MEL")
    st.write("MEL possesses a bold personality, finding enjoyment in their pursuits and making decisions with ease. They follow their instincts and often take an aggressive approach towards their goals. This person relishes new challenges and is willing to take on high risks in pursuit of substantial rewards. ")

    
  
  
  
  
  
  
  elif mbti == "CNTJ":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/frank.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### C(Considerable)")
      st.write("This investment firm primarily invests in series A to series C stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … FRANK")
    st.write("FRANK is a thoughtful and influential player in the investment landscape. Their primary focus on series A to series C stage companies, nurturing investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them stewards of sustainable growth in the world of venture capital.")
  elif mbti == "CNTP":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/john.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### C(Considerable)")
      st.write("This investment firm primarily invests in series A to series C stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … JOHN")
    st.write("JOHN  is a strategic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, nurturing investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining an aggressive and strategic approach to their investment portfolio, making them catalysts of growth in the world of venture capital.")

  elif mbti == "CNFJ":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/lance.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### C(Considerable)")
      st.write("This investment firm primarily invests in series A to series C stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")   
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … LANCE")
    st.write("LANCE is a compassionate and influential player in the investment landscape. Their excessive support, nurturing investment trend, and preference for one-time investments demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them sustained supporters of the entrepreneurial ecosystem.")
    
  elif mbti == "CNFP":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/darwin.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### C(Considerable)")
      st.write("This investment firm primarily invests in series A to series C stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")   
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … DARWIN")
    st.write("DARWIN is a strategic player in the investment landscape. Their primary focus on series A to series C stage companies, nurturing investment trend, and preference for one-time investments demonstrate their commitment to long-term growth and innovation. They are not afraid to take calculated risks and actively contribute to the success of their portfolio companies, positioning themselves as early innovators in the world of venture capital.")
  elif mbti == "CSTJ":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/kevin.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### C(Considerable)")
      st.write("This investment firm primarily invests in series A to series C stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … KEVIN")
    st.write("KEVIN is a dynamic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, above-average investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to strategic growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them valuable growth partners in the world of venture capital.")

  elif mbti == "CSTP":

    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/carl.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### C(Considerable)")
      st.write("This investment firm primarily invests in series A to series C stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … CARL")
    st.write("CARL is a dynamic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, above-average investment trends, and willingness to invest in startups multiple times position them as catalysts for growth in the startups they support. They are not afraid to take calculated risks and actively contribute to the success of their portfolio companies.")

  elif mbti == "CSFJ":

    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/dave.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### C(Considerable)")
      st.write("This investment firm primarily invests in series A to series C stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … DAVE")
    st.write("DAVE is a dynamic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, above-average investment trend, and preference for one-time investments demonstrate their commitment to strategic growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio.")


  elif mbti == "CSFP":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/ken.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### C(Considerable)")
      st.write("This investment firm primarily invests in series A to series C stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")   
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")

    st.subheader("🍌 MATCHING MINION CHARACTER IS … KEN")
    st.write("KEN iis a dynamic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, above-average investment trend, and preference for one-time investments demonstrate their commitment to strategic growth and innovation. They actively contribute to the success of their portfolio companies while maintaining an aggressive and strategic approach to their investment portfolio, making them pioneers of innovation in the world of venture capital.")






  elif mbti == "HNTJ":

    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/frank.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### H(Huge)")
      st.write("This investment firm primarily invests in series D to series G stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")

    st.subheader("🍌 MATCHING MINION CHARACTER IS … FRANK")
    st.wtire("FRANK s a strategic and influential player in the investment landscape. Their primary focus on series D to series G stage companies, nurturing investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them sustainers of sustainable growth in the world of venture capital.")

  elif mbti == "HNTP":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/john.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### H(Huge)")
      st.write("This investment firm primarily invests in series D to series G stage companies..")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … JOHN")
    st.write("JOHN is a strategic and influential player in the investment landscape. Their primary focus on series D to series G stage companies, nurturing investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining an aggressive and strategic approach to their investment portfolio, making them titans of growth in the world of venture capital.")

  elif mbti == "HNFJ":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/lance.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### H(Huge)")
      st.write("This investment firm primarily invests in series D to series G stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … LANCE")
    st.write("LANCE is a compassionate and influential player in the investment landscape. Their excessive support, nurturing investment trend, and preference for one-time investments demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them sustained supporters of the entrepreneurial ecosystem.")
    
  elif mbti == "HNFP":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/darwin.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### H(Huge)")
      st.write("This investment firm primarily invests in series D to series G stage companies.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … DARWIN")
    st.write("DARWIN is a forward-thinking player in the investment landscape. Their primary focus on series D to series G stage companies, nurturing investment trend, and preference for one-time investments demonstrate their commitment to long-term growth and innovation. They are not afraid to take calculated risks and actively contribute to the success of their portfolio companies, positioning themselves as vanguards of growth in the world of venture capital.")


  elif mbti == "HSTJ":
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/kevin.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### H(Huge)")
      st.write("This investment firm primarily invests in series D to series G stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … KEVIN")
    st.write("KEVIN is a dynamic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, above-average investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to strategic growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them valuable growth partners in the world of venture capital.")

  elif mbti == "HSTP":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/carl.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### H(Huge)")
      st.write("This investment firm primarily invests in series D to series G stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … CARL")
    st.write("CARL is a powerhouse in the investment landscape, known for their focus on series D to series G stage companies, consistently above-average investment trends, and their unique commitment to investing in startups multiple times. They thrive on taking calculated risks and actively contributing to the growth and success of their portfolio companies, setting them apart as maestros of growth in the world of venture capital.")
    

  elif mbti == "HSFJ":

    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/dave.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### H(Huge)")
      st.write("This investment firm primarily invests in series D to series G stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … DAVE")
    st.write("DAVE is a dynamic and influential player in the investment landscape. Their primary focus on series D to series G stage companies, above-average investment trend, and preference for one-time investments demonstrate their commitment to strategic growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio.")



  elif mbti == "HSFP":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/ken.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### H(Huge)")
      st.write("This investment firm primarily invests in series D to series G stage companies.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")

    st.subheader("🍌 MATCHING MINION CHARACTER IS … KEN")
    st.write("KEN is a dynamic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, above-average investment trend, and preference for one-time investments demonstrate their commitment to strategic growth and innovation. They actively contribute to the success of their portfolio companies while maintaining an aggressive and strategic approach to their investment portfolio, making them pioneers of innovation in the world of venture capital.")

    
    
    
    
    
    
  elif mbti == "ENTJ":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/frank.png')
      st.image(image, width=250)
    
    with col2:
      st.markdown("##### E(Excessive)")
      st.write("These investment firms frequently provide grants and support in their investments.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … FRANK")
    st.write("FRANK is a compassionate and influential player in the investment landscape. Their excessive support, nurturing investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them sustained benefactors of the entrepreneurial ecosystem.")
   


  elif mbti == "ENTP":
    
    col1, col2 = st.columns(2)
    
    
    with col1:
      image = Image.open('minion_img/john.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### E(Excessive)")
      st.write("These investment firms frequently provide grants and support in their investments.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### T(Twice))")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … JOHN")
    st.write("is a compassionate and influential player in the investment landscape. Their excessive support, nurturing investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining an aggressive and strategic approach to their investment portfolio, making them innovators in both investment and philanthropy.")
    
    
  elif mbti == "ENFJ":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/lance.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### E(Excessive)")
      st.write("These investment firms frequently provide grants and support in their investments.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … LANCE")
    st.write("LANCE is a compassionate and influential player in the investment landscape. Their excessive support, nurturing investment trend, and preference for one-time investments demonstrate their commitment to long-term growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them sustained supporters of the entrepreneurial ecosystem.")
    
  elif mbti == "ENFP":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/darwin.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### E(Excessive)")
      st.write("These investment firms frequently provide grants and support in their investments.")
      st.markdown("##### N(Nurturing)")
      st.write("The recent investment trend of this investment firm is below the average trend")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … DARWIN")
    st.write("DARWIN is a unique and compassionate player in the investment landscape. Their excessive support, nurturing investment trend, and preference for one-time investments demonstrate their commitment to the long-term success of the startups they back. While they embrace the early stages of startups, they do so with a calculated and benevolent approach, contributing to the innovation ecosystem with both financial and mentoring support.")

  elif mbti == "ESTJ":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/kevin.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### E(Excessive)")
      st.write("These investment firms frequently provide grants and support in their investments.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … KEVIN")
    st.write("KEVIN is a dynamic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, above-average investment trend, and preference for investing in the same startup multiple times demonstrate their commitment to strategic growth and innovation. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them valuable growth partners in the world of venture capital.")

  elif mbti == "ESTP":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/carl.png')
      st.image(image, width=250)
    
    with col2:
      st.markdown("##### E(Excessive)")
      st.write("These investment firms frequently provide grants and support in their investments.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### T(Twice)")
      st.write("This investment firm tends to invest in the same startup more than once")
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    
    st.subheader("🍌 MATCHING MINION CHARACTER IS … CARL")
    st.write("CARL is a trailblazer in the investment landscape, known for their excessive support, above-average investment trends, and their unique commitment to investing in startups multiple times. They are generous not only with capital but also with their time and resources, actively nurturing the startups they back and contributing to their long-term success.")

  elif mbti == "ESFJ":
    
    col1, col2 = st.columns(2)


    with col1:
      image = Image.open('minion_img/dave.png')
      st.image(image, width=250)
    
    with col2:
      st.markdown("##### E(Excessive)")
      st.write("These investment firms frequently provide grants and support in their investments.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### J(Judicious)")
      st.write("This investment firm has a relatively stable investment tendency, typically investing in companies with over 3 years of existence and serving as the second or subsequent investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … DAVE")
    st.write("DAVE is a dynamic and influential player in the investment landscape. Their excessive support, above-average investment trend, and preference for one-time investments demonstrate their commitment to nurturing innovation and philanthropy. They actively contribute to the success of their portfolio companies while maintaining a judicious and stable approach to their investment portfolio, making them innovators in both investment and philanthropy.")


  elif mbti == "ESFP":
    
    col1, col2 = st.columns(2)
  
    with col1:
      image = Image.open('minion_img/ken.png')
      st.image(image, width=300)
    
    with col2:
      st.markdown("##### E(Excessive)")
      st.write("These investment firms frequently provide grants and support in their investments.")
      st.markdown("##### S(Slight)")
      st.write("The recent investment trend of this investment firm is above the average trend.")
      st.markdown("##### F(Fleeting)")
      st.write("This investment firm tends to make one-time investments in startups.")      
      st.markdown("##### P(Peril)")
      st.write("This investment firm has a relatively aggressive investment tendency, typically investing in companies with less than 3 years of existence and serving as the first investor.")
    st.subheader("🍌 MATCHING MINION CHARACTER IS … KEN")
    st.write("KEN iis a dynamic and influential player in the investment landscape. Their primary focus on series A to series C stage companies, above-average investment trend, and preference for one-time investments demonstrate their commitment to strategic growth and innovation. They actively contribute to the success of their portfolio companies while maintaining an aggressive and strategic approach to their investment portfolio, making them pioneers of innovation in the world of venture capital.")

      
else:
  st.write('No result found')
  




