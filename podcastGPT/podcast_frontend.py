import streamlit as st
import modal
import json
import os
import feedparser

# podcast_feed_url = "https://www.omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/8a94442e-5a74-4fa2-8b8d-ae27003a8d6b/982f5071-765c-403d-969d-ae27003a8d83/podcast.rss"

def main():
    st.title("PodcastGPT Dashboard")

    st.markdown(
    """
    This app assists busy professionals with transcribing and summarizing Podcasts from [Listen Notes](https://www.listennotes.com/) website by following the below steps:
    - Search for your desired podcast from the Listen Notes website and click on the "RSS" tab to generate a unique link to the podcast. Example shown below: 
"""
)
    col1, col2 = st.columns(2)
    
    with col1:
        
        st.image('RSS.png', caption = 'Click RSS')

    with col2:

        st.image('RSS_copy.png',caption='Copy RSS Link')

    st.markdown(
    """
    - Copy the generated link and paste in the sidebar on the left: 
"""
)

    pods = {}
    
    # Left section - Input fields
    st.sidebar.header("Podcast RSS Feeds")

    # Input Box
    podcast_url = st.sidebar.text_input('Please paste the podcast RSS feed link here')

    latest_ep_button = st.sidebar.button("Get latest 5 Episodes")
    
    # st.sidebar.markdown("**Note**: Podcast processing can take upto 5 mins, please be patient.")

    if latest_ep_button:
        
        #Extract the list of episodes for the given podcast
        podcast_feed = feedparser.parse(podcast_url)

        for pod in podcast_feed.entries[:5]:
            podcast_title = pod['title']
        
            try:
                podcast_image = pod['image']['href']
        
            except:
                podcast_image = ''
        
            for i in pod['links']:
                if i['type'] == 'audio/mpeg':
                    podcast_url = i['href']

            pods.update({pod['title']:[podcast_url,podcast_image]})
            
        #Get the most recent 5 episodes
        podcast_five_titles = list(pods.keys())

        # Dropdown box
        st.sidebar.subheader("Available Podcasts Feeds")
        selected_podcast = st.sidebar.selectbox("Select Podcast", options=podcast_five_titles)

        if selected_podcast:
    
            st.sidebar.markdown("**Note**: Podcast processing can take upto 5 mins, please be patient.")
            
            podcast_link = pods[selected_podcast][0]
            podcast_image = pods[selected_podcast][1] 
    
            # Right section - Newsletter content
            st.header("Newsletter Content")
    
            # Display the podcast title
            st.subheader("Episode Title")
            st.write(selected_podcast)
    
            # Display the podcast summary and the cover image in a side-by-side layout
            col1, col2 = st.columns([7, 3])
    
            # Get podcast transcription and info
            podcast_info = process_podcast_info(podcast_link)
            
            with col1:
                # Display the podcast episode summary
                st.subheader("Podcast Episode Summary")
                st.write(podcast_info['podcast_summary'])

            if podcast_image:
                with col2:
                    st.image(podcast_image, caption="Podcast Cover", width=300, use_column_width=True)
    
            # Display the podcast guest and their details in a side-by-side layout
            col3, col4 = st.columns([3, 7])
    
            with col3:
                st.subheader("Podcast Guest")
                st.write(podcast_info['podcast_guest'])
    
            with col4:
                st.subheader("Podcast Guest Details")
                st.write(podcast_info["podcast_guest_title"])
                st.write(podcast_info["podcast_guest_org"])
    
            # Display the five key moments
            st.subheader("Key Moments")
            key_moments = podcast_info['podcast_highlights']
            for moment in key_moments.split('\n'):
                st.markdown(
                    f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)


def process_podcast_info(url):
    f = modal.Function.lookup("corise-podcast-project", "process_podcast")
    output = f.call(url, '/content/')
    return output

if __name__ == '__main__':
    main()
