from langchain.chains.llm import LLMChain
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
import streamlit as st
import string
import base64
import zlib
import os

maketrans = bytes.maketrans
plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
base64_alphabet   = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
b64_to_plantuml = maketrans(base64_alphabet.encode('utf-8'), plantuml_alphabet.encode('utf-8'))
plantuml_to_b64 = maketrans(plantuml_alphabet.encode('utf-8'), base64_alphabet.encode('utf-8'))

st.set_page_config(
    page_title="TEQ AI - DB Schema generator",
    layout="wide"
)

with st.sidebar:
  st.image(image ="https://teqnological.asia/images/companyLogo.webp", width=240)
  "Website: [Teqnological Asia](https://teqnological.asia)"
  "Email: ai-team@teqnological.asia"
  st.divider()
  "This chatbot is here to assist you in creating a database schema. You can review the diagram as we chat, and feel free to request updates to the schema, such as adding tables, incorporating new columns, modifying existing columns, or any other changes you need. Your feedback is highly appreciated!"
  "[Check-out video demo here!](https://www.youtube.com/watch?v=R4EjtUjqUs8)"
  database = st.selectbox("Database you use:",('MySql','Postgres'))
  btn_reset = st.button("RESTART")
  if btn_reset:
    st.session_state["messages"] = [{"role": "assistant", "content": "How may I assist you with your database design?"}]
    st.session_state["last_schema"] = ""
  st.divider()

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None and "OPENAI_API_KEY" in st.secrets.keys(): 
  openai_api_key = st.secrets["OPENAI_API_KEY"]
  
if openai_api_key is None:
  openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
  if not openai_api_key:
      st.info("Please add your OpenAI API key to continue.")
      st.stop()

llm = ChatOpenAI(model="gpt-3.5-turbo-16k", openai_api_key=openai_api_key, temperature=0, streaming=False)

def dbml_decode(str):
    return base64.urlsafe_b64encode(zlib.compress(str.encode('utf-8'), 9)).decode('ascii')

def get_history(messages):
  resp = ""
  for msg in messages:
    resp = msg["content"] + "." if msg["role"] == "assistant" else ""
  return resp

def process_response(msg):
  start_uml = msg.find("@startuml")
  end_uml = msg.find("@enduml") + len("@enduml")
  uml = ""
  content = msg
  if start_uml != -1 and end_uml != -1:
    uml = msg[start_uml: end_uml]
    start_uml = msg.find("PlantUML:")
    content = msg[0:start_uml]
  return content, uml

template_promting = """
Act as a database engineer. You'll only respond to me SQL schema code that I can use in {database} database. I will describe what I want in plain English and you will respond with the database schema which I can use to create the database. This is a relational database so you should de-normalise the tables and add relationships where appropriate.

You extend this base schema:
{history}

Do not write any explanations. If you don't know the answer, just say that you don't know, don't try to make up an answer.
You ALWAY answer as following format:

```sql
-- table name
CREATE TABLE `table` (
  `id` INT AUTO_INCREMENT NOT NULL, -- important
  /* other fields and definations */
);
```
"""

user_prompting = "{message}. You update Schema and response full Schema. You DO NOT use Alter table. You DO NOT write explanations. You DO NOT write the updated, write full schema please."

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            template_promting
        ),
        HumanMessagePromptTemplate.from_template(user_prompting)
    ]
)
# Notice that we `return_messages=True` to fit into the MessagesPlaceholder
# Notice that `"chat_history"` aligns with the MessagesPlaceholder name.
# memory = ConversationBufferMemory(memory_key="history", input_key="database")
conversation = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True
)

dbml_template_promting= """
Convert the SQL schema
```
{sql}
```
to dbml ( Database Markup Language) as format below
```
//DBML here
Table users {{
  id int [primary key]
  ...
}}
Table country {{
 code int
 name varchar
 ...
}}
// relationships at the bottom
Ref: countries.code < users.country;
```
Important notes:
- DO NOT add foreign key in tables
- DO NOT add indexes in DBML
- In case of `PRIMARY KEY (column_a,column_b)`, ignored them completely.
- In case of field like `decimal(8, 6)`, you should write `decimal`
- Extract relationships from SQL schema then add in the comment 'add the relationship at the bottom'
- You just show the dbml source, do not explain more
"""
dbml_prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            dbml_template_promting
        ),
    ]
)
unml_conversation = LLMChain(
    llm=llm,
    prompt=dbml_prompt,
    verbose=True
)
# set database type
# database = "Mysql 8.0"

# st.markdown(uml_code)

# init messages
if "messages" not in st.session_state:
  st.session_state["messages"] = [{"role": "assistant", "content": "How may I assist you with your database design?"}]
  st.session_state["last_schema"] = ""

prompt = st.chat_input()
# render messages chat
for msg in st.session_state["messages"]:
  with st.chat_message(msg["role"]):
    st.write(msg["content"])
    if msg["role"] == "assistant" and len(st.session_state["messages"]) == 1:
      bt1 = st.button("create database to manage a bookstore")
      bt2 = st.button("create table users, allow user to register and login")
      bt3 = st.button("create database has users, comments, posts")
      st.write("Or write your idea in message box...")
      if bt1:
        prompt = "create database to manage a bookstore"
      elif bt2:
        prompt = "create table users, allow user to register and login"
      elif bt3:
        prompt = "create database has users, comments, posts"

# handle input of user
if prompt:
  st.chat_message("user").write(prompt)
  with st.chat_message("assistant"):
    st_callback = StreamlitCallbackHandler(st.empty())

    # response = chain.run(database=database,request=prompt,history=get_history(st.session_state["messages"]))
    with st.spinner("Thinking...."):
      response = conversation.run(message=prompt,database=database,history=st.session_state["last_schema"])

    st.session_state.messages.append({"role": "user", "content": prompt})
    # content, uml = process_response(response)
    content = response
    st.write(content)
    st.session_state["last_schema"] = content
    # if img := render_image(response):
    #   st.image(img.content,caption="Diagram is from plantuml.com")
    st.session_state.messages.append({"role": "assistant", "content": content})
    
    with st.spinner("Generating diagram...."):
      with st.expander("See diagram"):
        # convert content to plantuml
        try:
          sql = content.split('```')[1]
          if sql:
            uml_response = unml_conversation.run(sql=sql)
            st.image(image='https://kroki.io/dbml/svg/{0}'.format(dbml_decode(uml_response)),width=560)
        except:
          st.write("Something wrong! We'll try again in next request")
          pass 

    st.download_button(
      label="Download SQL file",
      data=response.replace("```sql","").replace("```",""),
      file_name='my-db.sql',
      mime='text/sql',
    )
    st.download_button(
      label="Download DBML file",
      data=uml_response,
      file_name='my-db.dbml',
      mime='text/dbml',
    )
    st.caption("You can message me to add more tables, create new columns in existing tables, modify column types, or make changes to relationships.")