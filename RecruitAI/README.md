<div align="center">
  <img src="https://github.com/ramoonmedeiro/RecruitAI/assets/102380417/ca30c3f7-d7de-412a-9e2d-534fbc31b3b9" width="450px" />
</div>


# Introduction

RecruitAI is a powerful and innovative PDF resume analysis tool designed to simplify and streamline the candidate screening process. With cutting-edge artificial intelligence and an intuitive interface, RecruitAI lets you identify ideal candidates efficiently and accurately.

# How to use?

The central idea of ​​RecruitAI is to analyze resumes in relation to a certain job opening.

We know that CVs are often in TXT format. RecruitAI has a tab to transform your .TXT file into .PDF, which is the file type accepted by the tool.

After transforming your files into PDF. It's time to see the coolest part, which is the analyzer.

By clicking on the "Analysis" tab, you will be moved to a page where you can upload a PDF file representing the job description or vacancy and you can upload another PDF file which will be the participant's CV file.

Then just click on analyze and BOOM, a pdf will be generated for you containing a brief summary of the candidate, highlighting some qualities, then there is a step where a score will be given for each important characteristic for the vacancy and finally a general score for the candidate.

# Where to use?

You can test it now at the <a href="https://recruitai.streamlit.app/" target="_blank">link</a>

But you can also use it locally. Regardless of the methods below, you must clone this repository:

```
$ git clone https://github.com/ramoonmedeiro/RecruitAI.git
```

## Via poetry

You need first install poetry:
```
$ pip install poetry
```
Then, you need follow the following steps:

```
$ cd RecruitAI/
$ poetry shell
$ poetry install
```

With this, all dependencies were installed. Now you just need to upload the server locally:

```
$ cd webapp/
$ streamlit run app.py
```

The application will be running on your localhost (http://localhost:8501/).

## Via virtualenv and derivatives

You can use the virtual environment of your choice (mkvirtualenv, pipenv, etc).
I will use venv here.

First you will create a virtual environment and must install the project dependencies:

```
$ cd RecruitAI/webapp/
$ python3 -m venv <name-of-your-virtual-env>
$ source <name-of-your-virtual-env>/bin/activate
$ pip3 install -r requirements.txt
```

Then just run the streamlit server:
```
$ cd webapp/
$ streamlit run app.py
```

The application will be running on your localhost (http://localhost:8501/).

## Via docker

You can also run the application docker locally.

```
$ cd RecruitAI/
$ docker build . -t recuritai:1.0
$ docker container run -d -p 8501:8501 recuritai:1.0
```

The application will be running on your localhost (http://localhost:8501/).

# Final considerations

I'm always looking for new challenges and i'm creating this project to help people understand how to insert GenAI in different fields of application. I created this project also with the intention of participating in the streamlit hackathon about LLMs.

If you want to know more about me, please visit my <a href="https://www.linkedin.com/in/ramon-medeiro-767722246/" target="_blank">LinkedIn</a>.
