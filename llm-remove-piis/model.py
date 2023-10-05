from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
import os
import fitz 


class deidentifier():

    def __init__(self, OPENAI_API_KEY, old_path = "data/original/temp.pdf", new_path = "data/filtered/temp_masked.pdf"):
        self.model = "gpt-3.5-turbo"
        
        os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

        self.old_path = old_path
        self.new_path = new_path

        # document
        self.doc = fitz.open(self.old_path)

        self.template = """You are a data de-identification assistant. Your job is to point out all the personal information from the given text.
    Examples of personal information include:  (full name, maiden name, or any other names by which the individual is known), Contact Information (Addresses, phone numbers, email addresses, and social media profiles),
    Identification Number (Social Security numbers, passport numbers, driver's license numbers, and other government-issued identification numbers),
    Financial Information (Bank account numbers, credit card numbers, and financial records),
    Date of Birth, Health Information (Medical records, health insurance information), Employment information (job titles, employer names, and contact information), Online activities ( IP addresses, usernames, and online behavior such as website browser history),
    Education Information (School names, major), or any other information that you consider as personal. 

    You should be very careful about identifying if the information is personal. If you are not confident about a word or a phrase, then you should include it as personal information because we don't want any information to be leaked.

    You should always respond back by a list of words that you consider as personal information. DO NOT INCLUDE any other words in your response.
    Example response should be:
    ["Joe Biden", "America", "400-923-1093"]
    
    Following are the text, please provide the list of personal information as required:{text}"""

        self.prompt = PromptTemplate(template = self.template, input_variables = ['text'])
        self.llm = OpenAI(model_name = self.model)
        self.chain = LLMChain(llm = self.llm, prompt = self.prompt)

        # self.message = [{"role": "system", "content": self.system_prompt}]

        self.page_count = 0

        self.redact_words = {}

    def add_redact_words(self, page_index, word):
        if page_index not in self.redact_words:
            self.redact_words[page_index] = [word]
        else:
            self.redact_words[page_index].append(word)

    def remove_redact_words(self, page_index, word):
        if word in self.redact_words[page_index]:
            self.redact_words[page_index].remove(word)

    def query(self, text):

        input = {'text': text}
        return self.chain.run(input)
        
    
    def construct_redact_dict(self, page_index, response):
        for token in response:
            if token[0] == '"':
                token = token[1:]
            if token[-1] == '"':
                token = token[:-1]
            self.add_redact_words(page_index, token) 
        
    
    def mask_page(self, page_index, page):

        self.redact_words[page_index].sort(reverse=True, key = len)

        for word in self.redact_words[page_index]:
            rl = page.search_for(word)
            for r in rl:
                page.add_redact_annot(r, fill=(0,0,0))
        page.apply_redactions()


    def pipeline(self, send_query=True):
        if send_query:
            print("Send a query")
            for page_index, page in enumerate(self.doc):
                text = page.get_text()

                # get response from openai
                response = self.query(text)

                # construct redact word dict from the response 
                self.construct_redact_dict(page_index,  response[1:-1].split(", "))

                # mask the pdf based on the redact word dictionary 
                self.mask_page(page_index, page)

                self.page_count = page_index + 1

        else:
            print("We don't send a query")
            for page_index, page in enumerate(self.doc):
                self.mask_page(page_index, page)

        self.doc.save(self.new_path)




# assistant = deidentifier()

# assistant.pipeline()








