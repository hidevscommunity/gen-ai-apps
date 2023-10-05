import datetime
import logging
import random
from dataclasses import dataclass
from pprint import pprint

import cachetools
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from clarifai import Workflow

sample_reviews = [
    {"sentiment": "Positive",
     "text": "This film stands out in today's cinema landscape. Every scene is thoughtfully crafted, and the characters have depth and nuance. The story flows naturally, keeping viewers engaged. It's a high point in recent movie releases."},
    {"sentiment": "Positive",
     "text": "The film wields a powerful narrative, fused with a humor that's both organic and poignant. Our protagonist's journey is a tapestry of emotive beats, matched by an equally evocative score. The performances here aren't merely acted; they're lived. This is cinema in its most resonant form."},
    {"sentiment": "Positive",
     "text": "This film is a breath of fresh air. Beautifully shot scenes and a compelling storyline make it a standout. The cast's chemistry is palpable, driving the narrative forward with ease. A delightful cinematic experience from start to finish."},
    {"sentiment": "Positive",
     "text": "A captivating blend of drama and wit. The director's vision shines through every frame, complemented by a pitch-perfect score. Performances are top-notch, drawing viewers into the heart of the story. It's a film that lingers long after the credits roll."},
    {"sentiment": "Neutral",
     "text": "While the movie had its moments, it failed to leave a lasting impression. The cast did their job, but the script lacked depth. The music was fitting but forgettable. Overall, an average experience."},
    {"sentiment": "Neutral",
     "text": "There are moments of brilliance, but they're spread thin. Some themes resonate, but the delivery isn't always there. The music fits but isn't standout. It's a mixed bag overall."},
    {"sentiment": "Neutral",
     "text": "The movie is competently made, with moments that genuinely shine. However, the story often treads familiar territory, making it predictable at times. While the actors put forth solid performances, the script limits their potential. An even mix of highs and lows."},
    {"sentiment": "Neutral",
     "text": "It's a film that has its moments but fails to fully captivate. The visual appeal is there, but the emotional depth is inconsistent. Some scenes are beautifully executed, while others fall flat. A decent watch but not groundbreaking."},
    {"sentiment": "Negative",
     "text": "The movie starts with promise but soon disappoints. It drags at times, and some dialogues feel forced. Despite a talented cast, the script doesn't do them justice. It's a forgettable outing."},
    {"sentiment": "Negative",
     "text": "The film, regrettably, buckles under the weight of its own aspirations. Amidst its sprawling narrative, the essence is lost, characters relegated to mere shadows. Even its cinematographic choices, while occasionally inspired, largely feel derivative. A cinematic journey that promises much but delivers little."},
    {"sentiment": "Negative",
     "text": "Despite its potential, the film doesn't quite hit the mark. The narrative feels disjointed, often losing its momentum. While there are a few standout performances, they're overshadowed by a lackluster script. A missed opportunity in storytelling."},
    {"sentiment": "Negative",
     "text": "The movie offers a premise filled with promise but struggles in its execution. Pacing issues detract from key moments, and character development is lacking. While it boasts some well-composed shots, they're not enough to lift the overall experience. A film that's less than the sum of its parts."}
]

# Review = namedtuple('Review', ['text', 'date', 'sentiment', 'votes'])
st.toast('Welcome to review sentinel')


if 'history' not in st.session_state:
    c = cachetools.Cache(maxsize=100)
    print('history not found')
    st.session_state.history = c
    c['reviews'] = []
    c['in_progress'] = False
else:
    c = st.session_state.history

reviews = c['reviews']


@dataclass
class Review:
    text: str
    date: str
    sentiment: str
    votes: int


st.title("Movie Review Sentiment Analyzer")

sample_review = random.choice(sample_reviews)

new_review_text = st.text_input("Enter a movie review: ", value=sample_review["text"])
if st.button("Add Review", disabled=c['in_progress']) and new_review_text.strip() != "":
    r = Review(text=new_review_text, date=str(datetime.datetime.now()), sentiment='', votes=0)
    reviews.append(r)
    c['in_progress'] = True

for i, review in enumerate(reviews):
    # ic(review)
    if review.sentiment == "":
        with st.spinner(text='Sentiment Analysis In Progress'):
            c['in_progress'] = True
            w1 = Workflow('sentiment-analysis')
            try:
                res = w1.run(review.text)
            except Exception as e:
                logging.error(e)
                continue

            c['in_progress'] = False

        st.balloons()

        outputs = res.results[0].outputs

        pprint(outputs)

        o = outputs[1]
        possible_sentiments = ["Positive", "Negative", "Neutral"]

        # print(o)

        sentiment = o.data.text.raw

        for s in possible_sentiments:
            if s.lower() in sentiment.lower():
                sentiment = s
                break

        if sentiment not in possible_sentiments:
            raise ValueError('invalid sentiment')
        # sentiment = sentiment.replace("My answer:","").strip()

        print(f"sentiment is {sentiment}")
        print(f"review is {review}")
        # Update the review's sentiment
        # review._replace(sentiment=sentiment)
        review.sentiment = sentiment
    st.write(f"Review: {review.text}")
    st.write(f"Date: {review.date}")
    st.write(f"Sentiment: {review.sentiment}")
    st.write(f"Votes: {review.votes}")


    def onclick(i, inc):
        print(f"voting-{i}")
        reviews[i].votes += inc


    st.button("Upvote", key=f"up-{i}", on_click=lambda i=i: onclick(i, 1))
    # review = review._replace(votes=review.votes + 1)
    st.button("Downvote", key=f"down-{i}", on_click=lambda i=i: onclick(i, -1))

# st.write(reviews)
# for i, review in enumerate(reviews):
#
#     # review = review._replace(votes=review.votes - 1)
