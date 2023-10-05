import streamlit as st
from hugchat import *
import assemblyai as aai
from pytube import YouTube
import os
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import base64
import pandas as pd
import plotly.express as px
from streamlit_plotly_events import plotly_events
import plotly.graph_objects as go
import streamlit as st
from streamlit_option_menu import option_menu
from pytube import YouTube, Search

# Configurations and Setups
aai.settings.api_key = "08ff03f3ed4e4c559c82ad4f0356220c"
PAT = "51cd7e5b97bc4ebc8ef94e0e245cbf00"
USER_ID = "homanfor1"
APP_ID = "moodDetector"
WORKFLOW_ID = "GPT-4-workflow-ai3yb8"

# Initializing services
transcriber = aai.Transcriber()
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.    V2Stub(channel)
metadata = (('authorization', 'Key ' + PAT),)
# Initiliazing weaviet 
#auth_config = weaviate.AuthApiKey(api_key=st.secrets["weaviate"]["api_key"])
#weaviate_client = weaviate.Client(
#    url=st.secrets["weaviate"]["url"],
#    auth_client_secret=auth_config
#)




#def initialize_schema():
#    try:
#        class_obj = {
#            'class': 'MyClass',
#            'properties': [
#                {'name': 'mood', 'dataType': ['text']},
#                {'name': 'transcription', 'dataType': ['text']}
                # Add more properties as needed
#            ]
#        }
#        weaviate_client.schema.create_class(class_obj)
#    except weaviate.exceptions.UnexpectedStatusCodeException as e:
        # Check the error message to see if it's because the class already exists
#        if 'class name "MyClass" already exists' in str(e):
            # If the class already exists, do nothing
#            pass
#        else:
            # If it's another error, raise it
#            raise e
# Call the function to ensure the schema is initialized
#initialize_schema()

########################
#####################
# weaviet functions #
#####################
#########################

#def save_mood_to_weaviate(mood, transcription):
   # mood_data = {
    #    "mood": mood,
    #    "transcription": transcription
   # }
    
#    try:
        # Use the create method to add data
#        weaviate_client.data_object.create(mood_data, "Mood")
#    except Exception as e:
#        st.error(f"Error saving mood and transcription to Weaviate: {e}")
    
#    try:
        # Use the create method to add data
  #      weaviate_client.data_object.create(mood_data, "Mood")
 #   except Exception as e:
 #       st.error(f"Error saving mood to Weaviate: {e}")
#
#def get_all_moods_and_transcriptions_from_weaviate():
#    """Retrieve all moods and transcriptions from Weaviate."""
    # Fetching both mood and transcription properties
#    query = weaviate_client.query.get("Mood", ["mood", "transcription"]).with_limit(100).do()
#    if "data" in query and "Get" in query["data"] and "Mood" in query["data"]["Get"]:
        # Creating a list of dictionaries for each mood and transcription
#        return [{"Mood": entry["mood"], "Transcription": entry["transcription"]} for entry in query["data"]["Get"]["Mood"]]
#    return []

def transcribe_audio(file):
    """Transcribes an audio file."""
    temp_filename = "temp_file.ogg"
    with open(temp_filename, "wb") as f:
        f.write(file.getbuffer())
    transcript = transcriber.transcribe(temp_filename)
    os.remove(temp_filename)
    return transcript.text

def transcribe_youtube(url):
    """Transcribes audio from a YouTube URL."""
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    download_url = stream.url
    transcript = transcriber.transcribe(download_url)
    return transcript.text

def get_mood_clarifai(sentence):
    """Gets mood for a given sentence using Clarifai."""
    RAW_TEXT = 'Recognize the Mood of the following sentence: ' + sentence
    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=userDataObject,
            workflow_id=WORKFLOW_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=RAW_TEXT
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        print(post_workflow_results_response.status)
        raise Exception("Post workflow results failed, status: " + post_workflow_results_response.status.description)
    results = post_workflow_results_response.results[0]
    res = results.outputs[0].data.text.raw
    return res

def display_transcription_results(transcription, keyword):
    """Displays transcription and mood results in Streamlit."""
    st.text_area("Transcription:", transcription, height=250)
    # mood_clarifai = get_mood_clarifai(transcription)
    # st.write(f"Mood of the content (using Clarifai): **{mood_clarifai}**")
    if keyword:
        occurrences = transcription.lower().count(keyword.lower())
        st.write(f"'{keyword}' found {occurrences} times.")
        highlighted_text = transcription.replace(keyword, f'**{keyword}**')
        st.markdown(highlighted_text)
    st.download_button("Download Transcription", data=transcription, file_name="transcription.txt")

def set_page_background():
    """Sets the Streamlit page background using custom CSS."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://cdn.midjourney.com/59e387e5-b025-445a-9573-9ff32daaa623/0_0.webp");
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def display_sidebar():
        
    """
    Displays the sidebar options and returns the selected method.
    """
    user_type = st.sidebar.radio("", ["Standard User", "Content Creator (🔜)", "Programmers (🔜)"])
    if user_type == "Standard User":
        st.sidebar.header("Choose your method:")
        
        # Enhanced sidebar using option_menu component
        methods = ["Youtube/Upload", "Article Processing", "Observe Weaviate Database", "ChatBot"]
        
        # Customize the appearance and icons of the option_menu
        selected_method = option_menu(
            "Standard Functionalities", 
            methods,
            icons=['film', 'newspaper', 'database', 'chat-dots-fill'],  # Enhanced icons for each method
            menu_icon="list-ul",  # Icon for the menu title
            styles = {
                "container": {
                    "padding": "10px!important",
                    "background-color": "#2d2d2d"  # Dark grey background, looks professional and less stark
                },
                "menu-title": {
                    "color": "#f4a261",  # A more muted, but still warm color
                    "font-weight": "700",  # Bolder weight for title
                    "font-size": "22px",
                    "margin-bottom": "10px"
                },
                "icon": {
                    "color": "#f4a261",
                    "font-size": "20px",
                    "margin-right": "12px"
                },
                "nav-link": {
                    "font-size": "18px",
                    "text-align": "left",
                    "margin": "5px 0",  # Small margin to space them out slightly
                    "--hover-color": "#404040"  # Slightly lighter grey for hover
                },
                "nav-link-selected": {
                    "background-color": "#556ee6",  # Brighter blue to stand out
                    "color": "#ffffff",  # White for contrast
                    "font-weight": "700",  # Bolder font weight for selected item
                    "padding": "5px 10px"  # Padding to give the selection more presence
                },
                "separator": {
                    "border-color": "#556ee6",
                    "margin": "10px 0"  # Vertical margin to give breathing space around separators
                }
            }
        )

        return selected_method

        # Placeholder for future methods
    elif user_type == "Content Creator (Soon!)":
        st.sidebar.write("Stay tuned for exciting features!")
        return None

    elif user_type == "Programmers (Soon!)":
        st.sidebar.write("Exciting tools and features coming soon!")
        return None
    
def summarize_text_clarifai(text, word_count):
    """Gets Summarization for a given sentence using Clarifai."""
    RAW_TEXT = f'Summarize the following text under {word_count} words. the article : {text}'
    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=userDataObject,
            workflow_id=WORKFLOW_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=RAW_TEXT
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        print(post_workflow_results_response.status)
        raise Exception("Post workflow results failed, status: " + post_workflow_results_response.status.description)
    results = post_workflow_results_response.results[0]
    res = results.outputs[0].data.text.raw
    return res

def article_processing(user_text):
    """Processes an article to get its mood and summarize it."""
    with st.spinner("🔮 Detecting mood..."):
        mood = get_mood_clarifai(user_text)
    st.success(f"🎉 Predicted Mood using Clarifai: **{mood}**")

    # Add button to save mood to Weaviate
    #if mood and st.button("Save Mood to Weaviate"):
    #    save_mood_to_weaviate(mood, user_text)
     #   st.success("Mood saved to Weaviate!")

    with st.spinner("📝 Summarizing text..."):
        summarized_text = summarize_text_clarifai(user_text)
    st.text_area("Summarized Transcript:", summarized_text, height=250)
def classify_text_with_clarifai(user_text):
    # Define necessary variables
    PAT = '51cd7e5b97bc4ebc8ef94e0e245cbf00'
    USER_ID = 'homanfor1'
    APP_ID = 'moodDetector'
    WORKFLOW_ID = 'workflow-fa7a13'
    TEXT_FILE_URL = 'https://samples.clarifai.com/negative_sentence_12.txt'

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', 'Key ' + PAT),)
    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    RAW_TEXT = f"classify the following paragraph : {user_text}"
    
    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=userDataObject,  
            workflow_id=WORKFLOW_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=RAW_TEXT
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    
    # Handle errors in response
    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Post workflow results failed, status: " + post_workflow_results_response.status.description)

    results = post_workflow_results_response.results[0]

    # Each model we have in the workflow will produce one output.
    for output in results.outputs:
        model = output.model

    print("Predicted concepts for the model `%s`" % model.id)
    for concept in output.data.concepts:
        print("	%s %.2f" % (concept.name, concept.value))
    res = results.outputs[0].data.text.raw
        
    return res

def display_article_processing_results(text):
    """Handles the Article Processing method"""

    # Display Slider for User to Select Word Count for Summary
    # Check if mood has already been detected
    if 'mood' not in st.session_state:
        mood = get_mood_clarifai(text)
        st.session_state.mood = mood
        st.success(f"🎉 Predicted Mood using Clarifai: **{mood}**")
    else:
        st.success(f"🎉 Predicted Mood using Clarifai: **{st.session_state.mood}**")
        
    word_count = st.slider("Select number of words for your summary", 25, 50, 100)
    # Check if summarize button is clicked
    if st.button("Summarize Text"):
        summarized_text = summarize_text_clarifai(text, word_count)
        st.text_area("Summarized Transcript:", summarized_text, height=250)
    
    # Option to save mood to Weaviate
    #if st.session_state.mood and st.button("Save Mood to Weaviate"):
     #   save_mood_to_weaviate(st.session_state.mood, text)
    #    st.success("Mood saved to Weaviate!")
    # Step 2: Add button for classification and display results
    if st.button("Classify Text with Clarifai"):
        classified_text = classify_text_with_clarifai(text)
        st.text_area("Classification Results:", classified_text, height=250)
        
        # Step 3: Provide a download button for the classified text
        st.download_button(
            label="Download Classification Results",
            data=classified_text,
            file_name="classification_results.txt",
            mime="text/plain",
        )        
def to_csv_download_link(df, filename="data.csv"):
    """
    Generates a link to download the dataframe as a csv.
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}" style="display: none;"></a><script>location.href="{filename}"</script>'

#def get_mood_counts_from_weaviate():
  #  """Retrieve and parse moods from Weaviate, then count each mood's occurrences."""
    
    # Retrieve the data from Weaviate
   # query = weaviate_client.query.get("Mood", ["mood"]).with_limit(100).do()

    # Initialize an empty list to store parsed moods
   # parsed_moods = []

    # Check if the data is in the expected structure
  #  if "data" in query and "Get" in query["data"] and "Mood" in query["data"]["Get"]:
        # For each mood entry, split by commas and then strip whitespaces to parse individual moods
   #     for entry in query["data"]["Get"]["Mood"]:
    #        moods = entry["mood"].split(",")
    #        parsed_moods.extend([mood.strip() for mood in moods])

   # # Convert the list of parsed moods into a pandas series and get the value counts
   # mood_counts = pd.Series(parsed_moods).value_counts().to_dict()

   # return mood_counts

def plot_top_moods(mood_counts, top_n=3):
    """Generate a bar plot from the top_n moods with enhanced styling and better visualization."""
    
    # Sort moods by counts in descending order and select the top_n
    sorted_all_moods = dict(sorted(mood_counts.items(), key=lambda item: item[1], reverse=True))
    sorted_moods = dict(list(sorted_all_moods.items())[:top_n])
    
    # Generate a list of colors for the bars
    color_scale = px.colors.qualitative.Set1

    # Ensure there are enough colors for each mood by repeating the color set if necessary
    colors = (color_scale * (1 + len(sorted_moods) // len(color_scale)))[:len(sorted_moods)]
    
    # Create the bar chart using graph objects for more customization
    fig = go.Figure(go.Bar(
        x=list(sorted_moods.keys()),
        y=list(sorted_moods.values()),
        text=list(sorted_moods.values()),  # this will display the count on top of each bar
        marker_color=colors,
        hoverinfo='x+y',
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Rockwell"
        ),
        texttemplate='%{text}',
        textposition='outside'
    ))

    # Layout adjustments for a more professional look
    fig.update_layout(
        title={
            'text': f"Top {top_n} Detected Moods Frequency",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="Moods",
        yaxis_title="Count",
        font=dict(
            family="Rockwell, sans-serif",
            size=14,
            color="black"
        ),
        margin=dict(l=30, r=30, b=70, t=50),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    # Adding a grid for better readability
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)

    return fig

def get_youtube_link(query):
    search_results = Search(query).results
    if search_results:
        return search_results[0].watch_url
    return None

def main():
    
    set_page_background()

    # Create three columns
    col1, col2, col3 = st.columns([1,2,1])  # [1,2,1] means the middle column is twice as wide as the side columns

    with col1:
        st.write("")  # This acts as a placeholder to occupy space

    with col2:
        # Larger, centered title with potential custom styles
        st.markdown("<h1 style='text-align: center; color: orange;'>🤖MoodScribe</h1>", unsafe_allow_html=True)

    with col3:
        st.write("")  # Another placeholder to ensure symmetry
    #st.sidebar.image("logo/logo.png", caption="Your App Logo")  # Logo in the sidebar
    method = display_sidebar()

    if method == "Youtube/Upload":
        yt_url = st.text_input("🦜 Enter the YouTube video URL (or skip to upload an audio file):")

        if yt_url:
            keyword = st.text_input("🔍 Find in transcription:")
            yt = YouTube(yt_url)
            st.image(yt.thumbnail_url, caption=yt.title, use_column_width=True)
            if 'transcription' not in st.session_state:
                with st.spinner("🔄 Transcribing the YouTube video..."):
                    st.session_state.transcription = transcribe_youtube(yt_url)
            display_transcription_results(st.session_state.transcription, keyword)
        
        else:
            uploaded_file = st.file_uploader("📁 Upload an audio file:", type=["ogg", "mp3", "wav"])
            if uploaded_file:
                keyword = st.text_input("🔍 Find in transcription:")
                st.audio(uploaded_file, format='audio/ogg')
                if 'transcription' not in st.session_state:
                    with st.spinner("🔄 Transcribing your audio..."):
                        st.session_state.transcription = transcribe_audio(uploaded_file)
                display_transcription_results(st.session_state.transcription, keyword)
                
    elif method == "Article Processing":
    # Mood Detection Section
        st.header("🔮 Mood Detection")
        user_text = st.text_area("Enter the text for mood detection:", height=150)
        if user_text:
            mood = st.session_state.get('mood') or get_mood_clarifai(user_text)
            st.session_state.mood = mood
            st.success(f"Predicted Mood using Clarifai: **{mood}**")
            
            # Text Summarization Section
            st.header("📝 Text Summarization")
            word_count = st.slider("Select number of words for your summary", 25, 50, 100)
            if st.button("Summarize Text"):
                summarized_text = summarize_text_clarifai(user_text, word_count)
                st.text_area("Summarized Transcript:", summarized_text, height=250)

            # Text Classification Section
            st.header("🏷️ Text Classification with Clarifai")
            if st.button("Classify Text"):
                classified_text = classify_text_with_clarifai(user_text)
                st.text_area("Classification Results:", classified_text, height=250)
                
                # Download Classification Result
                st.download_button(
                    label="Download Classification Results",
                    data=classified_text,
                    file_name="classification_results.txt",
                    mime="text/plain",
                )
            
            # Database Integration Section
           # st.header("💾 Save to Weaviate Database")
          #  if st.button("Save Mood to Weaviate"):
          #      save_mood_to_weaviate(st.session_state.mood, user_text)
           #     st.success("Mood saved to Weaviate!")                
    elif method == "Observe Weaviate Database":
   #     with st.spinner("🔍 Fetching moods and transcriptions from Weaviate..."):
    #        moods_transcriptions = get_all_moods_and_transcriptions_from_weaviate()
        st.header("🗃️ SANDBOX EXPIRED ! ")
        st.write("Sorry, this feature is no longer available. Please try again later.")
        st.write("We apologize for any inconvenience.")
        st.write("You can still try out the other features of the app.")
        st.write("Thanks for your understanding.")
   #     if moods_transcriptions:
            # Convert the list of dictionaries to a dataframe
     #      df_moods_transcriptions = pd.DataFrame(moods_transcriptions)

            # Display the dataframe
     #       st.dataframe(df_moods_transcriptions)

            # Layout columns for buttons, visualization, and deletion functionality
      #      col1, col2, col3 = st.columns([1, 2, 1])  # Creates three columns 

       #     with col1:
        #        csv_data = df_moods_transcriptions.to_csv(index=False)
        #        st.download_button(
          #          label="Download as CSV",
           #         data=csv_data,
           #         file_name="moods_transcriptions.csv",
           #         mime="text/csv",
            #    )

          #  with col3:
            #    if st.button('Visualize Moods'):
             #       mood_counts = get_mood_counts_from_weaviate()
             #       fig = plot_top_moods(mood_counts)
              #      with col2:
          #              st.plotly_chart(fig, use_container_width=True)
#
            # Display the total count using st.metric() beneath the columns
        #    st.metric(label="Total Items in Database", value=len(df_moods_transcriptions), delta="1.0 +")
     #   else:
  #          st.write("No moods and transcriptions found in the database.")
    elif method == "ChatBot":
        # App title
        st.sidebar.title('🤗💬 HugChat')
        # Retrieve credentials from secrets
        hf_email = st.secrets['hugchat']['EMAIL']
        hf_pass = st.secrets['hugchat']['PASS']

        # Initial message for the chatbot
        if "messages" not in st.session_state.keys():
            st.session_state.messages = [{"role": "assistant", "content": "My name is ADMENAND but you can call me GREGOERY \n How may I Assist you Today?"}]

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Function for generating LLM response
        def generate_response(prompt_input, email, passwd):
            # Check if user's input matches a song request format
            if '-' in prompt_input:
                youtube_link = get_youtube_link(prompt_input)
                if youtube_link:
                    # Returns the video link to be displayed in the chat message.
                    return f"Here you go, this is the link to your request!\n{youtube_link}"
                else:
                    return "Sorry, I couldn't find the song on YouTube."
            # If not a song request, continue with the Chatbot's usual flow
            # Hugging Face Login
            sign = Login(email, passwd)
            cookies = sign.login()
            # Create ChatBot                        
            chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
            return chatbot.chat(prompt_input)
        # User-provided prompt
        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
        # Generate a new response if last message is not from assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_response(prompt, hf_email, hf_pass) 
                    st.write(response) 
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)
                     
          

                        
if __name__ == '__main__':
    main()  
