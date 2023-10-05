# <span style="color:rgb(255, 75, 75)">v0.0.6</span>

### General
* Allow usage by multiple users at the same time.
* Allow multiple sessions for each user at the same time.
* Stop agent loop in case of agent changing, conversation resetting and message deletion.
* Disable saving feature for example chat models
* Delete inactive sessions

---
# <span style="color:rgb(255, 75, 75)">v0.0.5</span>
### Agents
- :green[**[+] Summary Agent** ] 

### Tools
* :green[**[+] Summarize Tool:**] Performs document summarization using LLM.
* :green[**[+] File Path Finder:**] locates the file path of locally stored files.

### General
* Cache chat models for faster chat model loading time
---
# <span style="color:rgb(255, 75, 75)">v0.0.4</span>
### Agents
- :green[**[+] Image Chat Agent** ] 

### Tools
* :green[**[+] Image Caption:**] generates descriptive text for images.
* :green[**[+] Image Path Finder:**] locates the file path of locally stored images.
* :green[**[+] Image Object Detection:**] identifies and recognizes objects within an image.
* :green[**[+] Chooch Chat Tool:**] interfaces with the **Chooch API** to facilitate a chat or conversation involving the image

### General
* Parse Images from **Agent Observations**
* Stop agent loop using **Stop Generating** button
* Better chat model selection layout
* Ability to delete chat models
* **Thought Process** for every AI-Generated message with the ability to toggle them on/off
* Memory for each AI response in **Thought Process**
* Choose agents on unsaved chats
* :red[[-] Removed show/hide chat model checkbox on unsaved chats]
---
# <span style="color:rgb(255, 75, 75)">v0.0.3</span>
### General
* Chat model management for testing purposes
    * Assign distinctive names to each chat model.
    * Chat models can be selected from the home page and are sorted by **last_updated** field
    * Define various issues with detailed descriptions for any agent in a chat model.
    * Updates can be applied for model names, conversations and associated issues.
* Indicate the presence of unsaved changes in the chat.
* **New Chat** button to start a new blank chat with the same data
* Express disapproval for messages exhibiting incorrect agent behavior using **👎** button.
* Light red background color applied to disliked messages to make them stand out.
* Added a new URL parameter, ***model_id***, to access any chat model directly
* Ability to delete messages from any starting point
* **Memory** is managed automatically when messages are deleted
* Saved chats preserve **Memory**, ensuring a smooth continuation of conversations.
* Example chat models in changelog for new agents
- :red[[-] Removed trained button in favor of chat models ]
- :red[[-] Thought process for the last AI-Generated message has been removed temporarily]
---
# <span style="color:rgb(255, 75, 75)">v0.0.2</span>
### Agents
- :green[**[+] CSV Agent** ]

### File Parsing 
- :green[**[+] CSV :** ] LOCAL

### General
* **Agent Thoughts** and **Agent Observations** are now integrated into agent output
* Parse **Tables** from **Agent Observations** 
* Parse **Charts** from **Agent Observations**
* Parse **Errors** from **Agent Observations**
* Auto agent selection based on input data
* Agent annotation
* Save agent chat in the same session
* Processing files progress bar
* Preprocessed data via Trained Button
* Reset agent chat
---
# <span style="color:rgb(255, 75, 75)">v0.0.1</span>
### Agents
* :green[**[+] Conversational Retrival Agent** ]

### Tools
- :green[**[+] Vector Store Retriever** ]

### File Parsing
- :green[**[+] PDF :** ] PyPDFLoader ➜ [VECTOR]
- :green[**[+] PNG, JPG, JPEG :** ] Unstructured Image Loader ➜ [VECTOR]
- :green[**[+] DOCX :** ] Docx2Txt ➜ [VECTOR]
- :green[**[+] MP3 :** ] OpenAI Whisper API ➜ [VECTOR]
- :green[**[+] TXT** ] ➜ [VECTOR]

### General
* Thought Process for the last AI-Generated Message
* Parse Final Answer from agent output
