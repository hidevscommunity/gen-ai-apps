
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

from streamlit_extras.buy_me_a_coffee import button

import openai
import base64
import random

def sidebar_bg(side_bg):

   side_bg_ext = 'jpg'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )


# Define a function to generate an image using the OpenAI API with cache
def get_img(prompt, image_cache):
    # Check if the prompt is already in the cache
    
    if prompt in image_cache:
        return image_cache[prompt]
    
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        img_url = response.data[0].url
        # Cache the prompt-image URL pair
        image_cache[prompt] = img_url
    except Exception as e:
        # if it fails (e.g. if the API detects an unsafe image), use a default image
        img_url = "sorry"
    
    return img_url

def init():
    # Load the OpenAI API key from the environment variable
    load_dotenv()
    
    # test that the API key exists
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        print("OPENAI_API_KEY is set")

    # setup streamlit page
    st.set_page_config(
        page_title="Byomkesh Bakshi",
        page_icon="🫖"
    )


def generate_case():
    # List of sample cases with Indian names and places
    cases = [
        {
            "title": "The Mysterious Necklace",
            "description": "Case: A valuable necklace belonging to Mrs. Meera Verma has been stolen from her house in Mumbai. The prime suspects are her maid, Geeta, and her neighbor, Ramesh Gupta. Your task is to find out who stole the necklace. Ask questions and gather clues to solve the case.",
            "solution": "The maid, Geeta, stole the necklace."
        },
        {
            "title": "The Secret Room",
            "description": "Case: A secret room has been discovered in a centuries-old palace in Jaipur. The room contains ancient artifacts, but one of them is missing. The suspects are the caretaker, Ram Singh, and the historian, Dr. Maya Sharma. Your task is to find out who took the missing artifact. Ask questions and gather clues to solve the case.",
            "solution": "The caretaker, Ram Singh, took the missing artifact."
        },
        {
            "title": "The Enigmatic Painting",
            "description": "Case: A valuable painting by renowned artist Ravi Varma has been stolen from an art gallery in Delhi. The suspects are an art collector, Vikram Kapoor, and an art dealer, Anita Verma. Your task is to find out who is behind the theft. Ask questions and gather clues to solve the case.",
            "solution": "The art dealer, Anita Verma, is behind the theft."
        }
    ]

    # Select a random case
    selected_case = random.choice(cases)

    return selected_case

# Convert messages to dictionaries
def convert_message_to_dict(message):
    if isinstance(message, SystemMessage):
        return {"role": "system", "content": message.content}
    elif isinstance(message, HumanMessage):
        return {"role": "user", "content": message.content}
    elif isinstance(message, AIMessage):
        return {"role": "assistant", "content": message.content}
    else:
        raise ValueError(f"Got unknown type {message}")

def main():
    init()

    sidebar_bg("assets/main.jpg")

    chat = ChatOpenAI(temperature=0)

    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="Welcome, detective. A new case awaits your brilliant mind.")
        ]
    if "prompt" not in  st.session_state:
        st.session_state.prompt = {}


    st.header("Detective Byomkesh Bakshi")
    st.subheader("सत्यनवेशी: सत्य की खोज करने वाला")
    
    case = None
    # Check if a case has already been assigned
    if "current_case" not in st.session_state:
        # Generate a new case
        case = generate_case()
        st.session_state.current_case = case

        st.session_state.messages.append(SystemMessage(content="Case: " + case["title"]))
        st.session_state.messages.append(SystemMessage(content=case["description"]))
        st.session_state.messages.append(SystemMessage(content="Your task is to find out the solution to the case. Ask questions and gather clues to solve it. Good luck, detective!"))

    # sidebar with user input
    with st.sidebar:
        user_input = st.text_input("Your message: ", key="user_input")

        button(username="princep", floating=False, width=221)

        # handle user input
        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            
            st.session_state.messages.append(AIMessage(content=response.content))
            
            # Check if user has found the solution
            if case is not None and "solution" in case and case["solution"] in response.content.lower():
                st.success("Congratulations! You have found the solution to the case!")
                st.balloons()

                # Generate a new case
                case = generate_case()
                st.session_state.current_case = case

                st.session_state.messages.append(SystemMessage(content="Case: " + case["title"]))
                st.session_state.messages.append(SystemMessage(content=case["description"]))
                st.session_state.messages.append(SystemMessage(content="Your task is to find out the solution to the case. Ask questions and gather clues to solve it. Good luck, detective!"))

    # Convert messages to dictionaries
    messages_dict = [convert_message_to_dict(msg) for msg in st.session_state.messages]
    
    # Group messages based on role
    grouped_messages = {}
    for msg_dict in messages_dict:
        role = msg_dict["role"]
        if role in grouped_messages:
            grouped_messages[role].append(msg_dict)
        else:
            grouped_messages[role] = [msg_dict]

    print(st.session_state.prompt)
    # Display grouped messages
    for role, group in grouped_messages.items():
        for i, msg_dict in enumerate(group):
            message_content = msg_dict["content"]
            if role == "system":
                image_url = get_img(message_content, st.session_state.prompt)
                message(message_content, is_user=False, key=str(i) + '_' + role)
                if image_url != "sorry":
                    st.image(image_url)
            elif role == "user":
                message(message_content, is_user=True, key=str(i) + '_' + role)
            else:
                image_url = get_img(message_content, st.session_state.prompt)
                message(message_content, is_user=False, key=str(i) + '_' + role)
                if image_url != "sorry":
                    st.image(image_url)

if __name__ == '__main__':
    main()
