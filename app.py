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
import datetime
import plotly.express as px
from datetime import timedelta, date
from PIL import Image
import plotly.express as px
from GetImageCollections import egetImageCollectionbyCountry
#############################################################Read the datasets#################################################################
#BandInformation=pandas.read_csv('BandInformation.csv',delimiter=',',parse_dates=['StartDate', 'EndDate'])
BandInformation=pandas.read_csv('BandInformation.csv',delimiter=',',parse_dates=['StartDate', 'EndDate'],encoding='ISO-8859–1')
Provincesdf=pandas.read_csv('Provinces.csv',delimiter=';')


def plotIndictors(bandName,df):
  fig = px.line(df,x='Timestamp',y=bandName)
  fig.update_xaxes(title_text='Time')
  fig.update_yaxes(title_text=bandName)
  st.plotly_chart(fig,use_container_width=True)

def SillyFunctionToOvercomeCVSColorReadings(temp):
  xxx=temp.split(",")
  colorlist=[]
  for i in range(len(xxx)):
    acolor = ""
    for achar in xxx[i]:
      if achar.isalpha() or achar.isnumeric() :
        acolor=acolor+achar
    colorlist.append(acolor)
  return (colorlist)
  

#############################################################Page Layout starts here############################################################

st.title("CAQLCM of KSA")

MainPageDescription = st.empty() # The main canvas where the input/output is displayed 
SubMainPageDescription=st.empty() # subcanvas where the inputs/outputs are handled 
Sub2MainPageDescription=st.empty() # same as above
Sub3MainPageDescription=st.empty() # same as above
#####################ArabicDescription=Description
lng = st.sidebar.checkbox('Arabic')
if (lng):
  st.sidebar.write("يستخدم هذا التطبيق مجموعه من البيانات المتوفرة من الاقمار الصناعية لتوفيرمراقبة لعدد من مؤشرات المناخ وجودة الهواء والغطاء الأرضي في المملكة العربية السعودية ، الإصدار التجريبي")
  st.sidebar.write("تم  تطويره كمساهمة فى المبادرة السعودية الخضراء ، ستكون تعليقاتكم واقتراحاتكم محل تقدير كبير يمكنكم التواصل عبر")
  st.sidebar.markdown('<a href="mailto:mdbaz01@gamil.com">mdbaz01@gamil.com</a>', unsafe_allow_html=True)
else:
  st.sidebar.write("This app uses some satellite imagery datasets to monitor several climate, Air Quality and Land Cover's parameters of KSA, beta version.")
  st.sidebar.write("Developed as a support for Saudi Green Initiative, your comments and suggestions would be greatly appreciated at:")
  st.sidebar.markdown('<a href="mailto:mdbaz01@gamil.com">mdbaz01@gamil.com</a>', unsafe_allow_html=True)

with st.sidebar.expander('Please select Parameter'):
  InputedBand= st.radio('',BandInformation['Description'])  
  if InputedBand is not None:
    RowIndex=BandInformation[BandInformation['Description']==InputedBand].index[0]  
    ImageCollectionName=BandInformation['ImageCollection'][RowIndex]
    ListofBands=BandInformation['Bands'][RowIndex]
    Resultion=BandInformation['Resultion'][RowIndex]
    StartDate=BandInformation['StartDate'][RowIndex]
    EndDate=BandInformation['EndDate'][RowIndex]
    ColorPlatte=BandInformation['ColorPlatte'][RowIndex]
    ColorPlatte=SillyFunctionToOvercomeCVSColorReadings(ColorPlatte)
    Comments=BandInformation['Links'][RowIndex]
    CorrectionFactor=BandInformation['CorrectionFactor'][RowIndex]
    NumberofDays=BandInformation['NumberofDays'][RowIndex]
    
    TimeSelector = st.date_input("Pick a date", (StartDate, EndDate))
    #st.write("The strating date is:",TimeSelector[0])
    #st.write("The end date is",TimeSelector[1])
    
    

    
    results=egetImageCollectionbyCountry(CountryName='Saudi Arabia',
                                         ImageCollectionName=ImageCollectionName,
                                         BandName=ListofBands,
                                         StartDate=EndDate- timedelta(days=int(NumberofDays)),
                                         EndDate=EndDate,
                                         ColorPlatte=ColorPlatte,
                                         CorrectionFactor=CorrectionFactor
                                        )
    
    with MainPageDescription:
      #st.image(results[1],use_column_width=True,caption=' Image of '+ InputedBand+ ' for the Interval from '+ str(EndDate- timedelta(days=int(NumberofDays)))+' until '+str(EndDate))
   
      image = Image.open(ListofBands+'.gif')
      st.image(image,use_column_width=True,caption=' Image of '+ InputedBand+ ' for the Interval from '+ str(EndDate- timedelta(days=int(NumberofDays)))+' until '+str(EndDate))
   
    with SubMainPageDescription:
      plotIndictors(ListofBands,results[0])
    with Sub2MainPageDescription:
      st.write(results[0])
    with Sub3MainPageDescription:
      st.write("for more information about the dataset, please sse"+Comments)
