# llm-remove-piis
a streamlit app, utilize openai API and langchain to remove personal, sensitive information from a pdf document.

This project comes from a real user case. In a world data becomes more and more important, it's our responsibility to provide a 100% secure and trusted llm application. Normally the data masking and de-identification process involves a huge amount of human labor work, but our app provides a possibility to utilize the power of llms to automate the de-identification process.

![Project Structure](./image/project.png)

 - Steramlit Cloud Demo: https://llm-remove-piis-demo.streamlit.app/
 - Source Code: https://github.com/padshandsome/llm-remove-piis

## Instructions 
- Enter your personal OpenAI key.
- Upload the pdf file you want to de-identify.
- Modify the redact word list returned from OpenAI.
- Visualize and export the masked pdf file.

 ## Demo



 ## Run the app locally

Clone the git repository to local.
 ```
 git clone https://github.com/padshandsome/llm-remove-piis.git
 ```
 Install dependencies
 ```
 pip install -r requirements.txt
 ```
 Run the app locally
 ```
 streamlit run app.py
 ```




 


