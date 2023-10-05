###TROZO CODIGO PARA MAIN.py #################

""" import pickle
from pathlib import Path
import streamlit_authenticator as stauth

names = ['Jose', 'Noelia']
usernames = ['jmmartinnu', 'noerubi']

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, cookie_name, cookie_key="abcdef")


# Renderizar el widget de login
name, authentication_status, username = authenticator.login('Login', st.sidebar)


# Autenticar usuarios y mostrar contenido según el estado de autenticación
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')




if authentication_status: """














""" import pickle
from pathlib import Path
import streamlit_authenticator as stauth

passwords = ['abc123', 'abc']

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)


authenticator = stauth.Authenticate(names, usernames, hashed_passwords, cookie_name="sales_dashboard", cookie_key="abcdef") """