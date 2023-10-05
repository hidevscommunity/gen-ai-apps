from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain
from langchain.schema import SystemMessage,HumanMessage
from GraphRenderer import *

class LangchainHandler:
	def __init__(self,openai_api_key=st.secrets["OPENAI_API_KEY"]):
		self.llm = ChatOpenAI(
						temperature=0, 
						model="gpt-3.5-turbo",
						openai_api_key=openai_api_key
					)
		self.schema = {
				"properties": {
					"subject_entity": {"type": "string"},
					"relation_type": {"type": "string"},
					"target_entity": {"type": "string"},
				},
				"required": ["subject_entity", "relation_type", "target_entity"],
			}
	def keyword_prompt(self,keywords):
		message=[
			SystemMessage(content=("Provide information for each of the following topic(s) and try to relate the two topic")),
			HumanMessage(content=(keywords))
		]
		data=str(self.llm(message))
		return data
	
	def get_relation_triplets(self,data):
		chain = create_extraction_chain(self.schema,self.llm)
		data=chain.run(data)
		return data

