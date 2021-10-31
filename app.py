import json
import streamlit as st
import os 
import ee

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
PathtoKeyFile=os.path.join(os.getcwd(), "key.json") #https://signup.earthengine.google.com/#!/service_accounts
with open(os.path.join(os.getcwd(), "key.json"), 'w') as outfile:
json.dump(dictionary, outfile)
EE_CREDENTIALS = ee.ServiceAccountCredentials(st.secrets['client_email'], PathtoKeyFile)
ee.Initialize(EE_CREDENTIALS)
st.write("____________________________________ Initalised______________________________________________")

from GetImageCollections import getImageCollectionbyCoords,TemperatureCorrectionandConversionto
import pandas
import streamlit as st

import matplotlib.pyplot as plt
def PlotBandTimeSeries(TimeSeries,ValueofBand):     
  fig, ax = plt.subplots()
  plt.plot(TimeSeries, ValueofBand)
  st.pyplot(fig)
  
def PlotlyBandTimeSeries(TimeSeries,ValueofBand,yaxesTitle):
      import plotly.express as px
      fig = px.line(results, x='datetime', y=ListofBands)
      fig.update_xaxes(title_text='Time')
      fig.update_yaxes(title_text=yaxesTitle)
      st.plotly_chart(fig)
    
 
#############################################################Read the datasets#################################################################

BandInformation=pandas.read_csv('BandInformation.csv',parse_dates=['StartDate', 'EndDate'])

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
  InputedBand = st.selectbox('Please select the meteorological dataset',BandInformation['Description'])

  if InputedBand is not None:
    RowIndex=BandInformation[BandInformation['Description']==InputedBand].index[0]
    
    ImageCollectionName=BandInformation['ImageCollection'][RowIndex]
    ListofBands=BandInformation['Bands'][RowIndex]
    Resultion=BandInformation['Resultion'][RowIndex]
    StartDate=BandInformation['StartDate'][RowIndex]
    EndDate=BandInformation['EndDate'][RowIndex]
    Latitude=21.0807514
    Longitude= 40.2975893
    
    #TimeSelector = st.date_input("Pick a date", (StartDate, EndDate))
    #st.write("The strating date is:",TimeSelector[0])
    #st.write("The end date is",TimeSelector[1])
    results=getImageCollectionbyCoords(ImageCollectionName=ImageCollectionName,
                                     ListofBands=[ListofBands],
                                     Resultion=int(Resultion),
                                     StartDate=StartDate,
                                     EndDate=EndDate,
                                     Latitude=Latitude,
                                     Longitude=Longitude)
    if (ListofBands=='LST_Day_1km' or 'LST_Night_1km'):
      results[ListofBands]=TemperatureCorrectionandConversionto(results[ListofBands])
      
    
    #PlotBandTimeSeries(results['datetime'], results[ListofBands])
    with SubMainPageDescription:
      PlotlyBandTimeSeries(results['datetime'], results[ListofBands],InputedBand)
################################################################
