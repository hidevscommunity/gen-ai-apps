# 🎈 Streamlit + Langchain + Python Example

## Overview of the App

This app showcases a use case where teacher can use gpt through pre-engiennered promts, App generates elementary grade level curriculum through pre-engineered langchain prompts template. all end users(teachers) have to do is to select their teaching grade level and curriculum will be generated. The additional function is to download the curriculum as csv file, 

Tech Architecture.
![Screen Shot 2023-09-11 at 2 03 52 AM](https://github.com/syedabbast/Teachers_GPT/assets/17445744/fc561486-1d40-4d4f-ad9b-c46f87319c79)



#-**About App** <br>
**App Name:** American Elementary School Curriculum Generator <br>
**App Function:** Generate Response through dropdown through backend gpt pre-engineered prompts.<br>
**App Link:** Link https://teachersgpt-chatgpt.streamlit.app/<br>
**GitHub Link:** https://github.com/syedabbast/Teachers_GPT<br>


#**Solution:** The dropdown technique not to give open text to end users and control the results by engineering prompts. 
Note:I will be using this app to teach my students . I could see this app as a potential use case in the educational industry. 
Enterprise Usage: As I am Technology Architect I believe these three libraries can build prompt engineering solutions faster, the one I have created does not demonstrate any database on the backend which would be my next step to use snowflakes database to showcase in-house promt generating results. 

This is a good candidate for the LLM Hackathon by Streamlit IO (Snowflakes), (Please view and vote)

# Demo App

https://teachersgpt-chatgpt.streamlit.app

# Get an OpenAI API key

You can get your own OpenAI API key by following the following instructions:

1. Go to https://platform.openai.com/account/api-keys.
2. Click on the `+ Create new secret key` button.
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.

## Enter the OpenAI API key in Streamlit Community Cloud

To set the OpenAI API key as an environment variable in Streamlit apps, do the following:

1. At the lower right corner, click on `< Manage app` then click on the vertical "..." followed by clicking on `Settings`.
2. This brings the **App settings**, next click on the `Secrets` tab and paste the API key into the text box as follows:

```sh
OPENAI_API_KEY='xxxxxxxxxx'
```
<br><br><br><br><br>
Follow me on Medium and Twitter! <br>
**Syed Abbas** <br>
**Email**tahasyed110@gmail.com<br>
**Twitter:** https://twitter.com/SyedAbbasT<br>
**Medium** https://medium.com/@SyedAbbasT<br>
