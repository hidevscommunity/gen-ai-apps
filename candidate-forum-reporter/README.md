# Candidate Forum Reporter
A Streamlit app focused on local government issues.

Use it to:
* Get a summary of a meeting
* Understand quickly which local issues are being discussed 
* Read a full transcript of the meeting

## Prerequisites
* AssemblyAI API Key: https://www.assemblyai.com/

## Running Locally - Set up 
```bash
# clone the repo
git clone https://github.com/Skylight8177/candidate-forum-reporter.git
cd candidate-forum-reporter

# Rename the secrets file 
# Add your API key to secrets.toml
mv .streamlit/example.toml .streamlit/secrets.toml 

# create the virtual environment
conda create --name streamlit python=3.11
conda activate streamlit

# install the packages
pip install -r requirements.txt
brew install ffmpeg

# test the installation
streamlit hello
# CTRL + C to quit

# run the app
streamlit run app.py
```
