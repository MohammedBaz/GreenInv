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
################################################################



import folium
import streamlit_folium
from folium import plugins
from folium.plugins import MeasureControl

from folium.plugins import MousePosition


aoi = ee.FeatureCollection('EPA/Ecoregions/2013/L3').filter(
    ee.Filter.eq('na_l3name', 'Sierra Nevada')).geometry()

# Define a method for displaying Earth Engine image tiles to folium map.
def add_ee_layer(self, ee_image_object, vis_params, name):
  map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
  folium.raster_layers.TileLayer(
      tiles=map_id_dict['tile_fetcher'].url_format,
      attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine, USDA National Agriculture Imagery Program</a>',
      name=name,
      overlay=True,
      control=True).add_to(self)

# Add an Earth Engine layer drawing method to folium.
folium.Map.add_ee_layer = add_ee_layer

# Import a NAIP image for the area and date of interest.
naip_img = ee.ImageCollection('USDA/NAIP/DOQQ').filterDate(
    '2016-01-01',
    '2017-01-01').filterBounds(ee.Geometry.Point([-118.6407, 35.9665])).first()

# Display the NAIP image to the folium map.
m = folium.Map(location=[35.9665, -118.6407], tiles='Stamen Terrain', zoom_start=16)
m.add_ee_layer(naip_img, None, 'NAIP image, 2016')
m.add_child(MeasureControl())
# Add the point of interest to the map.
folium.Circle(
    radius=15,
    location=[35.9665, -118.6407],
    color='yellow',
    fill=False,
).add_to(m)

# Add the AOI to the map.
folium.GeoJson(
  aoi.getInfo(),
  name='geojson',
  style_function=lambda x: {'fillColor': '#00000000', 'color': '#000000'},
).add_to(m)

# Add a lat lon popup.
folium.LatLngPopup().add_to(m)
st.write(folium.LatLngPopup())

formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
st.write(formatter)
MousePosition(
    position="topright",
    separator=" | ",
    empty_string="NaN",
    lng_first=True,
    num_digits=20,
    prefix="Coordinates:",
    lat_formatter=formatter,
    lng_formatter=formatter,
).add_to(m)



# Display the map.
streamlit_folium.folium_static(m)

##########################
m = plugins.DualMap(location=(52.1, 5.1), tiles=None, zoom_start=8)

folium.TileLayer("cartodbpositron").add_to(m.m2)
folium.TileLayer("openstreetmap").add_to(m)

fg_both = folium.FeatureGroup(name="markers_both").add_to(m)
fg_1 = folium.FeatureGroup(name="markers_1").add_to(m.m1)
fg_2 = folium.FeatureGroup(name="markers_2").add_to(m.m2)

icon_red = folium.Icon(color="red")
folium.Marker((52, 5), tooltip="both", icon=icon_red).add_to(fg_both)
folium.Marker((52.4, 5), tooltip="left").add_to(fg_1)
folium.Marker((52, 5.4), tooltip="right").add_to(fg_2)

folium.LayerControl(collapsed=False).add_to(m)
streamlit_folium.folium_static(m)
##########################################
from owslib.wms import WebMapService


url = "https://pae-paha.pacioos.hawaii.edu/thredds/wms/dhw_5km?service=WMS"

web_map_services = WebMapService(url)

print("\n".join(web_map_services.contents.keys()))
layer = "CRW_SST"
wms = web_map_services.contents[layer]

name = wms.title

lon = (wms.boundingBox[0] + wms.boundingBox[2]) / 2.0
lat = (wms.boundingBox[1] + wms.boundingBox[3]) / 2.0
center = lat, lon

time_interval = "{0}/{1}".format(
    wms.timepositions[0].strip(), wms.timepositions[-1].strip()
)
style = "boxfill/sst_36"

if style not in wms.styles:
    style = None




import folium
from folium import plugins

lon, lat = -50, -40

m = folium.Map(location=[lat, lon], zoom_start=5, control_scale=True)

w = folium.raster_layers.WmsTileLayer(
    url=url,
    name=name,
    styles=style,
    fmt="image/png",
    transparent=True,
    layers=layer,
    overlay=True,
    COLORSCALERANGE="1.2,28",
)

w.add_to(m)

time = plugins.TimestampedWmsTileLayers(w, period="PT1H", time_interval=time_interval)

time.add_to(m)

folium.LayerControl().add_to(m)
streamlit_folium.folium_static(m)
#https://nbviewer.org/github/python-visualization/folium/blob/master/examples/WmsTimeDimension.ipynb

