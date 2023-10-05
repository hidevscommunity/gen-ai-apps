
import streamlit as st
from .func_show_source import func_show_source

count = 0 
def func_sources_buttons(num_columns, values):
    global count

    # Calculate the number of rows needed to display the values
    num_rows = -(-len(values) // num_columns)  # Ceiling division
    sources = list(values.keys())

    # Create a grid layout with the specified number of columns
    col_width = 12 // num_columns
    for row in range(num_rows):
        cols = st.columns(num_columns)
        for col_idx, col in enumerate(cols):
            value_idx = row * num_columns + col_idx
            if value_idx < len(values):
                source = sources[value_idx]
                count = count+1
                col.button(source,key=f'b{count}',use_container_width=True,on_click=func_show_source,args=(source,values[source],))
