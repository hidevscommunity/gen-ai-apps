# ClipInsight 🎥

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A game-changing web application that transforms the way you experience online video content. 

## Table of Contents

- [About the Project](#about-the-project)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [OctoberFest](#WellTestedAI-OctoberFest)

## About The Project

https://github.com/Sahil-kachhap/ClipInsight/assets/54017876/4b1421df-61bf-42e6-abdf-e7fdf97d4f99

**ClipInsight** is the result of a creative whirlwind during **LLM Hackathon by Streamlit** and **Generative AI hackathon by Peerlist**, where we set out to tackle the frustration of navigating through lengthy video content on platforms like YouTube. Our mission was to make video content more accessible, interactive, and time-efficient for users from all walks of life.

**Why?** Because we believe that knowledge should be easily accessible and engaging for everyone.

## Key Features

- 📋 **Text-Based Summaries with Timestamps**: Our app analyzes videos and generates concise summaries of key moments, complete with timestamps. No more endless scrolling!

- 💬 **Real-Time Chat**: Engage in dynamic discussions while interacting with our AI assistant. Ask questions and share insights.

## Tech Stack
1. **Python**
2. **Streamlit**
3. **Langchain**
4. **AssemblyAI**
5. **Replicate**
6. **Model Used: LLama2-70B**

## Getting Started

To get started with ClipInsight, follow these simple steps:
1. **Fork this repository**
2. **Clone the repository**: `git clone https://github.com/yourusername/your-repo.git`

3. **Install dependencies**: `pip install -r requirements.txt`

4. **Run the app**: `streamlit run app.py`

## Contributing

We welcome contributions from the community. Whether it's code, design, or ideas, your input is valuable.

## WellTestedAI OctoberFest 
I have added 2 unit tests described below :-
1. **download_video_test.py** - this unit test tests the download_video() method which actually extracts audio from a youtube video url.
2. **split_transcript_test.py** - this unit test tests the split_transcript() method which is a utility method in itself and helps in breaking a huge file of text into several chunks.

- To Run the test file: `python -m unittest <file_name>.py`

Checkout this [Commit](https://github.com/Sahil-kachhap/ClipInsight/commit/48dd74c640afdb9ac1e2ff43865278cdafd45849) for more details.
