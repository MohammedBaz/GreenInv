import ee
import streamlit as st

from google.oauth2 import service_account

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["Google_Earth_Engine"]
)
client = ee.Initialize(credentials=credentials)


st.write("initalised")
