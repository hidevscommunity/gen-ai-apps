from deta import Deta
import streamlit as st


deta_cred = st.secrets["db_credentials"]
deta = Deta(deta_cred["deta_key"])


def get_users():
    users = deta.Base("newsletter_signup")
    return users.fetch().items


def update_user(details):
    users = deta.Base("newsletter_signup")
    all_users = users.fetch().items
    all_emails = [user["email"] for user in all_users]
    if details["email"] in all_emails:
        return False
    users.insert(details)
    return True
