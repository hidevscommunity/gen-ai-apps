# utility_settings
import pandas as pd
import openai
import json
import time


class SelectionValueGetter:
    def __init__(self, _data):
        self.df = pd.DataFrame(_data).set_index('button')
        self.buttons = self.df.index.unique().tolist()

    def get_selection_value(self, button, selection_column):
        try:
            value = self.df.loc[button, selection_column]
            return value
        except KeyError:
            return f"No matching selection found for button: {button}"

    def get_button_list(self):
        return self.buttons

class SaveChat:
    def __init__(self, prompt, response):
        self.text_chat_file = None
        self.text_chat = None
        self.json_chat = None
        self.json_chat_file = None
        self.prompt = prompt
        self.response = response

    def generate_json_text_files(self):
        ls_chat = list(zip(self.prompt, self.response))
        self.json_chat = json.dumps(ls_chat)

        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
        self.json_chat_file = f'transcript_chat_{timestamp}.json'

        self.text_chat_file = f'transcript_chat_{timestamp}.txt'
        self.text_chat = ''
        for prompt, response in ls_chat:
            self.text_chat += f'prompt: {prompt}\n'
            self.text_chat += f'response: {response}\n'


def openai_psw_check(_psw):
    openai.api_key = _psw
    _valid = None
    _err = None
    try:
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
                {"role": "system", "content": "Hi OpenAI!"},
                {"role": "user", "content": "Hi!"},
            ]
        )
        _valid = True
    except Exception as e:
        _valid = False
        _err = str(e)
#         print("An error occurred:", str(e))
    return _valid, _err


data = {'button': ['DEMO1 - Challenge Kick-off', 'DEMO2 - Challenge Solutions', 'Try it!'],
        'ytb_link': ['https://www.youtube.com/watch?v=pgV_NFdokZ4',
                     'https://www.youtube.com/watch?v=ul5ZqnB3qVw',
                     'https://www.youtube.com/watch?v=rYEDA3JcQqw'],
        'path': ['llama_', 'llama_', None], 
        'ytb_name': ['ytb_hana_ml_call_20221128', 'ytb_hana_ml_call_20230126', None],
        'GPTVectorStoreIndex': [True, True, False],
        'text_input_ytb_link_disabled': [True, True, False]}
