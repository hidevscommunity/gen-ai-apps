# To create a basic Streamlit app for viewing and editing Org Mode files, you can build upon the Python script I provided earlier. Here's a simple Streamlit version:

# ```python
import streamlit as st
import orgparse
import streamlit as st
import streamlit.components.v1 as components
from streamlit.components.v1 import html

import streamlit as st
import difflib

def compute_and_display_diff(existing_text, user_input):
    differ = difflib.Differ()
    diff = list(differ.compare(existing_text.splitlines(), user_input.splitlines()))

    # Initialize lists to store changes
    added_lines = []
    removed_lines = []

    for line in diff:
        if line.startswith('+ '):
            added_lines.append(line[2:])
        elif line.startswith('- '):
            removed_lines.append(line[2:])


    st.code({
        "new": user_input,
        "added": added_lines,
        "removed":  removed_lines
    })


def read_org_file(file_path):
    with open(file_path, 'r') as file:
        lines =""
        for line in file:
            lines = lines + line
    return lines

def write_org_file(file_path, org_content):
    with open(file_path, 'w') as file:
        file.write(org_content)

def list_tree(org_structure) :
    #org_structure = [...]  # Replace with your Org Mode structure

    # Convert Org Mode structure to JSON (optional)
    org_json = json.dumps(org_structure)
    
    # Create a Streamlit tree view
    st.title("Org Mode Outline Viewer")
    st.sidebar.text("Outline Structure")
    
    # Display the Org Mode outline as a tree
    selected_node = st.sidebar.tree(data=org_json, key="org_tree")

    # Show details of the selected node (optional)
    if selected_node:
        st.write(f"Selected Node: {selected_node}")

def list_outline(org_structure):
    # Load the Org Mode structure (replace with your own method to load data)
    #org_structure = [...]  # Replace with your Org Mode structure

    # Create a Streamlit list view
    st.title("Org Mode Outline Viewer")
    st.sidebar.text("Outline Structure")

    # Display the Org Mode outline as a list
    def display_outline(node, indent=0):
        for item in node:
            title = item.get("title", "")
            st.write(" " * indent + title)
            children = item.get("children", [])
            display_outline(children, indent + 2)
         
def onchange_text(text, node_id):
    old = str(text)
    new = st.session_state[node_id]
    st.write("Compare Old",node_id)
    st.code(str(old))
    compute_and_display_diff(old, new)
    #st.write("Change", str(text) + str(old))
    #print("change"+ str(text) + str(old))
seen = {}
def main():
    file_path = "Hackathon.org"  # Replace with the path to your Org Mode file
    org_content = read_org_file(file_path)
    org_structure = orgparse.loads(org_content)
    
    node= 0
    #st.write("Org Mode Str", org_structure)
        
    for x in org_structure[1:]:
        if x not in seen:
            node_id=f"(N{node})"
            body = x #f"{node_id}=[{x}]"
            seen[x]=body
            
            st.text_area(
                node_id,
                body,
                key=node_id,
                height=428,
                on_change=onchange_text,
                kwargs={
                    "text":body,
                    "node_id":node_id
                }
            )
            node = node + 1


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.write("ERR" + str(e))
        raise e
    
