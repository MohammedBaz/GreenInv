import streamlit as st
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(st.secrets["gee_service_account"])
scoped_credentials = credentials.with_scopes(
    ['https://www.googleapis.com/auth/cloud-platform'])

session = AuthorizedSession(scoped_credentials)

url = 'https://earthengine.googleapis.com/v1beta/projects/earthengine-public/assets/LANDSAT'

response = session.get(url)

from pprint import pprint
import json
st.write(json.loads(response.content))


import ee
import streamlit as st

from google.oauth2 import service_account



from google.oauth2 import service_account

#st.write(st.secrets["gee_service_account"]["client_email"])
#st.write(st.secrets["gee_service_account"])
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gee_service_account"]
)


EE_CREDENTIALS = ee.ServiceAccountCredentials(st.secrets['gee_service_account']['client_email'], credentials)
ee.Initialize(EE_CREDENTIALS)
