
import ee
import streamlit as st

from google.oauth2 import service_account

import os 
st.write(os.environ)["secrets.toml"]

from google.oauth2 import service_account

#st.write(st.secrets["gee_service_account"]["client_email"])
#st.write(st.secrets["gee_service_account"])
#credentials = service_account.Credentials.from_service_account_info(
#    st.secrets["gee_service_account"]
#)


#EE_CREDENTIALS = ee.ServiceAccountCredentials(st.secrets['gee_service_account']['client_email'], credentials)
#ee.Initialize(EE_CREDENTIALS)
