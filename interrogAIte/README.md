# interrogAIte
# Purpose

People who have seen something happen and can give a first-hand description of it are referred to as "eyewitnesses". After an event (disaster, crime, etc.) has occurred, authorities find eyewitnesses to the event and gather their testimony. Often, the process of recording, analyzing and searching through the testimony of eyewitnesses for valuable information is a long and difficult task. Here is where InterrogAIte comes in.

InterrogAIte is an LLM powered tool which automates the process of analyzing eyewitness testimony. The functions performed by InterrogAIte are:

* **Transcription** : The application provides a transcription of the audio recording of the testimony. This transcription is then used for the other features of the app.
* **Summarization** : This features automatically summarizes the given transcription after being provided with the context of the interview. It generates a short summary containing all the key points of the transcription
* **Chat**: The LLM-powered chat answers any questions asked about the transcript by the user. This reduces time spent searching for specific information and conclusions
* **Tools**: The tools section contains an Image Generator. This is especially helpful when the eyewitness is giving a description of another person (say, a suspect in a crime)

The main libraries used in this application are:
* **AssemblyAI**: Used for transcription of the audio file
* **LeMUR (AssemblyAI)**: Used to generate the summary, power the AI chat and extract key information from the transcript which is used to generate the image
* **HuggingFace** : Used to generate the image via a Realistic Vision model


# Examples

For an example, the tool has been pre-loaded with the testimony of two eyewitnesses, who were present at the site of the assassination of U.S. President John F. Kennedy. Charles Givens, was one of the employees at the building from which the shots were fired and one of the last people to interact with the suspect Lee Harvey Oswald before the shooting. Arnold Rowland was one of the witnesses from the plaza where the shooting occurred, and he describes a "different" person he believes he saw in a window on the same floor where Lee Harvey Oswald is believed to have fired the shots from. Credits: LEMMiNO
