# TalkToMe 🌍✨

Welcome to TalkToMe, your personal language learning assistant! With this tool, you can practice speaking, discuss articles, and get instant feedback in various languages. Currently supported languages include German, French, Italian, Spanish, and English. The best part? You can practice in real-time, without needing a partner!
The app is deployed at:
https://talktomelanguagelearning.streamlit.app/

![TalkToMe Screenshot](header.png)  

## About and Rationale for development
### Contemporary language learning for a digital world
In the contemporary educational landscape, where digital transformation is becoming the new norm, there exists a palpable gap between traditional instructional methodologies and the potential of cutting-edge technologies. One of the most promising bridges for this divide in the realm of language education is Machine Learning (ML). This app aims to explore the transformative capacity of ML to evolve traditional language learning materials into dynamic, responsive, and tailored educational experiences.

While the shift to online platforms has been substantial, many instructional materials merely mirror their analog counterparts, failing to harness the digital medium's true potential. However, with ML, we can breathe life into these static resources, making them adaptive to students' individual needs and responsive to their progress. This not only provides a richer learning experience but also ensures that each learner's unique challenges and strengths are addressed.

This app addresses students' need to practice conversation in their target language and provides a non-threatening experience. Students can choose if they want to receive suggestions for grammar improvements, or if they want to just immerse themseslves in their target language. This

The app aims to emulate my own language teaching practice and aims to help students prepare for exams by allowing them to customise their practice. They can add an article or other text they want to practice talking about and practice specific vocabulary. The app keeps track of the student's practice goal and displays them as visualisations. The app also displays how many words the student's utterances have as well as the total word count. This addresses a common issue in spoken exams that students find it difficult to speak enough to showcase their language abilities.

Traditional: Fixed dialogues or conversation starters.
ML Transformation: Chatbots that can hold a conversation in the target language. Students interact with the chatbot, and the system adapts the conversation based on student responses, ensuring it remains at an appropriate level of difficulty.



## Features

- **Real-time Language Practice**: No need for a language partner.
- **Instant Feedback**: Get immediate feedback on your pronunciation, grammar, and usage.
- **Custom Vocabulary Tracker**: Add specific vocabulary you want to practice and track its usage during conversations.
- **Text & Voice Output**: Choose how you want to receive feedback – text, voice, or both!
- **Support for Multiple Languages**: Practice German, French, Italian, Spanish, and English.

## How to Run Locally

1. Clone this repository:

```bash
git https://github.com/GeriNZ/talktome
cd path_to_the_cloned_directory
```

## Installation and Setup

1. **Install the requirements using pipenv:**
```bash
pipenv install
```
Note: you need an **AssemblyAi** and an **OpenAI** API key to run this app locally.
Please create a config.py file and add your API keys. Make sure to uncomment the relevant lines in the code to make sure it runs locally correctly.

2. **Activate the virtual environment:**
```bash
pipenv shell
```
3. **Run the streamlit app:**
```bash
streamlit run 1_🎤_talktome.py
```
## Instructions & Tips

### How to Use:

1. **Select** your target language, proficiency level, and the kind of conversation you want (informal, formal, etc.).
2. If you have an **article or text** you want to discuss, paste it in the provided text box.
3. **Add specific vocabulary** you want to practice to the vocabulary list. The tracker will count how often you use these words.
4. **Record** your voice by pressing the microphone button, then converse freely!
5. Await the transcription and receive an **instant response** from the virtual language assistant.

### Tips for the Best Experience:

- Ensure you're in a **quiet environment**.
- Speak **clearly and at a moderate pace**.
- Use **news articles, stories, or study materials** as discussion topics.
- **Experiment and practice** as much as possible for the best results!

## Contribute

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcomed.

## Feedback

If you have any feedback or issues, please open an issue.

## License

This project is open-source and available under the MIT License.
