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
st.write(st.secrets['type'])
#https://signup.earthengine.google.com/#!/service_accounts
PathtoKeyFile=os.path.join(os.getcwd(), "key.json")
with open(os.path.join(os.getcwd(), "key.json"), 'w') as outfile:
    json.dump(dictionary, outfile)

import ee
EE_CREDENTIALS = ee.ServiceAccountCredentials(st.secrets['client_email'], PathtoKeyFile)
ee.Initialize(EE_CREDENTIALS)

i_date = '2000-01-01' # Initial date of interest (inclusive).
f_date = '2021-01-01'# Final date of interest (exclusive).

lc = ee.ImageCollection('MODIS/006/MCD12Q1')# Import the MODIS land cover collection.
lst = ee.ImageCollection('MODIS/006/MOD11A1')# Import the MODIS land surface temperature collection.
elv = ee.Image('USGS/SRTMGL1_003')# Import the USGS ground elevation image.

lst = lst.select('LST_Day_1km', 'QC_Day').filterDate(i_date, f_date)# Selection of appropriate bands and dates for LST.

u_lat = 21.0807514
u_lon = 40.2975893
u_poi = ee.Geometry.Point(u_lon, u_lat)# Define the urban location of interest as a point near Lyon, France. 

r_lon = 40.3173763
r_lat = 21.3618329
r_poi = ee.Geometry.Point(r_lon, r_lat) # Define the rural location of interest as a point away from the city.


scale = 1000  # scale in meters
elv_urban_point = elv.sample(u_poi, scale).first().get('elevation').getInfo()# Print the elevation near Lyon, France.
st.write(elv_urban_point)
