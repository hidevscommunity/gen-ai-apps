# DesignAId

An AI-powered application to assist in design thinking using the power of large language models.

## Introduction

`DesignAId` is an interactive Streamlit application that guides users through the design thinking process. The app uses AI to generate insights, suggestions, and guidance based on user inputs across various stages of the design thinking methodology: Empathize, Define, Ideate, Prototype, and Test.

## Features

1. **Interactive Interface**: Offers a step-by-step walkthrough of the design thinking stages.
2. **Autofill for Demo**: Users can quickly start with a demo setup, where the necessary fields are autofilled.
3. **AI-powered Suggestions**: Based on user input, the application generates AI suggestions for each stage.
4. **Report Generation**: After obtaining results, users can generate a downloadable PDF report.
5. **Input Review**: Users can review their input at any point.
6. **Restart Capability**: The application can be restarted from any stage.

## How to Use

1. **Autofill and Demo**: To quickly see the app in action, click "Autofill" to pre-populate the fields and then click "Generate Now" to get AI-powered insights.
2. **Manual Input**: Users can manually input answers to the presented questions, which will guide the AI's suggestions.
3. **Navigate Between Stages**: Once generated, the results for each design thinking stage can be viewed through tabs or by using the 'Next' button.
4. **Download Report**: Go to the "Download Report" tab to generate and download a comprehensive PDF report of your inputs and the AI's suggestions.
5. **Review Inputs**: Users can review their provided inputs in the "Your Input" tab.
6. **Restart**: If needed, users can restart the process by navigating to the "Restart" tab.

## Dependencies

- streamlit
- extra_streamlit_components
- streamlit_option_menu
- fpdf
- langchain
- weaviate
- clarifai

## Setup

To get the app running locally:

1. Clone the repository.
2. Install the dependencies.
3. Run the app using Streamlit.

`streamlit run your_app_filename.py`


## Note

This app makes use of utility functions from various modules (e.g., `utils.pdf`, `utils.clarifai`, `utils.prompts`). Ensure these modules and their respective functions are available in your local setup.

## Feedback

For any feedback, issues, or feature requests, please open an issue in the repository.

