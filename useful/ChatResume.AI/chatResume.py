import streamlit as st
import PyPDF2
# import openai
import subprocess
import os
from pdf2image import convert_from_path
import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
 
chatbot = None
Finished_Conversation = False

# Read the Resume Template from the workable_web.txt file
template_latex = ""

@st.cache_data
def load_template():    
    with open("workable_web.txt", "r") as f:
        template_latex = f.read()
    return template_latex

template_latex = load_template()

def extract_latex_code(final_response):
    # extract the final resume latex code after \documentclass and before \end{document} in the final_response

    # find the index of \documentclass in the final_response 
    begin_index = final_response.find("\\documentclass")

    # find the index of \end{document} in the final_response
    end_index = final_response.find("\\end{document}")

    # extract the latex code from the final_response
    final_resume_latex = final_response[begin_index: end_index+len("\\end{document}")]

    # replace all &&
    final_resume_latex = final_resume_latex.replace("&&", "\&\&")
    return final_resume_latex


def form_prefix(isCreateResume):
    # Write the prefix of the initial interaction with the chatbot
    # isCreateResume is a boolean value
    # if isCreateResume is True, then the chatbot will create a resume
    prefix = """
        Given the following format of a resume in LaTeX, please Generate the Latex code for the whole Resume after user input enough information 
        Return the final code response in a Code Block (Only Code Block). 
        The final code should end with \end\{document\}.
        Makre sure the syntax is correct and the format is similar to the template. 
        Only change the text information in the template, do not change the format. Or add any parenthesis or brackets or &."""
    if isCreateResume:
        prefix += """
            Use the following conversation to create a resume. (User can choose to skip any question, and leave it blank for output)
            1. (Now starts the heading section) What is your name?
            2. What is your email?
            3.  What is your phone number?
            4. What is your linkedin profile url?
            5. Where are you located (City, State)?
            6. (Now Starts the education section) What is your school name?
            7. What is your degree?
            8. What is your major?
            9. What is your GPA?
            10. What are your selected courses? (maximum of 3 courses)
            11. When is your (expected) graduation date?
            12. Where is your school located (City, State)?
            13. (Now starts the skills section) What are your top 5 coding languages (e.g. Java)?
            14. What are your top 5 frameworks (e.g. React)?
            15. What are your top 5 tools (e.g. Git, Docker)?
            16. What are your top 5 certifications (e.g. AWS)?
            17. (Now starts the experience section) How many companies have you worked for?
            18. (For every company) What is your company name?
            19. (For every company) What is your job title?
            20. (For every company) Where is the work location (City, State)?
            21. (For every company) When is your start date?
            22. (For every company) When is your end date?
            23. (For every company) What are your 1st accomplishments in the company? 
            24. (For every company) What are your 2nd accomplishments in the company? 
            25. (For every company) What are your 3rd accomplishments in the company?
            Repeat 18-25 for every company and ASK the accomplishment One by One.

            26. (Now starts the project section) How many projects have you worked on?
            27. (For every project) What is your project name?
            28. (For every project) What are your 1st accomplishments in the project? 
            29. (For every project) What are your 2nd accomplishments in the project? 
            30. (For every project) What are your 3rd accomplishments in the project? 
            Repeat 27-30 for every project.

            First Question Must be from assistant: What is your name?
            ASK Question One by One.
            Template:
        """

    # if isCreateResume is False, then the chatbot will edit a resume
    else:
        prefix += """
                Use the following conversation to create a resume
                1. Can you please paste your resume text here?

                After user paste the resume text, then generate the Latex code for the whole Resume using the template.
                Template:
        """

    return prefix


def chatbot_response():
    global Finished_Conversation
    if "Finished_Conversation" not in st.session_state:
        st.session_state["Finished_Conversation"] = False
    if "final_response" not in st.session_state:
        st.session_state["final_response"] = ""
    if "resume_choice_made" not in st.session_state:
        st.session_state["resume_choice_made"] = False
    if "create_from_scratch" not in st.session_state:
        st.session_state["create_from_scratch"] = None
    if "open_api_key" not in st.session_state:
        st.session_state["open_api_key"] = None

    with st.sidebar:
        # set the open_api_key as a session state data

        st.session_state["open_api_key"] = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

        # if user input the API key, then show a pop up message saying that the API key is saved
        if st.session_state["open_api_key"]:
            st.success("API key saved!")

    if not st.session_state["resume_choice_made"]:
        greeting_message = "Let's Create an ATS-Friendly Resume, Shall we? \n\n (Say 'YES' to create a ressume from scratch, SAY 'NO' to create a resume from current resume text) \n\n DON'T FORGET TO PUT YOUR OPENAI API KEY IN THE SIDEBAR 📢"
        st.chat_message("assistant").write(greeting_message)
        if first_prompt := st.chat_input(key="initial_prompt"):
            if not st.session_state["open_api_key"]:
                    st.info("Please add your OpenAI API key to continue.")
                    st.stop()

            user_choice = first_prompt.lower()
            st.chat_message('user').write(user_choice)

            if user_choice == "yes":
                st.session_state["create_from_scratch"] = True
                st.session_state["resume_choice_made"] = True
            elif user_choice == "no":
                st.session_state["create_from_scratch"] = False
                st.session_state["resume_choice_made"] = True
        
    if st.session_state["resume_choice_made"]:
        is_create_resume = st.session_state["create_from_scratch"]
        prefix = form_prefix(is_create_resume)

        if is_create_resume:
            first_message = "Let's Create a Resume from Scratch! (SAY 'YES' to continue)"
        else: 
            first_message = "Let's Edit Your Resume! (Paste your resume text here)"
        defined_template_starting_message = prefix + template_latex
    
        if "messages" not in st.session_state:
            st.session_state["messages"] = [AIMessage(content=first_message)]
            st.session_state["context"] = defined_template_starting_message

        print('here')
        for msg in st.session_state.messages:
            # if role is AI, then show the message as assistant
            if msg.type == "ai":
                st.chat_message("assistant").write(msg.content)
            # if role is human, then show the message as user
            else:
                st.chat_message("user").write(msg.content)
        
        

        if st.session_state.Finished_Conversation == False:
            if prompt := st.chat_input():
                if not st.session_state["open_api_key"]:
                    st.info("Please add your OpenAI API key to continue.")
                    st.stop()

                # openai.api_key = st.session_state["open_api_key"]
                chat = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0, openai_api_key=st.session_state["open_api_key"])
                st.session_state.messages.append(HumanMessage(content=prompt))
                st.chat_message("user").write(prompt)

                # if the user says "I am done", then stop the chatbot and set Finished_Conversation to True
                if prompt.lower() == "done":
                    # for last message from the role chatbot, store the message in final_resume_latex
                    # loop from the end of the list to the beginning of the list
                    # if the role is assistant, then store the message in final_response and the final_response contains \begin{document}
                    for i in range(len(st.session_state.messages) - 1, -1, -1):
                        if st.session_state.messages[i].type == "ai" and "\\begin{document}" in st.session_state.messages[i].content:
                            st.session_state['final_response'] = st.session_state.messages[i].content
                            break

                    Finished_Conversation = True
                    # Show the message saying that the conversation is finished
                    st.session_state.Finished_Conversation = True

                    # Restart the app
                    st.experimental_rerun()
                    return

                combined_messages = [HumanMessage(content=st.session_state["context"])] + st.session_state["messages"]

                # if the response is loading then show a message saying that the response is loading
                with st.spinner("Generating response..."):
                    # generate the response from the chatbot
                    # response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k", messages=combined_messages)
                    response = chat(messages=combined_messages)

                msg = response.content
                st.session_state.messages.append(AIMessage(content=msg))
                st.chat_message("assistant").write(msg + "\n\n (Type 'DONE' once you see the Latex Version of your Resume)")
    
        if st.button("Have a typo? Recall the last message"):
            # remove the last 2 message from the list (human and ai)
            if len(st.session_state.messages) >= 2:
                st.session_state.messages = st.session_state.messages[:-2]
                st.experimental_rerun()
                

def latex_to_pdf(latex_code, filename="output"):
    # Save the LaTeX code to a .tex file
    with open(f"{filename}.tex", "w") as f:
        f.write(latex_code)

    # Use lualatex to compile the .tex file
    try:
        print('Compiling LaTeX...')
        result = subprocess.run(["lualatex", f"{filename}.tex"], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=25)
    except subprocess.TimeoutExpired:
        # st.error("Compilation took too long! There might be an error or issue with the LaTeX code.")
        raise ValueError("There might be an error or formattinbg issue with the LaTeX code. \n\n Check whether the latex code ends with \\end{document} ")

    return f"{filename}.pdf"

# 5. Build an app with streamlit
def main():
    # set the title as "GPT Resume Builder ONLY by chatting"
    st.title("ChatResume.AI")

    # text for the app "NO more typing, just chatting, and a ATS friendly resume is ready for you!"
    st.subheader("NO more typing, just chatting, and a ATS friendly resume is ready for you!")

    # Input for LaTeX code
    chatbot_response()

    if st.session_state.Finished_Conversation == True:
        # extract the final resume latex code from the chatbot response
        final_latex_resume = extract_latex_code(st.session_state['final_response'])

        latex_code = st.text_area("Enter your LaTeX code",
                                value=final_latex_resume,
                                height=500)

        # Button to generate PDF
        if st.button("Generate PDF"):
            try:
                pdf_path = latex_to_pdf(latex_code)

            except ValueError as e:
                st.error(str(e))
                return

            try:
                # Convert the PDF to images for preview
                with st.spinner("Generating Your Resume PDF..."):
                    images = convert_from_path(pdf_path, dpi=300)
                    st.text("Preview of your resume:")
                    for img in images:
                        st.image(img)

                    # Provide a download link to the generated PDF
                    with open(pdf_path, "rb") as file:
                        st.download_button(label="Download PDF", data=file, file_name="output.pdf", mime="application/pdf")
                
            except Exception as e:
                st.error(f"An error occurred to convert PDF to images: {e}")


if __name__ == '__main__':
    main()