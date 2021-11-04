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
#####################################################
import streamlit as st   
import pandas
import plotly.express as px
from datetime import timedelta, date
from GetImageCollections import egetImageCollectionbyCountry
#############################################################Read the datasets#################################################################

BandInformation=pandas.read_csv('BandInformation.csv',delimiter=';',parse_dates=['StartDate', 'EndDate'])
Provincesdf=pandas.read_csv('Provinces.csv',delimiter=';')


def plotIndictors(aProvince,df):
  filteredVegetationConditionIndex=df[df["Province"]==aProvince]
  fig = px.line(filteredVegetationConditionIndex, x='Date', y='Data')
  fig.update_xaxes(title_text='Time')
  fig.update_yaxes(title_text='Vegetation Condition Index of'+aProvince)
  st.plotly_chart(fig)


  
def PlotMovieGIF(filename):
  import base64
  file_ = open(filename, "rb")
  contents = file_.read()
  data_url = base64.b64encode(contents).decode("utf-8")
  file_.close()
  st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',unsafe_allow_html=True)
#############################################################Page Layout starts here############################################################

st.title("متابعة الغطاء النباتي نسخة تحت التطوير مهادة الي مبادرة السعودية الخضراء")

MainPageDescription = st.empty() # The main canvas where the input/output is displayed 
SubMainPageDescription=st.empty() # subcanvas where the inputs/outputs are handled 
Sub2MainPageDescription=st.empty() # same as above
with MainPageDescription: 
  col1, col2 = st.columns(2)


import datetime
with st.sidebar.expander('الرجاء اختيار المؤشر'):
  InputedBand = st.selectbox('',BandInformation['ArabicDescription'])
  
  if InputedBand is not None:
    RowIndex=BandInformation[BandInformation['ArabicDescription']==InputedBand].index[0]
    ImageCollectionName=BandInformation['ImageCollection'][RowIndex]
    ListofBands=BandInformation['Bands'][RowIndex]
    Resultion=BandInformation['Resultion'][RowIndex]
    StartDate=BandInformation['StartDate'][RowIndex]
    EndDate=BandInformation['EndDate'][RowIndex]
    TimeSelector = st.date_input("Pick a date", (StartDate, EndDate))
    
    st.write("The strating date is:",TimeSelector[0])
    st.write("The end date is",TimeSelector[1])
    results=egetImageCollectionbyCountry(CountryName=['Saudi Arabia'],
                                 ImageCollectionName=ImageCollectionName,
                                 BandName=ListofBands,
                                 StartDate=StartDate,
                                 EndDate=StartDate+ timedelta(days=10))
    with Sub3MainPageDescription:
      st.write(results[0])

###############################################



