import streamlit as st
from whale import whale_function
from hawk import hawk_function
from op import op_function
from dhurandhar import dhurandhar_function

# Set the page title
st.title("Multi-Button Streamlit App")

# Create a layout with four buttons
st.header("Choose an Action")

# Create columns for better button layout (optional, for aesthetics)
col1, col2 = st.columns(2)

with col1:
    if st.button("Whale"):
        result = whale_function()
        st.write(result)

    if st.button("Hawk"):
        result = hawk_function()
        st.write(result)

with col2:
    if st.button("Op"):
        result = op_function()
        st.write(result)

    if st.button("Dhurandhar"):
        result = dhurandhar_function()
        st.write(result)