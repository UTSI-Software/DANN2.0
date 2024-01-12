import streamlit as st
from st_login_form import login_form
from supabase import create_client, client
from msal_streamlit_authentication import msal_authentication
from datetime import datetime
import random


loginForm = "UTSI Login"
redirectUri = ""

def check_authentication():
    """
    Check if the user is authenticated.
    
    Returns:
        bool: True if authenticated, False otherwise.
    """
    if 'authenticated' not in st.session_state:
        get_loginform()
        return False
    return True
#https://app.supabase.com/project/rbaawqpeyigwmzukrmvc/editor/28594
#https://docs.streamlit.io/knowledge-base/tutorials/databases/supabase#create-a-supabase-database


def get_loginform():
    client = login_form(loginForm, allow_guest=False)

    if st.session_state.authenticated:
        if st.session_state.username:
            st.success(f"Welcome {st.session_state.username}")
        else:
            st.success("Welcome Guest")
    else:
        st.error("Not Authenticated")


def generate_varKey():
    # Get the current date in the format YYYY-MM-DD
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Generate a random integer between 1 and 100000
    random_int = random.randint(1, 100000)
    
    # Concatenate the date and the random integer to form varKey
    varKey = f"{current_date} - {random_int}"
    
    return varKey


def get_msal_login_token():
    varAuth = {
        "clientId": "cb42cf75-3878-4eb6-b203-3147b862ae3f",
        "authority": "https://login.microsoftonline.com/eb998ecc-cd25-4963-ad28-6e2a1171f9f6", 
        "redirectUri": "http://localhost:8502/Test"#"https://feoc-dev.streamlit.app/auth_redirect",
        #"postLogoutRedirectUri": "https://feoc-dev.streamlit.app/"  # Or another URI where you handle post-logout navigation
    }
    varCache = {
        "cacheLocation": "sessionStorage",
        "storeAuthStateInCookie": False
    }
    varLoginRequests = {
        "scopes": ["cb42cf75-3878-4eb6-b203-3147b862ae3f/.default"]
    }
    varLogoutRequests = {} #optional
    varLoginButtonText = "Login"
    varLogoutButtonText = "Logout"
    varKey = "authlogin1"
    

    login_token = msal_authentication(
        auth=varAuth,
        cache=varCache,
        login_request=varLoginRequests,
        logout_request=varLogoutRequests,
        login_button_text=varLoginButtonText,
        logout_button_text=varLogoutButtonText, 
        key=varKey
    )
    st.write("token received", login_token)
    #   return login_token
