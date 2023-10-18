from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain
from langchain.schema import SystemMessage,HumanMessage
import streamlit as st

class LangchainHandler:
	def __init__(self,key=st.secrets["OPENAI_KEY"]):
		self.schema={
			"properties": {
				"contact_name": {"type": "string"},
				"contact_email": {"type": "string"},
				"contact_phone_number": {"type": "string"},
				"work_experience": {"type": "array", "items": {"type": "object", "properties": {
					"company_name": {"type": "string"},
					"job_title": {"type": "string"},
					"start_date": {"type": "string"},
					"end_date": {"type": "string"}
				}}},
				"degree": {"type": "array", "items": {"type": "object", "properties": {
					"type": {"type": "string"},
					"school/college": {"type": "string"},
					"year": {"type": "string"},
					"grade":{"type":"string"},
					"percentage":{"type":"string"},
					"subject/branch":{"type":"string"}
				}}},
				"projects": {"type": "array", "items": {"type": "object", "properties": {
					"name": {"type": "string"},
					"technologies_used": {"type": "array","items":{"type":"string"}},
					"description": {"type": "string"}
				}}},
				"certificates": {"type": "array", "items": {"type": "object", "properties": {
					"name": {"type": "string"},
					"issued_by": {"type": "string"}
				}}},
				"skills": {"type": "array", "items": {"type": "string"}}
			}
		}

		self.key=key

		self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo",openai_api_key=self.key)

	def get_resume_headers(self,data):
		chain = create_extraction_chain(self.schema, self.llm)
		data=chain.run(data)
		return data