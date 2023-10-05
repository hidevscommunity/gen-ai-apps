import os

from dotenv import load_dotenv
from supabase import Client, create_client  # type: ignore

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)  # type: ignore


def log_message(user_type: str, message: str):
    supabase.table('logs').insert(
        {"user_type": user_type, "message": message}).execute()