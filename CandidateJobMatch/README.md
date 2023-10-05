<div align="center">

# Candidate Job Match

### A Simple App using LLM to determine if a job resume matches the job profile. 

</div>

<br>

## How does it work?

</div>

The app will upload the resume, load it into llama index as knowledge base and then use LLM to query based on the Job Title and Company Name. 

To improve the accuracy, the app will first generate a detailed job profile using LLM and then match the resume with job profile. 

To save cost, the job profile is also saved so that it won't need to repeatedly generate the same profile.

It's currently using the 'davinci-txt-003' model. 

<div align="center">

## How to install

</div>

Follow these steps to set up the environment and run the application.

1. clone the repository

2. Create and activate a Python Virtual Environment and then install the requirement.txt modules.

3. Run "streamlit run app.py"

## Demo

https://github.com/iampgzp/CandidateJobMatch/assets/5464549/770d9052-dc7c-4da2-af43-fa6cc4ea0795

