# documentation for CharacterTextSplitter:

### https://python.langchain.com/en/latest/modules/indexes/text_splitters/examples/character_text_splitter.html

### embedding using openAI embedding. Warn: This will cost you money

### embedding using instructor-xl with your local machine for free you can find more details at:

### https://huggingface.co/hkunlp/instructor-xl This code snippet demo how to use other model for text embedding. Will

### not use this for my project. But will keep this here for reference. def get_vectorstore(text_chunks): embeddings =

### HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl") vectorstore = FAISS.from_texts(texts=text_chunks,

### embedding=embeddings) return vectorstore
