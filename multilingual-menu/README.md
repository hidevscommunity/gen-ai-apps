# Multilingual Menu  👨‍🍳🍳


LLM technologies: LangChain, Clarifai.

Clarifai models : *GPT-4*, *food-item-recognition*

## Description:
An interactive Streamlit application to generate multilingual recipes based on ingredient images or manual input. Utilizes Clarifai's AI models for image recognition and language generation.

This is a Streamlit app designed to take uploaded images of ingredients, identify the ingredient via the Clarifai API, and generate a recipe based on those ingredients in a desired language and culinary style.

## Features:
- 📷 **Image-based Ingredient Detection**: Upload images of your ingredients and the app will predict their names.
- 📜 **Manual Ingredient Input**: Alternatively, manually type in your ingredients.
- 🍲 **Culinary Style Specification**: Define the culinary style or country of the desired recipe.
- 🌐 **Multilingual Support**: Generate the menu in your desired language.
- 📺 **Demo Video**: Visual walkthrough to guide users.
- ⚙️ **Interactive UI**: User-friendly interface with real-time feedback.

## Demo Video:

Link : https://www.youtube.com/watch?v=gmYVblv8rec

## How to Use:

1. **Upload Ingredients Image**: Use the file uploader to upload images of ingredients. The app will process these images and predict the ingredient name.
2. **OR Manually Enter Ingredients**: If you prefer, you can also manually enter the ingredients in the text input box.
3. **Specify Culinary Style**: Enter the desired country or style of the recipe.
4. **Specify Language**: Enter the desired language for the menu.
5. **Generate Recipe**: Click the "Generate Recipe" button. If all fields are filled correctly, a recipe will be displayed; otherwise, warning messages will guide the user.

## Dependencies:

- **Streamlit**: For creating the interactive web application.
- **Clarifai GRPC API**: For the image recognition feature to identify ingredients from images.

## Setup:

1. **Secret Keys**: The app requires several secret keys and identifiers (e.g., `PAT`, `USER_ID`, `APP_ID`, `MODEL_ID`) which should be stored securely in Streamlit's secrets management or another secure environment.
2. **Install Required Packages**: Make sure to install all the necessary packages using pip:
    ```
    pip install -r requirements.txt
    ```
3. **Run the App**: Navigate to the app directory and run:
    ```
    streamlit run app_filename.py
    ```

## Limitations:

- The accuracy of the ingredient prediction is dependent on the Clarifai model being used.
- Recipe generation is based on the provided template and might not always result in a fully detailed or traditional recipe.

## Feedback & Contributions:

Feel free to open issues if you find any bugs or want to suggest improvements. Contributions to the project are also welcome.

---

Thank you for using the Multilingual Menu App!
