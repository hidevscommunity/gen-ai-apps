<div align="center">
<h1 align="center">
💊
TabLit
</h1>



</div>

---

## 📒 Table of Contents
- [📒 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [🧩 Modules](#-modules)
- [🚀 Getting Started](#-getting-started)

---

## 📍 Overview

- [TabLit](https://tablit.streamlit.app/) is a Streamlit application that provides a user interface for chatting with Tabular Data using a LLM. 
- Its core functionalities include setting up the chat interface, integrating with the language model for generating responses, pre-processing and formatting data for ingestion by the model, allowing users to explore data, displaying intermediate language model steps, and saving chat history. 
- The project aims to streamline user interaction with the language model, enabling them to chat, explore data, and provide feedback to improve model performance.
---


## 🧩 Modules

<details closed><summary>Root</summary>

| File                                                                      | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---                                                                       | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| [TabLit.py](https://github.com/Prajwalsrinvas/Tablit/blob/main/TabLit.py) | The code provided is a Streamlit application that allows users to chat with tabular data using a language model. The application provides a user interface where the user can upload or crawl web data, explore the data, and then engage in a conversation with the language model.The core functionalities of the code include:-Setting up the Streamlit interface with a sidebar for user inputs and displaying the chat interface.-Handling user input and displaying previous chat messages.-Integrating with the language model to generate responses to user queries.-Pre-processing and formatting data for ingestion by the language model.-Allowing users to explore the uploaded or crawled data in a tabular format.-Generating and displaying intermediate steps of the language model while processing user queries.-Saving the chat history and providing a link to the LangSmith trace.-Allowing users to provide feedback on the language model's responses.Overall, the code provides a streamlined interface for users to interact with the language model, allowing them to chat, explore data, and provide feedback to improve the model's performance. |
| [utils.py](https://github.com/Prajwalsrinvas/Tablit/blob/main/utils.py)   | This code provides several core functionalities:1. It creates a zip file containing selected files from a specified directory and allows users to download it.2. It generates a unique session ID using UUID.3. It deletes empty subfolders within a specified folder.4. It loads data from uploaded files in different formats (e.g., csv, excel) using pandas.5. It obtains credentials for a Nimble service based on secrets provided in the Streamlit app.6. It reads a configuration file in JSON format.7. It searches for data on a specified platform (e.g., ecommerce, SERP) using a search keyword.8. It saves search results in a CSV file and returns a DataFrame object.9. It saves the chat conversation in a JSON file.Overall, the code supports file manipulation, data processing, external API communication, and persistence of data.                                                                                                                                                                                                                                              |

</details>

<details closed><summary>Pages</summary>

| File                                                                                  | Summary                                                                                                                                                                                                    |
| ---                                                                                   | ---                                                                                                                                                                                                        |
| [3_Gallery.py](https://github.com/Prajwalsrinvas/Tablit/blob/main/pages/3_Gallery.py) | This code creates a Streamlit webpage for a gallery of images. It imports the necessary libraries, sets up the page layout, reads the gallery configuration, and creates a carousel to display the images. |
| [2_ReadMe.py](https://github.com/Prajwalsrinvas/Tablit/blob/main/pages/2_ReadMe.py)   | This code uses Streamlit to create a web page with a collapsed sidebar and a "ReadMe" title icon.                    |

</details>

---

## 🚀 Getting Started

### 📦 Installation

1. Clone the Tablit repository:
```sh
git clone https://github.com/Prajwalsrinvas/Tablit
```

2. Change to the project directory:
```sh
cd Tablit
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

3. Copy secrets file and make required changes:
```sh
cp .streamlit\secrets_example.toml .streamlit\secrets.toml
```

### 🎮 Using Tablit

```sh
streamlit run TabLit.py
```

