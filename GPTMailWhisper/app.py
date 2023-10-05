import openai
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plost 
from time import time, sleep


# TODO: make it easirr to read with documetation
# TODO: Add more Shortcuts and create documentation for them

def Settingup() -> None:
    '''
    -------------------------------------------
    This is where all the session state variables are created and the streamlit page is setup
    -------------------------------------------
    Parameters:
        None

    Returns:
        None
    '''
    hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            header {font-size: 4rem;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    # create sessionstate for msg
    if 'api_key' not in st.session_state:
        st.session_state['api_key'] = []
    if 'first_time' not in st.session_state:
        st.session_state['first_time'] = True

    if 'context' not in st.session_state:
        st.session_state['context'] = []
    if 'name' not in st.session_state:
        st.session_state['name'] = []
    if 'relation' not in st.session_state:
        st.session_state['relation'] = []
    if 'email_theme' not in st.session_state:
        st.session_state['email_theme'] = []
    if 'Sendername' not in st.session_state:
        st.session_state['Sendername'] = []

    if 'result' not in st.session_state:
        st.session_state['result'] = []
    if 'total_tolkens' not in st.session_state:
        st.session_state['total_tolkens'] = 0
    if 'total_cost' not in st.session_state:
        st.session_state['total_cost'] = 0.0

    if 'chart_cost' not in st.session_state:
        st.session_state['chart_cost'] = [0]
    if 'chart_time' not in st.session_state:
        st.session_state['chart_time'] = [0]
    if 'start_time' not in st.session_state:
        st.session_state['start_time'] = time()

    if 'advanced_options' not in st.session_state:
        st.session_state['advanced_options'] = {
            "temperature": 0.5,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "max_tokens": 64,
        }
    
    if 'prompt' not in st.session_state:
        st.session_state['prompt'] = []

def colored_header(label : str = "Cool title",description : str = "Cool description",color_name : str = "gold",help : str = "", description_help : str = "") -> None:
    """
    -------------------------------------------
    Shows a header with a colored underline and an optional description.
    -------------------------------------------
    Parameters:
        label (str): The title of the header. [Default: "Cool title"]
        description (str): The description of the header. [Default: "Cool description"]
        color_name (str): The color of the underline. [Default: "gold"]
        help (str): The help text of the title. [Default: nothing]
        description_help (str): The help text of the description. [Default: nothing]
    
    Returns:
        None

    Examples:
        >>> colored_header("Cool title", "Cool description", "gold", "This is the help text of the title", "This is the help text of the description")
        >>> colored_header("Cool title", "Cool description", "gold")

    """
    st.title(
        body=label,
        help=help,
    )
    st.write(
        f'<hr style="background-color: {color_name}; margin-top: 0;'
        ' margin-bottom: 0; height: 3px; border: none; border-radius: 3px;">',
        unsafe_allow_html=True,
    )
    if description:
        st.caption(description,help=description_help)
def Notif(type : str = "success",duration : int = 3, message : str = "None") -> None:
    '''
    -------------------------------------------
    Shows a notification for a few seconds
    -------------------------------------------
    Parameters:
        type (str): The type of the notification. [Default: "success"]
        duration (int): The duration of the notification. [Default: 3]
        message (str): The message of the notification. [Default: "None"]

    Returns:
        None

    Examples:
        >>> Notif("success", 3, "This is a success notification")
        >>> Notif("error", 2, "This is an error notification")
        >>> Notif("warning", 5, "This is a warning notification")
        >>> Notif("info", 3, "This is an info notification")
    '''
    if message == "None":
        message = type 

    if type == "success":
        notif = st.success(message)
    elif type == "error":
        notif = st.error(message)
    elif type == "warning":
        notif = st.warning(message)
    elif type == "info":
        notif = st.info(message)
    else:
        notif = st.write("Notif type not found")
    
    sleep(duration)
    notif.empty()
def SetAPI(NotifMode : bool = True) -> None:
    ''' 
    -------------------------------------------
    This is where the API Key is set and authenticated
    -------------------------------------------
    Parameters:
        NotifMode (bool): If True then it will show a notification if the API Key is authenticated. [Default: True]

    Returns:
        None
    '''

    st.session_state['api_key']= st.text_input(
        label="Enter your OpenAI API Key",
        help="Please Enter your API Key",
        type="password",
    )



    if NotifMode and st.session_state.api_key:
        # check for authentication error
        openai.api_key = st.session_state.api_key
        try:
            openai.Engine.retrieve("ada")
            if st.session_state.first_time:
                st.session_state.first_time = False
                Notif("success",duration = 1.5 , message="API Key Authenticated")
                
        except:
            Notif("error",duration = 1.5, message = "Authentication Error with API Key")

    else:
        openai.api_key = st.session_state.api_key

def ClearButton() -> None:
    '''
    -------------------------------------------
    This is where the clear button is created
    -------------------------------------------
    It will clear the session state variables and show a 
    notification for a few seconds
    '''
    clear_button = st.button("Clear Session")
    if clear_button:
        Notif("info",duration = 1.5, message = "Conversation Cleared")
        st.session_state['total_tolkens'] = 0
        st.session_state['total_cost'] = 0.0
        st.session_state['chart_cost'].append(0)
        st.session_state['chart_time'].append(time() - st.session_state.start_time)

def AdvancedOptions() -> None:
    '''
    -------------------------------------------
    This is where the advanced options are created
    -------------------------------------------
    Expander for the advanced options like temperature, top_p, etc...
    to adjust the AI's response to the user's input
    '''        
    # make a dropdown menu for the advanced options
    with st.expander("Advanced Options: "):
        st.session_state["advanced_options"]["temperature"] = st.slider(
            label="Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.01,
            help="Controls randomness. Lowering results in less random completions. As the temperature approaches zero, the model will become deterministic and repetitive. Higher temperature results in more random completions.",

        )

        st.session_state["advanced_options"]["top_p"] = st.slider(
            label="Top P",
            min_value=0.0,
            max_value=1.0,
            value=1.0,
            step=0.01,
            help="Controls diversity via nucleus sampling: 0.5 means half of all likelihood-weighted options are considered.",

        )

        st.session_state["advanced_options"]["frequency_penalty"] = st.slider(
            label="Frequency Penalty",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.01,
            help="How much to penalize new tokens based on their existing frequency in the text so far. Decreases the model's likelihood to repeat the same line verbatim.",

        )

        st.session_state["advanced_options"]["presence_penalty"] = st.slider(
            label="Presence Penalty",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.01,
            help="How much to penalize new tokens based on whether they appear in the text so far. Increases the model's likelihood to talk about new topics.",

        )

        st.session_state["advanced_options"]["max_tokens"] = st.slider(
            label="Max Tokens",
            min_value=10,
            max_value=150,
            value=64,
            step=1,
            help="The maximum number of tokens to generate. Requests can use up to 2048 tokens shared between prompt and response. helps to limit the cost of requests.",
        )

        # create a checkbox for dev mode
        dev = st.checkbox(
            label="Developer Mode",
            value=False,
            help="Developer Mode will show the raw response from the API.",
        )

        if dev:
            # create a new variable that has all values for st.session_state except the api_key
            dev_session_state = st.session_state
            del dev_session_state["api_key"]
            st.write(dev_session_state)
def EmailTheme() -> None:
    '''
    -------------------------------------------
    This is where the email theme is created
    -------------------------------------------
    It will create a multiselect box for the user to select the theme of the email
    '''
    st.session_state['email_theme'] = st.multiselect(
            "What is the theme and lenght of the Email?",
            options = [
                "Short",
                "Long",
                "Medium",
                "Concise",
                "Apology",
                "Formal",
                "Casual",
                "Friendly",
                "Intellectual",
                "Informative",
                "Persuasive",
                "Collaborative",
                "Appreciation",
                "Invitation",
                "Thank You",
                "Condolence",
                "Urgent",
                "Sales Promotion",
                "Feedback Request",
                "Announcement",
                "Reminder",
                "Follow-up",
                "Welcome",
                "Congratulations",
                "Professional",
                "Personal",
                "Business Proposal",
                "Job Application",
                "Networking",
                "Inquiry",
                "Meeting Request",
                "Complaint",
                "Resignation",
                "Holiday Greetings",
                "Other"
            ],
            max_selections=6,
            default=["Formal","Short"],
            help="Select Other if you don't see the theme of the email in the list.",
        )

    if "Other" in st.session_state.email_theme:
        extra_theme = st.text_input(
            label="Theme of the Email",
            max_chars=100,
            help="Please Enter the theme of the Email seperated by commas if there are multiple themes. MAX 3",
            placeholder="Enter the Theme of the Email",   
        )
        # seperate the themes by commas then combine the two lists
        if extra_theme:
            st.session_state.email_theme = st.session_state.email_theme + extra_theme.split(",")[:3]
        else:
            st.session_state.email_theme = extra_theme.split(",")[:6]
def Relation() -> None:
    '''
    -------------------------------------------
    This is where the relation of the recipient is created
    -------------------------------------------
    It will create a select box for the user to select the relation of the recipient

    '''
    st.session_state['relation'] = st.selectbox(
        "How is the Recipient related to you?",
        options= [
            "Co-Worker",
            "Boss",
            "Manager",
            "Receptionist",
            "Customer Support Representative",
            "Sales Representative",
            "Project Manager",
            "Human Resources Manager",
            "Marketing Manager",
            "IT Support Specialist",
            "Executive Assistant",
            "Account Manager",
            "Event Planner",
            "Financial Analyst",
            "Research Scientist",
            "Journalist",
            "Operations Manager",
            "Graphic Designer",
            "Software Developer",
            "Academic Advisor",
            "Architect",
            "Librarian",
            "CEO",
            "Consultant",
            "Psychologist",
            "Artist",
            "Lawyer",
            "Dean",
            "Teacher",
            "Professor",
            "Doctor",
            "Engineer",
            "Scientist",
            "Nurse",
            "Chef",
            "Police Officer",
            "Firefighter",
            "Writer",
            "Musician",
            "Entrepreneur",
            "Athlete",
            "Photographer",
            "Social Media Manager",
            "Financial Planner",
            "Veterinarian",
            "Flight Attendant",
            "Fashion Designer",
            "Data Analyst",
            "Translator",
            "Dentist",
            "Pharmacist",
            "Real Estate Agent",
            "Electrician",
            "Mechanic",
            "Friend",
            "Family",
            "Mother",
            "Father",
            "Brother",
            "Sister",
            "Son",
            "Daughter",
            "Grandmother",
            "Grandfather",
            "Aunt",
            "Uncle",
            "Cousin",
            "Niece",
            "Nephew",
            "Husband",
            "Wife",
            "Boyfriend",
            "Girlfriend",
            "Partner",
            "Other"
        ],
        help="Select Other if you don't see the relation of the recipient in the list.",
    )

    if st.session_state.relation == 'Other':
        st.session_state.relation = st.text_input(
            label="relation of the Recipient",
            max_chars=100,
            help="Please Enter how the Recipient is related to you.",
            placeholder="Enter the relation of the Recipient",   
        )
def RecipientName() -> None:
    '''
    -------------------------------------------
    This is where the name of the recipient is created
    -------------------------------------------
    It will create a text input box for the user to enter the name of the recipient
    and set the session state variable to the name of the recipient
    '''
    st.session_state['name'] = st.text_input(
            label="To: ",
            max_chars=100,
            help="This will show up in the Email. If you don't enter a name then it will be Sir/Madam by default.",
            placeholder="Recipient",   
        )
def SenderName() -> None:
    '''
    -------------------------------------------
    This is where the name of the sender is created
    -------------------------------------------
    It will create a text input box for the user to enter the name of the sender
    and set the session state variable to the name of the sender
    '''
    st.session_state['Sendername'] = st.text_input(
            label="From: ",
            max_chars=100,
            help="This will show up in the Email.",
            placeholder="Sender",   
        )
def CostCalculation(chat_usage : dict) -> None:
    '''
    -------------------------------------------
    This is where the cost of the email is calculated
    -------------------------------------------
    It will calculate the cost of the email based on the chat usage
    and add it to the total cost and total tokens

    Parameters:
        chat_usage (dict): The chat usage of the email

    Returns:
        None
    '''
    st.session_state.total_tolkens = chat_usage["total_tokens"] + st.session_state.total_tolkens
    st.session_state.total_cost += (chat_usage["prompt_tokens"] * 0.0015 / 1000) + (chat_usage["completion_tokens"] * 0.002 / 1000)

    st.session_state.chart_cost.append(st.session_state.total_cost)
    st.session_state.chart_time.append(time() - st.session_state.start_time)

def Sidebar() -> None:
    '''
    -------------------------------------------
    This is where the sidebar is created
    -------------------------------------------
    It will create the sidebar with all the options
    '''
    with st.sidebar:

        colored_header(
        label="Basic Info",
        description="Create a professional email with GPT-3.5 ",
        description_help= ""
        )

        SetAPI()

        col1, col2 = st.columns(2)
        with col1:
            RecipientName()
        with col2:
            SenderName()
        Relation()
        EmailTheme()

    # create col
    col1, col2 = st.sidebar.columns(2)
    with col1:
        ClearButton()
    with col2:
            graph_button = st.button("Show Graph", key="graph")
    if graph_button:
        # # TEMPORARY
        # # ----------------------------------------------------------------------------------- 
        # st.session_state.chart_cost.append(st.session_state.chart_cost[-1] + random.randint(0, 10))
        # st.session_state.chart_time.append(time() - st.session_state.start_time)
        # # -----------------------------------------------------------------------------------
        with st.chat_message("user"):
            st.write("Can You Show me the Cost Graph?")

        # Convert the lists to a DataFrame
        df = pd.DataFrame({'Time': st.session_state.chart_time, 'Total Cost': st.session_state.chart_cost})
        if len(df) > 1:
            with st.chat_message("assistant"):
                st.write("Sure, Here you go!")
                st.write(" ")
                plost.area_chart(
                    data=df,
                    x="Time",
                    y="Total Cost",
                    color="#a29614",
                    opacity=0.85,
                    title="Total Cost Over Time",
                    width=800,
                    pan_zoom= 'minimap'
                    # x_annot= x_annotation,

                )
        else:
            with st.chat_message("assistant"):
                st.write("There is no data to show. Please Generate an Email First.")
                st.write(" ")
    with st.sidebar:
        AdvancedOptions()
def Body() -> None:
    '''
    -------------------------------------------
    This is where the body is created
    -------------------------------------------
    It will create the body of the main page
    '''
    if not st.session_state.name:
        st.session_state.name = "Sir/Madam"
    
    prompt_template = f"""You are a Profestional Email Drafter who will Draft an Email to {st.session_state.name} who is your {st.session_state.relation} from {st.session_state.Sendername} with the requirements to be {st.session_state.email_theme}"""
    
    colored_header(
    label="Professional Email Drafter",
    description=f"Cost: ${st.session_state.total_cost:.5f} | ₹{(st.session_state.total_cost*82.4582560):.2f} Tokens: {(st.session_state.total_tolkens)}"  ,
    help= "Prompt: " + prompt_template,
    description_help= "Cost Calculated based on OpenAI Pricing"
    )

    st.session_state["context"] = st.text_area(
        label="Email Context ",
        value="",
        max_chars=2500,
        help="This will help the AI to understand the context of the email. (It is Completely Optional) )",
        placeholder = 
            '''        Example: 

        I need to Reply to the Following Email:
        "Hi John,
        I hope you are doing well.
        I am writing to you to ask about the status of the project.
        Best Regards,
        Jane"
        ''',
        height=200,
        
    )
    prompt = [{"role": "system", "content": prompt_template}]
    if st.session_state.first_time:
        st.session_state.prompt.append(prompt)


    # This is where the user types a question
    question = st.chat_input(
        placeholder="Enter the Subject of the Email (Ex: Meeting Request, Sick Leave, Complaint, etc... )",
    )
    st.caption("Shortcut: Press '/' to activate input and Press '/help' for all shortcuts..")


    question = Shortcuts(question)

    # Adding Context
    if st.session_state.context != "":
        question_for_gpt = "Context of email is: \n" + st.session_state.context+ "\nand the Request is: "+ str(question).strip()
    else:
        question_for_gpt = str(question).strip()

    try:
        if question:  # Someone have asked a question
            # TODO
            # prompt.append({"role": "user", "content": question_for_gpt})

            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):
                botmsg = st.empty()
            response = []
            result = ""
            # TODO
            # st.session_state.prompt = prompt
            st.session_state.prompt.append({"role": "user", "content": question_for_gpt})
            with st.spinner("Generating Email... Please Wait for a few seconds"):
                # TODO
                completion = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=prompt,n = 1)
                # completion = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=prompt[-1],n = 1)
                result = completion.choices[0].message.content

            st.session_state.prompt.append({"role": "assistant", "content": result})
            botmsg.write(result)
            st.caption("Press Shift Anywhere to Copy to Clipboard")
            st.session_state.result = result

            chat_usage = completion.usage
            CostCalculation(chat_usage)

            # TODO
            # prompt.append({"role": "assistant", "content": result})
            # st.session_state["prompt"] = prompt
    except openai.error.AuthenticationError:
        Notif("error",duration = 3.5, message = "Authentication Error with API Key")
    except openai.error.RateLimitError:
        Notif("error",duration = 3.5, message = "Rate Limit Error, Please Wait for 30 seconds")
    except openai.error.APIConnectionError:
        Notif("error",duration = 3.5, message = "API Connection Error, Please Check your Internet Connection")
    except openai.error.OpenAIError:
        Notif("error",duration = 3.5, message = "OpenAI Error, Please Check your Internet Connection")
    except:
        Notif("error",duration = 3.5, message = "Unknown Error, Please Try Again")
def ReadHTMLFile(filename : str = "index.html", msg : str = " ") -> str:
    '''
    -------------------------------------------
    This is where the HTML file is read
    -------------------------------------------
    It will read the HTML file and replace the copy_text with the msg
    this is done to allow the copy to clipboard feature to work
    and to allow the autoselect feature to work on the chat input

    Parameters:
        filename (str): The name of the HTML file. [Default: "index.html"]
        msg (str): The message to replace the copy_text with. [Default: " "]

    Returns:
        str: The HTML file with the copy_text replaced with the msg
    '''
    if msg == []:
        msg = " "
    with open(filename, 'r') as file:
        return file.read().replace(
            "copy_text", f"{msg}"
        )
def Shortcuts(question : str) -> str:
    '''
    -------------------------------------------
    This is where the shortcuts are created
    -------------------------------------------
    It will create the shortcuts for the user to use
    The Shortcuts are:
        '/clear' or '/cl': Clears the Conversation
        '/history' or '/hst' : Shows the History of the Conversation
        '/cost' or '/c': Shows the Cost of the Conversation
        '/graph' or '/g': Shows the Cost Graph
        '/prompt' or '/p': Shows the Context of the Email
        '/context' or '/con': Shows the Entire Context behind the Email
        '/relation' or '/r': Shows the Relation of the Recipient
        '/dev'  or '/d': Shows the Dev Mode
        '/help' or '/h': Shows the Shortcuts

    Parameters:
        question (str): The question that the user asked

    Returns:
        str: The question that the user asked
    '''
    if question == '/help' or question == '/h':
        with st.chat_message("assistant"):
            st.write("Here are the shortcuts:")
            st.write(" ")
            st.info("'/clear' or '/cl': Clears the Conversation")
            st.info("'/history' or '/hst' : Shows the History of the Conversation")
            st.info("'/cost' or '/c': Shows the Cost of the Conversation")
            st.info("'/graph' or '/g': Shows the Cost Graph")
            st.info("'/prompt' or '/p': Shows the Context of the Email")
            st.info("'/context' or '/con': Shows the Entire Context behind the Email")
            st.info("'/relation' or '/r': Shows the Relation of the Recipient")
            st.info("'/dev'  or '/d': Shows the Dev Mode")
            st.info("'/help' or '/h': Shows the Shortcuts")
        question = False
    if question == "/clear" or question == "/cl":
        Notif("info",duration = 1.5, message = "Conversation Cleared")
        st.session_state['total_tolkens'] = 0
        st.session_state['total_cost'] = 0.0
        st.session_state['chart_cost'].append(0)
        st.session_state['chart_time'].append(time() - st.session_state.start_time)
        question = False
    
    if question == "/history" or question == "/hst":

        hist = st.session_state.prompt[2:]
        st.divider()
        
        with st.chat_message("assistant"):
            st.subheader("The History of the Conversation is: ")
        for i in hist:
            with st.chat_message(i["role"]):
                st.write(i["content"])
            st.divider()

        question = False

    if question == "/cost" or question == "/c":
        with st.chat_message("assistant"):
            st.write("The Total Cost of the Conversation is: $" + str(st.session_state.total_cost))
            st.write("The Total Tokens of the Conversation is: " + str(st.session_state.total_tolkens))
        question = False
    
    if question == "/graph" or question == "/g":
        with st.chat_message("user"):
            st.write("Can You Show me the Cost Graph?")

        # Convert the lists to a DataFrame
        df = pd.DataFrame({'Time': st.session_state.chart_time, 'Total Cost': st.session_state.chart_cost})
        if len(df) > 1:
            with st.chat_message("assistant"):
                st.write("Sure, Here you go!")
                st.write(" ")
                plost.area_chart(
                    data=df,
                    x="Time",
                    y="Total Cost",
                    color="#a29614",
                    opacity=0.85,
                    title="Total Cost Over Time",
                    width=800,
                    pan_zoom= 'minimap'
                )
        else:
            with st.chat_message("assistant"):
                st.write("There is no data to show. Please Generate an Email First.")
                st.write(" ")
        question = False
    if question == "/prompt" or question == "/p":
        with st.chat_message("assistant"):
            if st.session_state.prompt == "":
                st.write("There is no Context Given")
            else:
                st.write("The Context of the Email is: ")
                st.write(st.session_state.prompt[0]["content"])
        question = False

    if question == "/context" or question == "/con":
        # st.session_state.prompt.pop(0)

        with st.chat_message("assistant"):
            if st.session_state.prompt == "":
                st.write("There is no Context Given")
            else:
                st.write("The Full Context of the Email is: ")
                st.write(st.session_state.prompt)
        question = False

    if question == "/relation" or question == "/r":
        with st.chat_message("assistant"):
            st.write("The Relation of the Recipient is: " + st.session_state.relation)
        question = False

    if question == "/dev" or question == "/d":
        with st.chat_message("assistant"):
            st.write("The Dev Mode is: " )
            safe_dev = st.session_state
            del safe_dev["api_key"]
            st.write(safe_dev)
        question = False

    if type(question) == str:
        if question[0] == "/":
            question = question[1:]
    return question

def main():
    '''
    -------------------------------------------
    Connects all the functions together
    -------------------------------------------
    '''
    
    st.set_page_config(
        page_title="GottaMail", 
        page_icon="📫",
        layout="wide",
        )
    Settingup()
    Body()
    Sidebar()

    components.html(
        ReadHTMLFile(msg=st.session_state.result), 
        height=0,
        width=0,
    )

if __name__ == '__main__':
    main()


