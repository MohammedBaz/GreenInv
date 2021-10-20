import json
dictionary = {'type':st.secrets['Google_Earth_Engine']['type'],
              'project_id':st.secrets['Google_Earth_Engine']['project_id'],
              'private_key_id':st.secrets['Google_Earth_Engine']['private_key_id'],
              'private_key':st.secrets['Google_Earth_Engine']['private_key'],
              'client_email':st.secrets['Google_Earth_Engine']['client_email'],
              'client_id':st.secrets['Google_Earth_Engine']['client_id'],
              'auth_uri':st.secrets['Google_Earth_Engine']['auth_uri'],
              'token_uri':st.secrets['Google_Earth_Engine']['token_uri'],
              'auth_provider_x509_cert_url':st.secrets['Google_Earth_Engine']['auth_provider_x509_cert_url'],
              'client_x509_cert_url':st.secrets['Google_Earth_Engine']['client_x509_cert_url']
             }
y = json.loads(dictionary)
st.write(y)


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
EE_CREDENTIALS = ee.ServiceAccountCredentials(st.secrets['Google_Earth_Engine']['client_email'], newnewfile)
ee.Initialize(EE_CREDENTIALS)

