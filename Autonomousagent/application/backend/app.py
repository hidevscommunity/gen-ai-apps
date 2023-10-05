import os
from flask import Flask, jsonify, request
from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from email.message import EmailMessage
import ssl
import smtplib
from langchain.chat_models import ChatOpenAI, ChatAnthropic
import faiss
from agent import AutoGPT
from langchain.vectorstores import FAISS
from typing import Optional

from langchain import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from pydantic import BaseModel, Field
from flask_cors import CORS

from langchain.docstore import InMemoryDocstore
from langchain.vectorstores.faiss import FAISS


app = Flask(__name__)
CORS(app)


def send_email(email_receiver, subject, body):
    email_sender = os.environ.get(
        "EMAIL_SENDER"
    )  # Retrieve sender from environment variable
    email_password = os.environ.get(
        "EMAIL_PASSWORD"
    )  # Retrieve password from environment variable

    if email_sender is None or email_password is None:
        raise ValueError(
            "EMAIL_SENDER and EMAIL_PASSWORD environment variables must be set"
        )

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


@app.errorhandler(Exception)
def handle_error(error):
    response = {"status": "error", "message": str(error)}
    return jsonify(response), 500


@app.route("/support", methods=["POST"])
def handle_support_request():
    try:
        customer_query = request.json.get("query", "")
        user_email = request.json.get("email", "")

        search = SerpAPIWrapper()
        tools = [
            Tool(
                name="search",
                func=search.run,
                description="useful for when you need to answer questions ",
            ),
            WriteFileTool(),
            ReadFileTool(),
        ]

        vectorstore = setup_vectorstore()

        agent = AutoGPT.from_llm_and_tools(
            ai_name="SupportBot",
            ai_role="AnswerBot",
            tools=tools,
            llm=ChatOpenAI(temperature=0),
            memory=vectorstore.as_retriever(),
        )
        agent.chain.verbose = True

        result = agent.run(
            [
                f"Please answer this question {customer_query}",
                f"save the report in the `query` directory",
            ],
            limit=4,
        )

        if user_email:
            subject = "Your Support Query has been Answered"
            body = f"Your support query '{customer_query}' has been answered. Here is the response:\n\n{result}"
            send_email(user_email, subject, body)

        return jsonify({"status": "success", "result": result})
    except Exception as e:
        return handle_error(e)


@app.route("/responses", methods=["GET"])
def list_responses():
    try:
        responses = os.listdir("query")
        return jsonify({"status": "success", "result": responses})
    except Exception as e:
        return handle_error(e)


@app.route("/responses/<response_name>", methods=["GET"])
def read_response(response_name):
    try:
        response_path = os.path.join("query", response_name)
        if os.path.exists(response_path):
            with open(response_path, "r") as file:
                content = file.read()
            return jsonify({"status": "success", "result": content})
        else:
            return jsonify({"status": "failed", "error": "File not found"}), 404
    except Exception as e:
        return handle_error(e)


@app.route("/research", methods=["POST"])
def handle_market_research():
    try:
        customer_query = request.json.get("research", "")
        embeddings_model = OpenAIEmbeddings()
        # Initialize the vectorstore as empty

        search = SerpAPIWrapper()
        tools = [
            Tool(
                name="search",
                func=search.run,
                description="useful for when you need to answer questions ",
            ),
            WriteFileTool(),
            ReadFileTool(),
        ]

        vectorstore = setup_vectorstore()

        agent = AutoGPT.from_llm_and_tools(
            ai_name="MarketResearchBot",
            ai_role="Helps in Business ideas",
            tools=tools,
            llm=ChatOpenAI(temperature=0),
            memory=vectorstore.as_retriever(),
        )
        agent.chain.verbose = True

        result = agent.run(
            [
                f"Understand the business idea {customer_query} ",
                f"save the report in the `research` directory",
            ],
            limit=4,
        )

        return jsonify({"status": "success", "result": result})
    except Exception as e:
        return handle_error(e)


@app.route("/researched", methods=["GET"])
def list_researched():
    try:
        researched = os.listdir("research")
        return jsonify({"status": "success", "result": researched})
    except Exception as e:
        return handle_error(e)


@app.route("/researched/<researched_name>", methods=["GET"])
def read_researched(researched_name):
    try:
        response_path = os.path.join("research", researched_name)
        if os.path.exists(response_path):
            with open(response_path, "r") as file:
                content = file.read()
            return jsonify({"status": "success", "result": content})
        else:
            return jsonify({"status": "failed", "error": "File not found"}), 404
    except Exception as e:
        return handle_error(e)


def setup_vectorstore():
    embeddings_model = OpenAIEmbeddings()
    embedding_size = 1536
    index = faiss.IndexFlatL2(embedding_size)
    return FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})


if __name__ == "__main__":
    app.run(debug=True)
