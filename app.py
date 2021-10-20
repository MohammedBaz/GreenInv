import json
import ee
import streamlit as st
import os 
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


PathtoKeyFile=os.path.join(os.getcwd(), "key.json")
with open(PathtoKeyFile, 'w') as outfile:
    json.dump(dictionary, outfile)

EE_CREDENTIALS = ee.ServiceAccountCredentials(st.secrets['Google_Earth_Engine']['client_email'], PathtoKeyFile)
ee.Initialize(EE_CREDENTIALS)

