
from pathlib import Path
import base64
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io

##This module contains visualisation functions

def generate_cumulative_word_cloud(word_counts):
    # Only generate if word_counts is not empty
    if not word_counts or sum(word_counts.values()) == 0:
        return None
    # Generate the word cloud based on accumulated vocabulary
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)

    # Use matplotlib to create the figure
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

    # Convert the Matplotlib figure to an image buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close(fig)
    
    return buffer


    
# def generate_word_cloud(student_text):
#     tokens = tokenize(student_text)
#     word_counts = Counter(tokens)
    
#     # Generate the word cloud
#     wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)

#     # Use matplotlib to create the figure
#     fig, ax = plt.subplots(figsize=(10, 5))
#     ax.imshow(wordcloud, interpolation='bilinear')
#     ax.axis('off')
    
#     return fig

##images
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

