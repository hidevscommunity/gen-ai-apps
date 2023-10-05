import json
import re


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if re.match(pattern, email):
        return True
    else:
        return False
