import streamlit as st
from whale import whale_function
from hawk import hawk_function
from op import op_function
from dhurandhar import dhurandhar_function
import urllib.parse

# Get query parameter
query_params = st.query_params
page = query_params.get("page", ["main"])[0].lower()
st.write(f"Debug: Raw query_params = {query_params}, Parsed page = {page}")  # Enhanced debugging

# Set the page title based on the function
if page == "main":
    st.title("Multi-Button Streamlit App")
elif page == "whale":
    st.title("Whale Function")
elif page == "hawk":
    st.title("Hawk Function")
elif page == "op":
    st.title("Op Function")
elif page == "dhurandhar":
    st.title("Dhurandhar Function")
else:
    st.title("Unknown Page")
    st.write(f"Invalid page value: '{page}'. Please use a valid page link (e.g., ?page=hawk).")
    st.write("[Back to Main](?) (Open in new tab)")

# Main page with buttons to open new tabs
if page == "main":
    st.header("Choose an Action")
    col1, col2 = st.columns(2)
    with col1:
        st.write("[Whale](?page=whale) (Open in new tab)")
        st.write("[Hawk](?page=hawk) (Open in new tab)")
    with col2:
        st.write("[Op](?page=op) (Open in new tab)")
        st.write("[Dhurandhar](?page=dhurandhar) (Open in new tab)")

    st.write("Click the links above to open each function in a new tab.")

# Render the appropriate function based on the page
if page == "whale":
    whale_function()
elif page == "hawk":
    hawk_function()
elif page == "op":
    op_function()
elif page == "dhurandhar":
    dhurandhar_function()

# Add a back link to return to the main page
if page != "main" and page in ["whale", "hawk", "op", "dhurandhar"]:
    st.write("[Back to Main](?) (Open in new tab)")