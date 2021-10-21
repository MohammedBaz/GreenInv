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
st.write("____________________________________ Initalised______________________________________________")
import pandas

def GetInformtionFromGoogleEarth(ImageCollectionName,ListofBands,Resultion,StartDate,EndDate,Latitude,Longitude):
  PoI = ee.Geometry.Point(Longitude, Latitude) # Cast Lat and Long into required class
  ImageCollection=ee.ImageCollection(ImageCollectionName) # get the image collecton from google earthengine
  FilteredImageCollections = ImageCollection.select(ListofBands).filterDate(StartDate, EndDate) # apply filter(s):time and/or bands
  results=FilteredImageCollections.getRegion(PoI, Resultion).getInfo() # get the time series of the required bands
  resultsdf=pandas.DataFrame(results) #Cast the results getten from the above to dataframe
  headers = resultsdf.iloc[0] # set the header of dataframe to the first line of the results
  resultsdf = pandas.DataFrame(resultsdf.values[1:], columns=headers) # assign the results to the dataframe and use headers as columns names
  resultsdf = resultsdf.dropna() # drops all rows with no data 
  for band in ListofBands: # Convert the data to numeric values
        resultsdf[band] = pandas.to_numeric(resultsdf[band], errors='coerce')
  resultsdf['datetime'] = pandas.to_datetime(resultsdf['time'], unit='ms') # Convert the time field into a datetime.
  resultsdf = resultsdf[['time','datetime',  *ListofBands]]
  return resultsdf

def TemperatureCorrectionandConversionto(RawData):
   #This funcion is applied to LST_Day_1km bands of MODIS/006/MOD11A1 image collection as
   # the returned readings need to multiplied by correction factor and converted to Celsius
   # here we ignore the QC_Day but it need to be consider at production time, good source can be
   # found at https://spatialthoughts.com/2021/08/19/qa-bands-bitmasks-gee/
   requiredresults =  0.02*RawData - 273.15
   return requiredresults



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
    results=GetInformtionFromGoogleEarth(ImageCollectionName=ImageCollectionName,
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
      
import folium
import streamlit_folium
m = folium.Map(location=[Latitude,Longitude], zoom_start=16)
def add_ee_layer(self, ee_image_object, vis_params, name):
  map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
  folium.raster_layers.TileLayer(
      tiles=map_id_dict['tile_fetcher'].url_format,
      attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
      name=name,
      overlay=True,
      control=True
  ).add_to(self)

folium.Map.add_ee_layer = add_ee_layer

image = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_044034_20140318')

# Define the visualization parameters.
image_viz_params = {
    'bands': ['B5', 'B4', 'B3'],
    'min': 0,
    'max': 0.5,
    'gamma': [0.95, 1.1, 1]
}

# Define a map centered on San Francisco Bay.
map_l8 = folium.Map(location=[37.5010, -122.1899], zoom_start=10)

# Add the image layer to the map and display it.
map_l8.add_ee_layer(image, image_viz_params, 'false color composite')
display(map_l8)




""""
tile_layer = folium.TileLayer(
    tiles="https://{s}.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}.png",
    attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    max_zoom=19,
    name='darkmatter',
    control=False,
    opacity=0.7
)
tile_layer.add_to(m)
"""

streamlit_folium.folium_static(m)

 
