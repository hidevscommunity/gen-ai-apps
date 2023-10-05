from utils.session_state import *
from custom_streamlit.functions import func_stop_generating

def func_delete_messages(index):
    try:
        ##Stop Generating Function
        max_iterations = executor_session_state().max_iterations
        executor_session_state().max_iterations = 0
        st.session_state['executing'] = False
        st.session_state.max_iterations = max_iterations
        st.session_state['execute']["ids"][st.session_state['execute']["current_id"]]["type"] = "Forced"

        messages_session_state()[:] = messages_session_state()[:index]

        memory = executor_session_state().memory
        messages = memory.chat_memory.messages
        #Find index in memory
        memory_index = -2
        for i,message in enumerate(messages):
            class_name = message.__class__.__name__
            if(class_name == 'HumanMessage'):
                if(index <= 0):
                    break
                memory_index = i
                index = index - 2

        messages[:] = messages[:memory_index+2]

    except:
        print('No Memory for agent')

