import openai
import streamlit as st
from langchain.agents import create_spark_sql_agent
from langchain.agents.agent_toolkits import SparkSQLToolkit
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.llms.openai import OpenAI
from langchain.utilities import SparkSQL
from pyspark.sql import SparkSession
import json

openai.proxy="http://127.0.0.1:1087"

st.set_page_config(page_title="Chat With SparkSql")
st.title("🚀 SparkSQL AI Assistant")

# User inputs
metastore_uri = st.sidebar.text_input(
    label="hive metastore URI", placeholder="thrift://my-hive-metastore:9083"
)

database = st.sidebar.text_input(
    label="hive database", placeholder="default"
)


hadoop_config = st.sidebar.text_area(label="️Hadoop Config ⚙️「Optional」️",
                                     placeholder='''{"defaultFS": "hdfs://nameserver1"}''')

st.sidebar.markdown("---")

openai_api_key = st.sidebar.text_input(
    label="OpenAI API Key",
    type="password",
)

# Check user inputs
if not metastore_uri:
    st.info("Please enter hive metastore URI to connect️")
    st.stop()

if not database:
    st.info("Please enter hive database")
    st.stop()


if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()

# Setup agent
llm = OpenAI(openai_api_key=openai_api_key, temperature=0, streaming=True, model_name="gpt-4")


@st.cache_resource(ttl="2h")
def configure_spark_session(metastore_uri, database, hadoopConfig):
    sparkBuilder = SparkSession.builder.master("local[*]") \
        .config("spark.sql.catalogImplementation", "hive") \
        .config("spark.hadoop.hive.metastore.uris", metastore_uri) \

    if hadoopConfig != "":
        hadoopConf = json.loads(hadoopConfig)
        for key, value in hadoopConf.items():
            sparkBuilder.config(key, value)
    sparkSession = sparkBuilder.getOrCreate()
    return SparkSQL(sparkSession, schema=database)


db = configure_spark_session(metastore_uri, database, hadoop_config)

toolkit = SparkSQLToolkit(db=db, llm=llm)

agent = create_spark_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder="Ask me anything about spark sql")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
