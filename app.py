import ee
import streamlit as st

from google.oauth2 import service_account

# Create API client.
st.write("DB username:",st.secrets["client_email"])

#EE_PRIVATE_KEY_FILE = 'privatekey.json'

EE_CREDENTIALS = ee.ServiceAccountCredentials(st.secrets["client_email"],st.secrets["gee_service_account"])
