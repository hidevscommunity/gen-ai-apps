import weaviate
import time
import streamlit as st
class WeaviateHandler:
    def __init__(self,weaviatekey=st.secrets["WEAVIATE_KEY"],openaikey=st.secrets["OPENAI_KEY"]):
        self.auth_config = weaviate.AuthApiKey(api_key=weaviatekey)
        self.client = weaviate.Client(
            url="https://questionsdb-y4chqhq5.weaviate.network",
            auth_client_secret=self.auth_config,
            additional_headers={
                "X-OpenAI-Api-Key": openaikey,
            }
        )
    def get_questions(self,data):

        questions={
            "skills":[],
            "work_experience":[],
            "projects":[],
            "certificates":[],
        }
        answers={
            "skills":[],
            "work_experience":[],
            "projects":[],
            "certificates":[],
        }
        company={
            "skills":[],
            "work_experience":[],
            "projects":[],
            "certificates":[],
        }
        role={
            "skills":[],
            "work_experience":[],
            "projects":[],
            "certificates":[],
        }
        question_topics = set()
        
        def fetch_questions_from_concept(concept, category):
            try:
                response = (
                    self.client.query
                    .get("Questionnew", ["question", "answer", "company", "role"])
                    .with_near_text({"concepts": concept})
                    .with_limit(1)
                )
                response = response.do()

                if response:
                    for k in response["data"]["Get"]["Questionnew"]:
                        questions[category].append(k["question"])
                        answers[category].append(k["answer"])
                        company[category].append(k["company"])
                        role[category].append(k["role"])
                    question_topics.add(concept)
                time.sleep(20)
            except Exception as e:
                st.error(f"An error occurred while fetching questions: {str(e)} Probably your OpenAI API Rate limit exceeded!!")

        if "work_experience" in data:
            with st.spinner("Fetching questions based on your work experience..."):
                for i in data["work_experience"]:
                    concept = i.get("job_title", "")
                    if concept and concept not in question_topics:
                        fetch_questions_from_concept(concept, "work_experience")

        if "projects" in data:
            with st.spinner("Fetching questions based on your projects..."):
                for i in data["projects"]:
                    if "technologies_used" in i:
                        for concept in i["technologies_used"]:
                            if concept and concept not in question_topics:
                                fetch_questions_from_concept(concept, "projects")

        if "certificates" in data:
            with st.spinner("Fetching questions based on your certificates..."):
                for i in data["certificates"]:
                    concept = i.get("name", "")
                    if concept and concept not in question_topics:
                        fetch_questions_from_concept(concept, "certificates")

        if "skills" in data:
            with st.spinner("Fetching questions based on your skills..."):
                for i in data["skills"]:
                    if i and i not in question_topics:
                        fetch_questions_from_concept(i, "skills")

        return questions, answers, company, role
