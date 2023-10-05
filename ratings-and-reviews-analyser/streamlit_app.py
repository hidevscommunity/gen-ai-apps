import streamlit as st
from backend.review_analyser import analyse_reviews
from backend.amazon_review_scraper import get_amazon_reviews


st.title("Amazon Reviews Analyser")

with st.sidebar:
    api_key = st.text_input(label="Your Open AI API Key", type="password")

product_url = st.text_input(
    label="Enter Amazon product link",
    value="https://www.amazon.co.uk/Notebook-Refillable-Travelers-Professionals-Organizer/dp/B01N24BYQ7/ref=sr_1_1_sspa?crid=16IFJTVN8OZTQ&keywords=traveler%2Bnotebook%2Bpassport%2Bnotebooks&qid=1694895888&sprefix=%2Caps%2C165&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1",
)


if st.button(label="Analyse", use_container_width=True):
    reviews = get_amazon_reviews(product_url)

    try:
        result = str(analyse_reviews(reviews=reviews, openai_api_key=api_key))

        tab1, tab2 = st.tabs(["Overview", "Reviews"])
        with tab1:
            st.markdown(result)

        with tab2:
            reviews_list = reviews.get("reviews")

            # loop through list of reviews
            for review in reviews_list:
                name = review.get("name")
                title = review.get("title")
                rating = review.get("rating")
                review_text = review.get("review_text")
                st.markdown(
                    f"""
                    ## {name}
                    
                    #### {title}
                    
                    Rating: {rating}
                    
                    {review_text}
                    """
                )
                st.divider()
    except:
        st.error("Please provide an Open AI API Key.")
