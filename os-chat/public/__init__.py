from utils.inputs.html import extract

public_dir = "public/"

css_index = extract(f"{public_dir}index.css")
tpl_bot = extract(f"{public_dir}bot.html")
tpl_user = extract(f"{public_dir}user.html")
