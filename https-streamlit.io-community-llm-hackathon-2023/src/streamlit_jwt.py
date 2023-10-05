import streamlit as st
import jwt
import time
import urllib.parse

def url_gen(resource, expiration, secret):
    payload = {
        "resource": resource,
        "exp": round(time.time()) + (expiration * 60)  # Convert minutes to seconds
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    query_params = dict( embedded=True,
                         _jwt=token)
    return query_params, token

def main():
    st.title("Streamlit JWT URL Generator")

    oparams = st.experimental_get_query_params()
    params = {
        x: oparams[x][0]  for x in oparams
    }
    #params # smart

    #embedded":"True"
    #"_jwt":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZXNvdXJjZSI6ImRmZHNzZCIsImV4cCI6MTY5NDY5NTQ2Nn0.Ch1ex58sojWxSXX1LDFSqtgdoODlRoFcxVV2BtrxDDg"
    #"expiration":"60"
    #"resource":"dfdssd"
    #"secret":"60"

    # User input for resource, expiration, and secret key
    #context = st.text_input("ContextKey:",params.get("context","standard",))        
    resource = st.text_input("Resource ID:",params.get("resource",""),key="res")
    expiration = st.number_input("Expiration (minutes):", min_value=1, value=int(params.get("expiration",60)), key="expire")
    secret = st.text_input("Secret Key:",params.get("secret",""), key="secret")
    jwt_token = st.text_input("Enter JWT Token",params.get("_jwt",""), key="jwt")

    # Generate URLs and JWT token
    if st.button("Generate URLs and JWT Token"):
        if resource and expiration and secret:
            query_params, token = url_gen(resource, expiration, secret)

            # Display URLs and token using st.markdown
            st.subheader("Generated URLs and JWT Token:")

            query_params["expiration"]=expiration
            encoded_query1 = urllib.parse.urlencode(query_params, doseq=True)
            st.markdown(f"* Share [URL with Query Parameters {encoded_query1}](/?{encoded_query1})")

            query_params["resource"]=resource
            encoded_query2 = urllib.parse.urlencode(query_params, doseq=True)
            st.markdown(f"* Share [URL with Query Parameters {encoded_query2}](/?{encoded_query2})")

            query_params["secret"]=secret
            encoded_query3 = urllib.parse.urlencode(query_params, doseq=True)
            st.markdown(f"* SECRETShare [URL with Query Parameters {encoded_query3}](/?{encoded_query3})")

            st.markdown(f"* JWT Token:")
            st.code(token)

            # magic
            #st.write("st.session_state",st.session_state)
            st.session_state
            for x in st.session_state:
                v = st.session_state[x]
                st.write("DEBUG",x,v)

        else:
            st.warning("Please fill in all fields.")
            secret_key = st.text_input("Enter Secret Key")

        # Create a button to initiate decoding
    decode_button = st.button("Decode JWT", )
    if decode_button:
        if jwt_token and secret:
            decoded_result = decode_jwt(jwt_token, secret)
            st.write("Decoded JWT Payload:")
            st.write(decoded_result)
        else:
            st.write("Please enter a JWT token and secret key to decode.")


# Function to decode JWT
def decode_jwt(token, key):
    try:
        decoded_payload = jwt.decode(token, key, algorithms=["HS256"])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return "JWT token has expired"
    except jwt.InvalidTokenError:
        return "Invalid JWT token"

# Handle decoding when the button is clicked


if __name__ == '__main__':
    main()
