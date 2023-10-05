# Import necessary libraries
import streamlit as st
import datetime
from newsapi import NewsApiClient
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Set up the Streamlit app
col1,col2,col3=st.columns(3)
col2.title("LinkCraft")
st.markdown("<h1 style='text-align: center; color: black; font-size: 38px;'>AI-Powered LinkedIn Content Composer</h1>", unsafe_allow_html=True)


st.write(
    """
    Welcome to 🌐 LinkCraft, your premier AI-driven tool for crafting LinkedIn content. Designed for professionals and thought leaders, LinkCraft transforms trending news headlines into insightful LinkedIn posts. 📊 Select an industry, choose a headline, and receive a post tailored for the LinkedIn audience, echoing the styles of industry influencers. Elevate your LinkedIn narrative with precision and flair. 🚀
"""
)
st.write('\n')
st.write('\n')

# Display a styled waiting message using HTML and CSS
waiting_html = """
<div style="
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    background-color: #FFD700;
    color: black;
    font-size: 24px;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
">
    Please wait! Your LinkedIn Post is being generated! 🚀
</div>
"""



# Initialize the NewsAPI client
NEWS_API_KEY = st.secrets["NEWS_API"]["api_key"]
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# Initialize the OpenAI language model
OPENAI_API_KEY = st.secrets["OPENAI_API"]["chatgpt_api"]
#llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.7)
#llm = ChatOpenAI(model="gpt-4", temperature=0)

# Define a list of industries
industries = [
    'automobile', 'e-vehicle', 'renewable energy', 'technology', 
    'environment', 'global affairs', 'healthcare', 'finance', 
    'entertainment', 'sports', 'real estate', 'education', 
    'agriculture', 'fashion', 'travel', 'food & beverages'
]

# Get the user's selected industry
col1,col2,col3=st.columns([0.5,1.5,.5])
col2.subheader('Selet a News Segment')
col1,col2,col3=st.columns([0.5,1.5,.5])
selected_industry = col2.selectbox(' ', industries)
st.write('\n')
# Date range selection
st.write('\n')
st.subheader('select a Date Range for the top 10 Trending News Headlines')
today = datetime.date.today()
col1,col2=st.columns(2)
start_date = col1.date_input('Start Date', min_value=today - datetime.timedelta(days=7), value=today - datetime.timedelta(days=7))
end_date = col2.date_input("End Date")

st.write('\n')
st.write('\n')

# Initialize session state variables if they don't exist
if 'selected_news' not in st.session_state:
    st.session_state.selected_news = None

if 'news_headlines' not in st.session_state:
    st.session_state.news_headlines = []

# Fetch headlines button
col1,col2,col3=st.columns(3)
if col2.button("Fetch Headlines"):
    try:
        # Fetch the top 5 trending news headlines for the selected industry within the date range and in English
        news_articles = newsapi.get_everything(q=selected_industry, 
                                               from_param=start_date,  
                                               to=end_date,          
                                               sort_by='relevancy',
                                               language='en',
                                               page_size=10)

        # Extract the headlines from the articles
        headlines = [article['title'] for article in news_articles['articles']]
        st.session_state.news_headlines = list(set(headlines))  # Remove duplicates using set

    except Exception as e:
        st.error(f"Error: {e}")

# Display the news headlines as selectable options if headlines are fetched
if st.session_state.news_headlines:
    st.session_state.selected_news = st.radio("Select a news headline:", st.session_state.news_headlines)

# Confirm news selection button
if st.session_state.selected_news and st.button("Confirm Selection"):
    st.write("You selected:")
    selected_headline_html = f"""
    <div style="
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: #4CAF50;
        color: white;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    ">
        Selected Headline: {st.session_state.selected_news}
    </div>
    """
    st.markdown(selected_headline_html, unsafe_allow_html=True)
    st.write('\n')
    st.write('\n')
    
    # Display a temporary message while the article is being generated
    temp_message = st.markdown(waiting_html, unsafe_allow_html=True)
    # Generate LinkedIn post based on the selected headline
    linkedin_prompt = f"""
    Craft an engaging LinkedIn post within 500 words based on the provided {st.session_state.selected_news}. 
    The post should be targeted towards the {selected_industry} professionals. 
    Incorporate statistical data to support key arguments and points throughout the post. 
    Begin with a captivating hook sentence to encourage users to click on 'read more' instantly. 
    Emulate the writing styles of renowned LinkedIn influencers like Gary Vaynerchuk/ Simon Sinek/ Arianna Huffington. 
    Write in a compact and concise manner, utilizing bullet points where appropriate. 
    Share insights from the news article, highlighting industry trends, advancements to foster positive discussions.
    Also include emojis in between the sesntences whichever and wherever its applicable and looks good
    """
    
    

    try:
        # Instantiate the OpenAI LLM model
        llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, temperature=0.7)
        
        # Generate the LinkedIn post
        response = llm(linkedin_prompt)
        
        # Directly use the response as the generated post
        generated_post = response

        # Replace the temporary message with the generated LinkedIn post
        temp_message.text_area("Generated LinkedIn Post:", generated_post, height=600)
        
    
    except Exception as e:
        st.error(f"Error generating LinkedIn post: {e}")