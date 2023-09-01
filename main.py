import datetime
import os
import random
from dataclasses import dataclass
from pprint import pprint
from typing import Final

import cachetools
import streamlit as st
from dotenv import load_dotenv

load_dotenv()



# Review = namedtuple('Review', ['text', 'date', 'sentiment', 'votes'])

c = cachetools.Cache(maxsize=100)

if 'history' not in st.session_state:
    print('history not found')
    st.session_state.history = c
    c['models'] = []
else:
    c = st.session_state.history

models = c['models']

st.title("Movie Review Sentiment Analyzer")

sample_review = random.choice(sample_models)

new_review_text = st.text_input("Enter a movie review: ", value=sample_review["text"])
if st.button("Add Review") and new_review_text.strip() != "":
    r = Review(text=new_review_text, date=str(datetime.datetime.now()), sentiment='', votes=0)
    models.append(r)

for review in models:
    # ic(review)

    if review.sentiment == "":
        w1 = Workflow('sentiment-analysis')

        res = w1.run(review.text)

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

# st.write(models)
for i, review in enumerate(models):
    st.write(f"Review: {review.text}")
    st.write(f"Date: {review.date}")
    st.write(f"Sentiment: {review.sentiment}")
    st.write(f"Votes: {review.votes}")


    def onclick(inc):
        review.votes += inc


    st.button("Upvote", key=f"up-{i}", on_click=lambda: onclick(1))
    # review = review._replace(votes=review.votes + 1)
    st.button("Downvote", key=f"down-{i}", on_click=lambda: onclick(-1))
    # review = review._replace(votes=review.votes - 1)
