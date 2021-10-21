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

import pandas
def GetInformtionFromGoogleEarth(ImageCollectionName,ListofBands,Resultion,StartDate,EndDate,Lat,Long):
  PoI = ee.Geometry.Point(Long, Lat) # Cast Lat and Long into required class
  ImageCollection=ee.ImageCollection(ImageCollectionName) # get the image collecton from google earthengine
  FilteredImageCollections = ImageCollection.select(ListofBands).filterDate(StartDate, EndDate) # apply filter(s):time and/or bands
  results=FilteredImageCollections.getRegion(PoI, Resultion).getInfo() # get the time series of the required bands
  resultsdf=pandas.DataFrame(results) #Cast the results getten from the above to dataframe
  headers = resultsdf.iloc[0] # set the header of dataframe to the first line of the results
  resultsdf = pd.DataFrame(resultsdf.values[1:], columns=headers) # assign the results to the dataframe and use headers as columns names
  resultsdf = resultsdf.dropna() # drops all rows with no data 
  for band in ListofBands: # Convert the data to numeric values
        resultsdf[band] = pandas.to_numeric(resultsdf[band], errors='coerce')
  resultsdf['datetime'] = pandas.to_datetime(resultsdf['time'], unit='ms') # Convert the time field into a datetime.
  resultsdf = resultsdf[['time','datetime',  *ListofBands]]
  return resultsdf

 
#############################################################Read the datasets#################################################################

BandInformation=pandas.read_csv('BandInformation.csv')
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

import datetime
with st.sidebar.expander("Please select the dataset we wish to work on"):
  option = st.selectbox('Please select the meteorological dataset',BandInformation['Description'])
  st.write('You selected:', option)
  if option is not None:
    SelectedBand=BandInformation[BandInformation['Description']==option]
    ImageCollectionName=SelectedBand['ImageCollection'][0]
    ListofBands=SelectedBand['Bands'][0]
    Resultion=SelectedBand['Resultion'][0]
    StartDate=SelectedBand['StartDate'][0]
    EndDate=SelectedBand['EndDate'][0]
    Lat=21.0807514
    Long= 40.2975893
   
    
    d = st.date_input("Plase select the date range",min_value=datetime.date(2019, 7, 6),max_value=datetime.date(2020, 7, 6))
   
