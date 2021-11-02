import streamlit as st   
import pandas 
#############################################################Read the datasets#################################################################

BandInformation=pandas.read_csv('BandInformation.csv',delimiter=';',parse_dates=['StartDate', 'EndDate'])
Provinces=pandas.read_csv('Provinces.csv',delimiter=';')

import plotly.express as px
VegetationConditionIndex=pandas.read_csv('VegetationConditionIndex.csv')
Provinces=VegetationConditionIndex['Province'].unique()
def plotIndictors(aProvince,df):
  filteredVegetationConditionIndex=df[df["Province"]==aProvince]
  fig = px.line(filteredVegetationConditionIndex, x='Date', y='Data')
  fig.update_xaxes(title_text='Time')
  fig.update_yaxes(title_text='Vegetation Condition Index of'+aProvince)
  st.plotly_chart(fig)


import base64


file_ = open("movie.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()
st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True,
)
#############################################################Page Layout starts here############################################################

st.title("متابعة الغطاء النباتي نسخة تحت التطوير مهادة الي مبادرة السعودية الخضراء")

MainPageDescription = st.empty() # The main canvas where the input/output is displayed 
SubMainPageDescription=st.empty() # subcanvas where the inputs/outputs are handled 
Sub2MainPageDescription=st.empty() # same as above
Sub3MainPageDescription=st.empty() # same as above

import datetime
with st.sidebar.expander("Please select the dataset we wish to work on"):
  InputedBand = st.selectbox('Please select the meteorological dataset',BandInformation['ArabicDescription'])
  
  if InputedBand is not None:
    RowIndex=BandInformation[BandInformation['ArabicDescription']==InputedBand].index[0]
    ImageCollectionName=BandInformation['ImageCollection'][RowIndex]
    ListofBands=BandInformation['Bands'][RowIndex]
    Resultion=BandInformation['Resultion'][RowIndex]
    StartDate=BandInformation['StartDate'][RowIndex]
    EndDate=BandInformation['EndDate'][RowIndex]
    localdatasource=BandInformation['localdatasource'][RowIndex]
    with Sub2MainPageDescription:
      with st.expander("See explanation"):
        InputedProvince = st.selectbox('Please select the meteorological dataset',Provinces['Province'])
    with Sub3MainPageDescription:
      plotIndictors('Asir',VegetationConditionIndex)
    
##############################

###############################################



