import streamlit as st
from joblib import load as jb_load
import numpy as np

st.subheader('Prediction Form')
# Load the model
nb_predict_train = jb_load(f'best_model.pkl')
columns = st.session_state['df_columns']
target = st.session_state['target']
inputs = []

# Add input fields for user input
for column in columns:
    if column == target:
        continue
    inputs.append(st.text_input(column))

# Add a button to trigger the prediction
if st.button("Predict"):
    # Perform prediction using the loaded model
    prediction = nb_predict_train.predict(inputs) 
    
    # Display the prediction result
    st.write("Prediction:", prediction)