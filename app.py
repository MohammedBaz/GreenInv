
import ee
import streamlit as st

from google.oauth2 import service_account

import os 
st.write(os.environ)
#st.write(os.listdir(os.getcwd()).streamlit )
from google.oauth2 import service_account

newfile=os.path.join(os.getcwd(), ".streamlit")
st.write(os.listdir(newfile))

newnewfile=os.path.join(newfile, "secrets.toml")

st.write(os.getcwd()+"/.streamlit/secrets.toml")

#st.write(st.secrets["gee_service_account"]["client_email"])
#st.write(st.secrets["gee_service_account"])
#credentials = service_account.Credentials.from_service_account_info(
#    st.secrets["gee_service_account"]
#)

st.write(os.path.exists(newnewfile))
#EE_CREDENTIALS = ee.ServiceAccountCredentials(st.secrets['gee_service_account']['client_email'], newnewfile)
#ee.Initialize(EE_CREDENTIALS)
#
