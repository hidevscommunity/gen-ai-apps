import streamlit as st
import llama

message_data = []


def main():
    
    st.title("Llama 2 Chat App")

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = ""

    st.info("Ask Your Query Below")

    input_text = st.text_area("Enter your query")

    if input_text is not None:
        if st.button("Chat"):
            st.info("Your Query: " + input_text)
            st.session_state.chat_history += "User: " +" "+ str(input_text) + "\n"
            result = llama.get_response(input_text)
            st.session_state.chat_history += "AI Assistant: " + " "+str(result) + "\n"
            st.success("Response:" + str(result))

        st.text_area("Chat History:", value="\n"+st.session_state.chat_history +"\n", height=300)
        session_data = "\n"+st.session_state.chat_history+"\n"
        message_data.append(session_data)

# Run the Streamlit application
if __name__ == "__main__":
    main()