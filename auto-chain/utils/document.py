
from itertools import groupby



class DocumentProcessor:
    def __init__(self, documents):
        self.documents = documents

    def group_and_sort(self):
        sorted_documents = sorted(self.documents, key=lambda doc: (doc.metadata['source'], doc.metadata['doc_id']))
        grouped_documents = {}
        
        for source, group in groupby(sorted_documents, key=lambda doc: doc.metadata['source']):
            grouped_documents[source] = list(group)
        
        return grouped_documents

        

# Sample list of Document objects


# Create a DocumentProcessor instance and process the documents
