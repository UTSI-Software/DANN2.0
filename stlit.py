import streamlit as st

# Title of the app
st.title("My Streamlit App")

# Sidebar with options
option = st.sidebar.selectbox("Select an option", ["Option 1", "Option 2", "Option 3"])

# Main content based on the selected option
if option == "Option 1":
    st.write("You selected Option 1.")
elif option == "Option 2":
    st.write("You selected Option 2.")
else:
    st.write("You selected Option 3.")
