import streamlit as st
from whale import whale_function
from hawk import hawk_function
from op import op_function
from dhurandhar import dhurandhar_function

# Set the page title
st.title("Multi-Button Streamlit App")

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'main'

# Main page with buttons
if st.session_state.page == 'main':
    st.header("Choose an Action")
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
            st.session_state.page = 'op_screen'
        if st.button("Dhurandhar"):
            result = dhurandhar_function()
            st.write(result)

# Op screen
if st.session_state.page == 'op_screen':
    st.title("Upload Option Greeks")
    if st.button("Back"):
        st.session_state.page = 'main'
    op_function()