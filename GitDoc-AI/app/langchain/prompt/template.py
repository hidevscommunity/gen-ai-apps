from langchain import PromptTemplate

def question_answer_prompt():
    template = """You are a GitDoc AI, who is expert AI assistant built to answer questions and provides information over the following pieces of documentation as context to answer the question at the end. 
    Do not answer the question if its out of context provided.
    Always be polite and respectful, even if the user is not. Try to help, even if the user is not clear or is giving incorrect information.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    context:
    ```
    {context}
    ```
           
    {question}
    Answer in markdown:"""
   
    prompt = PromptTemplate(input_variables=["context", "question"], template=template)
    return prompt

def summary_prompt():
    template = """Write a concise summary of following conversation:
    {input}

    CONCISE SUMMARY WITH KEY ENTITIES:"""

    prompt = template
    return prompt
