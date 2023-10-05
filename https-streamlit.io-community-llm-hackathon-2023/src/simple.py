import os
import streamlit as st
import json
from base import BaseClarifaiModel
from clarifai.auth.helper import ClarifaiAuthHelper


class SimpleContextClarifaiModel(BaseClarifaiModel):
    def __init__(self, app_id):
        self.config = None        
        user_id =st.secrets["clarifai_user_id"]

        #app_id = self.read_app_id_from_config()

        super().__init__(user_id=user_id, app_id=app_id)
        #self.app = self.client.app(app_id=self.app_id)
        self.auth = None  # for auth helper

    def get_auth_helper(self,app_id):
        # needed for lower level apis
        self.api_key = st.secrets["CLARIFAI_PAT"]
        if self.auth is None:
            self.auth = ClarifaiAuthHelper(
                pat=self.api_key, user_id=self.user_id,
                app_id=app_id
            )
        return self.auth

    def get_user_id_from_config(self):
        config = self.read_config_file()
        return config.get("user_id")

    def read_config_file(self):
        #config_file_path = os.path.expanduser("~/.clarify")
        with open(config_file_path) as fi:
            config = json.load(fi)
        return config

    def create_dataset(self, dataset_id):
        if not self.user_id:
            raise ValueError("User ID is not set")

        dataset_index = {}
        datasets = self.app.list_datasets()
        for ds in datasets:
            name = ds.dataset_info.id
            dataset_index[name] = ds

        idn = "cf_dataset_" + dataset_id.lower()
        if idn not in dataset_index:
            dataset = self.app.create_dataset(dataset_id=idn)
        else:
            dataset = dataset_index[idn]

        return dataset


#model = SimpleContextClarifaiModel()
