import openai
import os

MULTI_CHOICE_SEPARATOR = '\n\n##################################################\n\n'

def chat(messages, max_tokens,temperature = 1, n=1, model="gpt-3.5-turbo-16k"):
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        n=n,
    )
    return MULTI_CHOICE_SEPARATOR.join([choice.message.content for choice in completion.choices])