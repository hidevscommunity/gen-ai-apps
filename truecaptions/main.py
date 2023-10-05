import streamlit as st
import openai
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

# Set your Clarifai API credentials
CLARIFAI_API_KEY = st.secrets["CLARIFAI_API_KEY"]
openai.api_key = st.secrets["openai_api_key"]

# Initialize Clarifai channel and stub
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

def process_image_with_clarifai(image_bytes, model_id):
    metadata = (('authorization', 'Key ' + CLARIFAI_API_KEY),)
    user_id = 'salesforce'
    app_id = 'blip'

    response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=resources_pb2.UserAppIDSet(user_id=user_id, app_id=app_id),
            model_id=model_id,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=image_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    if response.status.code != status_code_pb2.SUCCESS:
        st.error("Failed to process the image.")
        return None

    return response.outputs[0]

# Function to validate text and provide a reason
def validate_text_with_reason(input_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use gpt-3.5-turbo for chat-based models
        messages=[
            {"role": "system", "content": "You are a helpful assistant that validates text."},
            {"role": "user", "content": input_text},
        ]
    )

    if response.choices:
        answer = response.choices[0].message["content"].strip()
        if "valid" in answer.lower():
            reason_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use gpt-3.5-turbo for chat-based models
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides a reason."},
                    {"role": "user", "content": f"Why is '{input_text}' considered valid?"},
                ]
            )
            if reason_response.choices:
                reason = reason_response.choices[0].message["content"].strip()
                return f"{answer} because {reason}"
        return answer

    return "No answer found."

def generate_question_from_caption(caption):
    return f"Is '{caption}' valid?"

def answer_question(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use gpt-3.5-turbo for chat-based models
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions."},
            {"role": "user", "content": question},
        ]
    )

    if response.choices:
        answer = response.choices[0].message["content"].strip()
        return answer
    else:
        return "No answer found."

st.title("True Captions: Let's validate your content!")
st.sidebar.success("Navigate through pages 📚") 
st.write("Great Power comes Great Responsibility. As we increased the use of online news and social media, sometimes fake news and misinformation can be spread easily. This app helps you to validate your content before you share it with the world!🌎")

# Text input field
input_text = st.text_input("Enter text to validate:")

# Validation button
validate_button = st.button("Validate")

# Upload image from user
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

selected_demo_image = st.selectbox("Select a Demo Image:", ["None (Upload Your Own)", "elephant.jpg", "elephant-statue.png", "elephant-swimming.png", "elephant-flying.png"])

# Default demo image selection
if selected_demo_image == "elephant.jpg":
    demo_image_path = "ele.jpg"
elif selected_demo_image == "elephant-statue.png":
    demo_image_path = "elestatue.png"
elif selected_demo_image == "elephant-swimming.png":
    demo_image_path = "eleswimming.jpg"
elif selected_demo_image == "elephant-flying.png":
    demo_image_path = "eleflying.jpg"
else:
    demo_image_path = None

if validate_button and input_text:
    
    validation_result = validate_text_with_reason(input_text)

    st.subheader("Validation Result:")
    if "valid" in validation_result.lower():
        st.success(validation_result)
    else:
        st.warning(validation_result)


if uploaded_image is not None:
    
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    # Process the uploaded image and get predictions
    image_bytes = uploaded_image.read()
    model_id = 'general-english-image-caption-blip' 

    output = process_image_with_clarifai(image_bytes, model_id)

    if output is not None:
        # Extract only the caption text
        image_caption = output.data.text.raw


        # Generate a question based on the caption
        question_image = generate_question_from_caption(image_caption)

        st.subheader("Predicted Image Caption using Clarifai Image Caption Generation Model:")
        st.write(image_caption)
        

         # Answer the generated question
        answer = answer_question(question_image)

        st.subheader("Answer:")

        if "valid" in answer.lower():
            st.success(answer)
        else:
            st.warning(answer)

if demo_image_path:
    
    st.image(demo_image_path, caption="Uploaded Image", use_column_width=True)

    with open(demo_image_path, "rb") as image_file:
        image_bytes = image_file.read()

    model_id = 'general-english-image-caption-blip'  # Change this to your desired model ID

    output = process_image_with_clarifai(image_bytes, model_id)

    if output is not None:
        # Extract only the caption text
        image_caption = output.data.text.raw

        # Generate a question based on the caption
        question_image = generate_question_from_caption(image_caption)

        st.subheader("Predicted Image Caption using Clarifai Image Caption Generation Model:")
        st.write(image_caption)

        # Answer the generated question
        answer = answer_question(question_image)

        st.subheader("Answer:")

        if "valid" in answer.lower():
            st.success(answer)
        else:
            st.warning(answer)