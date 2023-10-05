from utils.session_state import *
def func_stop_generating():
    max_iterations = executor_session_state().max_iterations
    executor_session_state().max_iterations = 0
    st.session_state['executing'] = False
    st.session_state.max_iterations = max_iterations
    st.session_state['execute']["ids"][st.session_state['execute']["current_id"]]["type"] = "Forced"

    
    #st.experimental_rerun()
  