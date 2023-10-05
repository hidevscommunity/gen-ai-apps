import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import LLMChain, RetrievalQA
from nemoguardrails import LLMRails, RailsConfig
from app.langchain.models import load_chat_model
from app.langchain.prompt.template import summary_prompt, question_answer_prompt


def initialise_qa_chain():
    if 'summary_memory' not in st.session_state:
        st.session_state['summary_memory'] = None

    if "qa_chain" not in st.session_state:
        search_index = st.session_state['knowledge_base']
        llm = load_chat_model()
        QA_PROMPT = question_answer_prompt()
        load_qa = load_qa_chain(llm=llm, chain_type="stuff", prompt=QA_PROMPT, verbose=True)
        qa_chain = RetrievalQA(combine_documents_chain=load_qa, retriever=search_index.as_retriever(), return_source_documents=True, verbose=True)  
        st.session_state.qa_chain = qa_chain

    if st.session_state["is_guardrail"] and "guardrail_qa_chain" not in st.session_state:
        search_index = st.session_state['knowledge_base']
        config = RailsConfig.from_path("app/config")
        app = LLMRails(config)
        QA_PROMPT = question_answer_prompt()
        chain_type_kwargs = {"prompt": QA_PROMPT}
        qa_chain = RetrievalQA.from_chain_type(llm=app.llm, chain_type="stuff", retriever=search_index.as_retriever(), chain_type_kwargs=chain_type_kwargs, return_source_documents=True, verbose=True)  
        app.register_action(qa_chain, name="qa_chain")
        st.session_state.guardrail_qa_chain = app

    if "summary_chain" not in st.session_state:
        SUMMARY_PROMPT = summary_prompt()
        llm = load_chat_model()
        summary_chain = LLMChain.from_string(llm=llm, template=SUMMARY_PROMPT)
        st.session_state.summary_chain = summary_chain


def qa_chain(message, runnable_config):
    initialise_qa_chain()
    query = message
    if st.session_state['memory'] and st.session_state['summary_memory']:
        query = "\nConversation Summary: " + st.session_state['summary_memory']  + "\nQuestion: " + message 

    source_document = st.session_state['knowledge_base'].similarity_search_with_score(query)
    
    if st.session_state['is_guardrail']:
        ai_response = st.session_state.guardrail_qa_chain.generate(query)
    else:
        ai_response = st.session_state.qa_chain.invoke(query, config=runnable_config)
        ai_response = ai_response['result']

    if st.session_state['memory']:
        summary = "\nUser: " + message + "\nAI: " + ai_response
        if st.session_state['summary_memory']:
            summary = "\nConversation Summary: " + st.session_state['summary_memory']  + "\nQuestion: " + message + "\nAI: " + ai_response
        st.session_state['summary_memory'] = st.session_state.summary_chain.predict(input=summary)

    return ai_response, source_document
