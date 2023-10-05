# OSChat

Open source chatbot that helps user in their experience

The OS Chat project aims to develop a chatbot using OpenAI's GPT (Generative Pre-trained Transformer) language model
and a vector database. The goal is to create a chatbot that can interact with users and provide responses based on
natural language understanding and generation.

The chatbot's functionality will be specifically tailored to handle conversations related to
documents`(PDF, markdowns, html)`. Users will
be able to ask questions, seek information, or request assistance regarding docs-related topics. The chatbot will
utilize
the capabilities of GPT to comprehend user inputs and generate informative and contextually appropriate responses.

## Updates...

### Hackathon Submission: - [DevPost](https://devpost.com/software/oschat)

### Demo: [Video](https://youtu.be/_jU1oCfH6G8)

## Prerequisites

To run the OS-Chat project, you need to have the following prerequisites:

- Python (version 3.10 or higher) installed on your machine.
- The necessary Python packages and dependencies installed. You can find the required packages in the `requirements.txt`
  file of the project repository.

## How to Run with Python3 and `make`

To run the OS-Chat project using `Python` and `make`, follow these steps:

```shell
   git clone https://github.com/AIFame/os-chat os-chat
   cd os-chat
   make install
   make run
```

## How to Run via Docker

To run the OS-Chat project using `Docker`, follow these steps:

```shell
docker build -t os-chat .
docker run -p 8501:8501 os-chat
```

> For developers,
> I recommend <br>
> ```docker run -it -e "mode=development" -p 8501:8501 os-chat``` <br>
> playaround and test your code!


> That's it! You can now use the OS-Chat chatbot to have conversations related to your documentations.

I hope this helps! Raise issues to clarify your doubts and notify bugs.

## How to Contribute

We welcome contributions from the community! To get started, follow these steps:

1. Fork the repository on GitHub.
2. Clone your fork of the repository to your local machine.
3. Create a new branch for your changes: `git checkout -b <your-username>/your-feature-branch`.
4. Make your changes and commit them to your branch.
5. Push your changes to your fork on GitHub.
6. Open a pull request from your fork's branch to the main repository.

Please make sure to follow the [Code of Conduct](./CODE_OF_CONDUCT.md) when contributing to this project.
