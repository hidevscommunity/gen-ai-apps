SYSTEM_TEMPLATE = '''Answer all question using the provided transcript as source. If there is no trascript, the user may ask you whether you can answer the question based on the existing information. If the transcript does not contain any specific information, answer with "No information available in the source documents."
Do not give just short answers, but try to incorporate the information from all trancrtipts to give a complete answer and additonal information if possible.
Do not forget to add the time stamp as reference to the answer.

Answer the question using the time stamp as reference and the following format:
answer_part [time stamp] anser_part .... answer_part [time stamp] etc...
example answer: "The company is based in San Francisco. [2496.52] The company was founded in 2015. [3025.12] There are 100 employees."

It is very important to have AFTER each claim a time stamp as reference!!! Do not answer based on your general knowledge!!!
Do not add Transcript 1, Transcript 2, etc. to your answer, but the time stamps as described above. e.g. [2496.52] or [3025.12] etc.
'''

INITIAL_TEMPLATE = """Transcripts:

{source_documents}

------------

Question:

{question}"""




NEW_SEARCH_REQUIRED_TEMPLATE = '''Question: {question}


Can you answer the question above based on existing information from our conversation? If you can answer it, just say "Yes" or "No" only, no addtioninal output is required and do not answer the question!

Yes or No?:
'''


DOCUMENT_TEMPLATE = """Transcript {document_number}:
{document_content}"""

def get_initial_template(source_documents, question):
    doc_msg = "\n\n".join([DOCUMENT_TEMPLATE.format(document_number=i+1, document_content=doc.page_content) for i, doc in enumerate(source_documents)])
    return INITIAL_TEMPLATE.format(source_documents=doc_msg, question=question)


def get_new_search_required_template(question):
    return NEW_SEARCH_REQUIRED_TEMPLATE.format(question=question)

def get_system_template():
    return SYSTEM_TEMPLATE



