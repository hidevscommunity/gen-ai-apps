import os
from typing import List, Any

import openai
from dotenv import load_dotenv
from instructor import openai_schema
from pydantic import create_model

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def create_schema_model(fields, field_name="Document"):
    labels = [i.strip() for i in fields.split(",")]
    model = openai_schema(
        create_model(field_name, **{item: (Any, ...) for item in labels})
    )
    multi_model = openai_schema(create_model(f"{field_name}s", data=(List[model], ...)))
    return multi_model


def completion_fn(model, content):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        functions=[model.openai_schema],
        function_call={"name": model.openai_schema["name"]},
        messages=[
            {"role": "user", "content": content},
        ],
    )
    return completion


def process_extraction(fields, _obj, content):
    model = create_schema_model(fields=fields, field_name=_obj)
    completion = completion_fn(model=model, content=content)
    response = model.from_response(completion)
    return response.model_dump()


def process_qa(content):
    result = process_extraction(
        fields="question, answer", _obj="Question", content=content
    )
    return result
