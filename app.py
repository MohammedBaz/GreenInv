import ee
import streamlit as st

from google.oauth2 import service_account

# Create API client.

#EE_PRIVATE_KEY_FILE = 'privatekey.json'

#credentials = service_account.Credentials.from_service_account_info(
#    st.secrets["gee_service_account"]
#)
#client = ee.ServiceAccountCredentials(credentials=credentials)
EE_CREDENTIALS = ee.ServiceAccountCredentials(st.secrets["gee_service_account"]["client_email"], st.secrets["gee_service_account"])
