# JoeRAGanApp
Created By: [Preston Goren](https://www.linkedin.com/in/prestongoren/) and [Lucas Werneck](https://www.linkedin.com/in/lucas-werneck/)

[Check out the app here](https://joeraganapp.streamlit.app/)

Presentation: [Video](https://www.youtube.com/watch?v=HGB_zUmIFlM) | [Slides](https://docs.google.com/presentation/d/1lrcUbo9y4kGLIPtPKfgBCw9OE0HE4IV2PiEuraO3OUQ/edit?usp=sharing)

![sample_screenshot](https://github.com/lrwerneck/JoeRAGanApp/assets/80135054/de78c974-67c5-4e85-b224-4900a0b01d30)


## About
Welcome to The Joe RAG-an Experience! This chatbot has access to a few episode transcripts of the Joe Rogan podcast and can answer questions about the discussions that occurred within those episodes. This project attempts to improve upon the traditional RAG (Retrieval Augmented Generation) implementation by chunking the episode transcripts dynamically based on semantic context, as well as enriching these chunks with tags describing the topics discussed within the chunk.

## Smart Chunking
One issue commonly encountered with traditional chunking methods is that they can often cut off relevant context as they denote chunk boundaries with arbitrary word or token counts. Although this is partially solved by adding overlap between chunks, we thought that perhaps this could be made even better by having a LLM determine where the chunk boundaries should be placed. To do this we first use a standard text splitter to create “default” chunks, then prompt a LLM to adjust these chunks in order to retain semantic context and avoid cutting off a chunk in the middle of a thought or sentence. This way, our chunks are “intelligently” selected in order to optimally retain context. 

## Information Enrichment
Another improvement we wanted to try on the traditional RAG implementation was information enrichment. The idea is to add another form of metric to retrieve context based on, rather than relying purely on a vector similarity search based on the user query. When performing the chunking process, we additionally have a LLM assign topic descriptions to each chunk. This comes in the form of a couple ~sentence long tags describing what is discussed within the chunk. When attempting to retrieve context to help answer a user query, we first search through the topic descriptions to grab relevant topics, then use those topics to help narrow down the similarity search for the embedded chunks. The goal behind this technique was to improve retrieval of relevant context and limit retrieval of irrelevant context. 

### Limitations:
Often relies on a well-formulated question from the user

Extra Cost / Complexity

Consistency / Reliability

### Future work:
Evaluation (benchmark vs standard methodology)

CoT prompting instead of single prompt

Fine-tune LLM with intelligent chunking prompt

Begin search at the episode-level

Incorporate more episodes

Further prompt engineering

