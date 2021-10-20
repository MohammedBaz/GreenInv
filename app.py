import ee
import streamlit as st

from google.oauth2 import service_account

#st.write(st.secrets["gee_service_account"]["client_email"])
#st.write(st.secrets["gee_service_account"])

EE_CREDENTIALS = ee.ServiceAccountCredentials(st.secrets["gee_service_account"]["client_email"], **st.secrets.gee_service_account)
ee.Initialize(EE_CREDENTIALS)
