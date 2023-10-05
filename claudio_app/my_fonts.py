import streamlit as st

# SET FONT STYLES
font_style = """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Ysabeau+SC:wght@200&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Rubik+Dirt&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Rock+Salt&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Josefin+Slab:wght@200&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Koulen&display=swap');
            /* Set the font family for paragraph elements */
            p {
               font-family: 'Ysabeau SC', sans-serif;
            }
            
            /* Set the font family, size, and weight for unordered list and ordered list elements */
            ul, ol {
                font-family: 'Ysabeau SC', sans-serif;
                font-size: 16px;
                font-weight: normal;
            }
            
            /* Set the font family, size, weight, and margin for list item elements */
            li {
                font-family: 'Ysabeau SC', sans-serif;
                font-size: 16px;
                font-weight: normal;
                margin-top: 5px;
            }
            </style>
            """
            
# Define a function to convert sentiment scores to colored text
def color_text_by_sentiment(text, sentiment_score):
    # Define color ranges for positive, neutral, and negative sentiment
    if sentiment_score > 0.1:
        color = 'lightgreen'  # Light green for positive
    elif sentiment_score < -0.1:
        color = 'lightcoral'  # Light red for negative
    else:
        color = 'lightgray'   # Light gray for neutral

    # Use HTML to apply the color to the text
    colored_text = f'<span style="background-color:{color};padding:2px;border-radius:4px;">{text}</span>'
    return colored_text


def my_text_header(my_string,
                   my_text_align='center', 
                   my_font_family='Lobster, cursive;',
                   my_font_weight=200,
                   my_font_size='36px',
                   my_line_height=1.5):
    text_header = f'<h1 style="text-align:{my_text_align}; font-family: {my_font_family}; font-weight: {my_font_weight}; font-size: {my_font_size}; line-height: {my_line_height};">{my_string}</h1>'
    st.markdown(text_header, unsafe_allow_html=True)

# def my_text_paragraph(my_string,
                       # link_url=None,
                       # my_text_align='center',
                       # my_font_family='Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
                       # my_font_weight=200,
                       # my_font_size='18px',
                       # my_line_height=1.5,
                       # add_border=False,
                       # border_color="#45B8AC"):
    # if add_border:
        # border_style = f'border: 2px solid {border_color}; border-radius: 10px; padding: 10px; box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);'
    # else:
        # border_style = ''
    
    # if link_url:
        # paragraph = f'<p style="text-align:{my_text_align}; font-family:{my_font_family}; font-weight:{my_font_weight}; font-size:{my_font_size}; line-height:{my_line_height}; background-color: rgba(255, 255, 255, 0); {border_style}">{my_string} <a href="{link_url}" target="_blank">Click here</a></p>'
    # else:
        # paragraph = f'<p style="text-align:{my_text_align}; font-family:{my_font_family}; font-weight:{my_font_weight}; font-size:{my_font_size}; line-height:{my_line_height}; background-color: rgba(255, 255, 255, 0); {border_style}">{my_string}</p>'
    
    # st.markdown(paragraph, unsafe_allow_html=True)        

def my_text_paragraph(my_string, 
                      score=None,
                      sentiment_score=None,
                      link_url=None,
                      my_text_align='center',
                      my_font_family='Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
                      my_font_weight=200,
                      my_font_size='18px',
                      my_line_height=1.5,
                      confidence_font_size='12px',  # Specify a separate font size for the confidence score
                      add_border=False,
                      border_color="#45B8AC"):
    if add_border:
        border_style = f'border: 2px solid {border_color}; border-radius: 10px; padding: 10px; box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);'
    else:
        border_style = ''

    if sentiment_score is not None:
        colored_text = color_text_by_sentiment(my_string, sentiment_score)
        paragraph = f'<p style="text-align:{my_text_align}; font-family:{my_font_family}; font-weight:{my_font_weight}; font-size:{my_font_size}; line-height:{my_line_height}; background-color: rgba(255, 255, 255, 0); {border_style}">{colored_text}</p>'
    elif link_url:
        if score is not None:
            formatted_score = f" (Confidence Score: {int(score * 100)}%)"
            my_string_with_score = f"{my_string}<span style='font-size:{confidence_font_size}'>{formatted_score}</span>"
        else:
            my_string_with_score = my_string
        paragraph = f'<p style="text-align:{my_text_align}; font-family:{my_font_family}; font-weight:{my_font_weight}; font-size:{my_font_size}; line-height:{my_line_height}; background-color: rgba(255, 255, 255, 0); {border_style}">{my_string_with_score} <a href="{link_url}" target="_blank">Click here</a></p>'
    else:
        if score is not None:
            formatted_score = f" (Confidence Score: {int(score * 100)}%)"
            my_string_with_score = f"{my_string}<span style='font-size:{confidence_font_size}'>{formatted_score}</span>"
        else:
            my_string_with_score = my_string
        paragraph = f'<p style="text-align:{my_text_align}; font-family:{my_font_family}; font-weight:{my_font_weight}; font-size:{my_font_size}; line-height:{my_line_height}; background-color: rgba(255, 255, 255, 0); {border_style}">{my_string_with_score}</p>'

    st.markdown(paragraph, unsafe_allow_html=True)