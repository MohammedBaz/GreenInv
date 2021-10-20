import json
import streamlit as st
import os 
dictionary = {'type':st.secrets['type'],
              'project_id':st.secrets['project_id'],
              'private_key_id':st.secrets['private_key_id'],
              'private_key':st.secrets['private_key'],
              'client_email':st.secrets['client_email'],
              'client_id':st.secrets['client_id'],
              'auth_uri':st.secrets['auth_uri'],
              'token_uri':st.secrets['token_uri'],
              'auth_provider_x509_cert_url':st.secrets['auth_provider_x509_cert_url'],
              'client_x509_cert_url':st.secrets['client_x509_cert_url']
             }

#https://signup.earthengine.google.com/#!/service_accounts
PathtoKeyFile=os.path.join(os.getcwd(), "key.json")
with open(os.path.join(os.getcwd(), "key.json"), 'w') as outfile:
    json.dump(dictionary, outfile)

import ee
EE_CREDENTIALS = ee.ServiceAccountCredentials(st.secrets['client_email'], PathtoKeyFile)
ee.Initialize(EE_CREDENTIALS)

import pandas as pd
def GetInformtionFromGoogleEarth(StartDate,EndDate,RequestedImageCollection,RequestedImageCollectionFilelds, 
                                 LatPoI,LonPoT,RequiredScale):
  PoI=ee.Geometry.Point(LonPoT, LatPoI)
  ImageCollectionName=ee.ImageCollection(RequestedImageCollection)
  DateFilteredImageCollectionName=ImageCollectionName.select(RequestedImageCollectionFilelds).filterDate(StartDate,EndDate)
  df = pd.DataFrame((DateFilteredImageCollectionName).getRegion(PoI,RequiredScale).getInfo())
  headers = df.iloc[0]
  df = pd.DataFrame(df.values[1:], columns=headers)
  return (df)

X=GetInformtionFromGoogleEarth('2015-01-01','2015-02-01','ECMWF/ERA5_LAND/HOURLY',
                                                                        ['leaf_area_index_high_vegetation','soil_temperature_level_1','soil_temperature_level_2',
                                                                         'lake_ice_depth','lake_ice_temperature','lake_mix_layer_depth','skin_reservoir_content',
                                                                         'leaf_area_index_low_vegetation','volumetric_soil_water_layer_2','evaporation_from_bare_soil',
                                                                         'runoff'],21.0807514,40.2975893,1000)
st.write(X)


#############################################################Page Layout starts here############################################################

#st.set_page_config(layout="wide") just change the page to wide mode
#st.markdown(""" <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """, unsafe_allow_html=True)

st.title("This is a POC app dedicated to Green initiative")
st.header("                                                   ")
#One of the good widgets presented in streamlit is empty. it is a place holder so that we can consider it as template. 
MainPageDescription = st.empty() # The main canvas where the input/output is displayed 
SubMainPageDescription=st.empty() # subcanvas where the inputs/outputs are handled 
Sub2MainPageDescription=st.empty() # same as above
Sub3MainPageDescription=st.empty() # same as above

with st.sidebar.expander("Please select the dataset we wish to work on"):
  ption = st.selectbox('How would you like to be contacted?',('Email', 'Home phone', 'Mobile phone'))
  st.write('You selected:', option)
