
from utils.session_state import *
from custom_streamlit.functions import func_stop_generating
def func_reset_messages():
    try:
        ##Stop Generating Function
        max_iterations = executor_session_state().max_iterations
        executor_session_state().max_iterations = 0
        st.session_state['executing'] = False
        st.session_state.max_iterations = max_iterations
        st.session_state['execute']["ids"][st.session_state['execute']["current_id"]]["type"] = "Forced"


        messages_session_state().clear()
        executor_session_state().memory.clear()
        
    except:
        print('No Memory for agent')
