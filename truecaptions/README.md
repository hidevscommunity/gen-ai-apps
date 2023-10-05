# truecaptions - Image and Text Validation Streamlit App

This Streamlit app allows you to validate both images and text using the Clarifai and OpenAI APIs. You can upload an image, and the app will generate a caption for it using Clarifai. It will also generate a question based on the caption using OpenAI's GPT-3. After that, it will provide an answer to the generated question.

Similarly, you can input text, and the app will use OpenAI's GPT-3 to determine whether the text is valid or not.

## Setup

Before running the app, you need to set up your Clarifai and OpenAI API credentials.

1. Install the required Python libraries:
   ```bash
   pip install streamlit clarifai-grpc openai

## Image Validation <br>
• Use the "Upload an image" section to upload an image (supported formats: jpg, png, jpeg).
• The app will process the uploaded image using Clarifai to generate a caption.
• It will then use OpenAI's GPT-3 to generate a question based on the caption and provide an answer to that question.

## Text Validation <br>
• In the "Text Validation" section, enter the text you want to validate in the text input field.
• Click the "Validate" button.
• The app will use OpenAI's GPT-3 to determine whether the input text is valid or not and display the validation result.

## Dependencies
• Streamlit
• Clarifai Python gRPC
• OpenAI Python library

## Author <br>
[Om Bhojane]
