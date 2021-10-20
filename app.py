import json
dictionary = {'type':34,
              'project_id':61,
              'private_key_id':82,
              'private_key':34,
              'client_email':61,
              'client_id':82,
              'auth_uri':34,
              'token_uri':61,
              'auth_provider_x509_cert_url':82,
              'client_x509_cert_url':123
             }



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
import jetblack-tomlutils
toml2json newnewfile- > newnewfile.json

st.write(os.path.exists(newnewfile))
EE_CREDENTIALS = ee.ServiceAccountCredentials(st.secrets['gee_service_account']['client_email'], newnewfile)
ee.Initialize(EE_CREDENTIALS)
#
"""
