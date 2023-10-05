import os
import streamlit.components.v1 as components
import streamlit as st

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "card-list/build")

_component_func = components.declare_component("my_component", path=build_dir)
def my_component(data,type, key=None):
    
    """Create a new instance of "my_component".

    Parameters
    ----------
    name: str
        The name of the thing we're saying hello to. The component will display
        the text "Hello, {name}!"
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(data=data,type=type, key=key, default=0)


    
    if not "my_comm" in st.session_state:
        st.session_state.my_comm = component_value
        return component_value
    elif (st.session_state["my_comm"]!= component_value):
        st.session_state["my_comm"] = component_value
        return component_value
    else:
        return False

