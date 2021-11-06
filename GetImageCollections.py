import ee
import pandas
import streamlit as st

def getImageCollectionbyCoords(ImageCollectionName,ListofBands,Resultion,StartDate,EndDate,Latitude,Longitude):
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
  return (resultsdf)

def TemperatureCorrectionandConversionto(RawData):
   #This funcion is applied to LST_Day_1km bands of MODIS/006/MOD11A1 image collection as
   # the returned readings need to multiplied by correction factor and converted to Celsius
   # here we ignore the QC_Day but it need to be consider at production time, good source can be
   # found at https://spatialthoughts.com/2021/08/19/qa-bands-bitmasks-gee/
   requiredresults =  0.02*RawData - 273.15
   return (requiredresults)
#############################################https://developers.google.com/earth-engine/tutorials/community/time-series-visualization-with-altair#

def create_reduce_region_function(geometry,reducer=ee.Reducer.mean(),scale=1000,crs='EPSG:4326',bestEffort=True,maxPixels=1e13,tileScale=4):
  def reduce_region_function(img):
    stat = img.reduceRegion(reducer=reducer,geometry=geometry,scale=scale,crs=crs,bestEffort=bestEffort,maxPixels=maxPixels,tileScale=tileScale)
    return ee.Feature(geometry, stat).set({'millis': img.date().millis()})
  return reduce_region_function

def fc_to_dict(fc):
  prop_names = fc.first().propertyNames()
  prop_lists = fc.reduceColumns(
      reducer=ee.Reducer.toList().repeat(prop_names.size()),
      selectors=prop_names).get('list')
  return ee.Dictionary.fromLists(prop_names, prop_lists)

def add_date_info(df):
  df['Timestamp'] = pandas.to_datetime(df['millis'], unit='ms')
  df['Year'] = pandas.DatetimeIndex(df['Timestamp']).year
  df['Month'] = pandas.DatetimeIndex(df['Timestamp']).month
  df['Day'] = pandas.DatetimeIndex(df['Timestamp']).day
  df['DOY'] = pandas.DatetimeIndex(df['Timestamp']).dayofyear
  return df


@st.cache
def egetImageCollectionbyCountry(CountryName,ImageCollectionName,BandName,StartDate,EndDate,ColorPlatte,CorrectionFactor):
  aCountry = ee.FeatureCollection("FAO/GAUL/2015/level0").filter(ee.Filter.eq('ADM0_NAME', CountryName))
  aoi=aCountry.geometry()
  date_range=ee.DateRange(StartDate, EndDate)
  mapBands = ee.ImageCollection(ImageCollectionName).filterDate(date_range).select(BandName).filterBounds(aoi)
  reducedMapBands = create_reduce_region_function(
    geometry=aoi, reducer=ee.Reducer.mean(), scale=1000, crs='EPSG:3310')
  reducedMapBandsFeatureCollection = ee.FeatureCollection(mapBands.map(reducedMapBands)).filter(
    ee.Filter.notNull(mapBands.first().bandNames()))
  reducedMapBandsFeatureCollectionDictionary = fc_to_dict(reducedMapBandsFeatureCollection).getInfo()
  reducedMapBandsFeatureCollectionDataFrame = pandas.DataFrame(reducedMapBandsFeatureCollectionDictionary)
  if (BandName=='LST_Day_1km' or 'LST_Night_1km'):
    reducedMapBandsFeatureCollectionDataFrame[BandName]=TemperatureCorrectionandConversionto(reducedMapBandsFeatureCollectionDataFrame[BandName])
  else:
    reducedMapBandsFeatureCollectionDataFrame[BandName]=reducedMapBandsFeatureCollectionDataFrame[BandName]*CorrectionFactor
  reducedMapBandsFeatureCollectionDataFrame=add_date_info(reducedMapBandsFeatureCollectionDataFrame)
  ####################generate imageThumburl
  BandMean=mapBands.mean()
  BandMean=BandMean.clip(aoi)
  if (BandName=='LST_Day_1km' or 'LST_Night_1km'):
    BandMean=BandMean.multiply(0.02)
    BandMean=BandMean.add(-273.15)
  # here we assigns the min and max of the color palette to the min and max of the band respectively, other statistical measures such as:
  #  std(), mean(),median(),quantile(0.1) which is 10th percentile,quantile(0.9) which is 90th percentile can be used also. 
  url = BandMean.getThumbUrl({
    'min':reducedMapBandsFeatureCollectionDataFrame[BandName].min(), 'max':reducedMapBandsFeatureCollectionDataFrame[BandName].max(),
     'dimensions': 512, 'region': aoi,
    'palette': ColorPlatte})
  return(reducedMapBandsFeatureCollectionDataFrame, url)







"""
def getImageCollectionbyCountry(CountryName,ImageCollectionName,BandName,StartDate,EndDate,CorrectionFactor):
  aCountry = ee.FeatureCollection("FAO/GAUL/2015/level0").filter(ee.Filter.eq('ADM0_NAME', CountryName))
  aoi=aCountry.geometry()
  date_range=ee.DateRange(StartDate, EndDate)
  mapBands = ee.ImageCollection(ImageCollectionName).filterDate(date_range).select(BandName)
  reducedMapBands = create_reduce_region_function(
    geometry=aoi, reducer=ee.Reducer.mean(), scale=1000, crs='EPSG:3310')
  reducedMapBandsFeatureCollection = ee.FeatureCollection(mapBands.map(reducedMapBands)).filter(
    ee.Filter.notNull(mapBands.first().bandNames()))
  reducedMapBandsFeatureCollectionDictionary = fc_to_dict(reducedMapBandsFeatureCollection).getInfo()
  reducedMapBandsFeatureCollectionDataFrame = pandas.DataFrame(reducedMapBandsFeatureCollectionDictionary)
  reducedMapBandsFeatureCollectionDataFrame[BandName]=reducedMapBandsFeatureCollectionDataFrame[BandName]/10000
  reducedMapBandsFeatureCollectionDataFrame=add_date_info(reducedMapBandsFeatureCollectionDataFrame)
  reducedMapBandsFeatureCollectionDataFrame.head(5)
  return(reducedMapBandsFeatureCollectionDataFrame)


def egetImageCollectionbyCountry(CountryName,ImageCollectionName,BandName,StartDate,EndDate):
  aCountry = ee.FeatureCollection("FAO/GAUL/2015/level0").filter(ee.Filter.inList('ADM0_NAME', CountryName))
  aoi=aCountry.geometry()
  date_range=ee.DateRange(StartDate, EndDate)
  mapBands = ee.ImageCollection(ImageCollectionName).filterDate(date_range).select(BandName)
  reducedMapBands = create_reduce_region_function(
    geometry=aoi, reducer=ee.Reducer.mean(), scale=1000, crs='EPSG:3310')
  reducedMapBandsFeatureCollection = ee.FeatureCollection(mapBands.map(reducedMapBands)).filter(
    ee.Filter.notNull(mapBands.first().bandNames()))
  reducedMapBandsFeatureCollectionDictionary = fc_to_dict(reducedMapBandsFeatureCollection).getInfo()
  reducedMapBandsFeatureCollectionDataFrame = pandas.DataFrame(reducedMapBandsFeatureCollectionDictionary)
  if (BandName=='LST_Day_1km' or 'LST_Night_1km'):
    reducedMapBandsFeatureCollectionDataFrame[BandName]=TemperatureCorrectionandConversionto(reducedMapBandsFeatureCollectionDataFrame[BandName])
  else:
    reducedMapBandsFeatureCollectionDataFrame[BandName]=reducedMapBandsFeatureCollectionDataFrame[BandName]/10000
  reducedMapBandsFeatureCollectionDataFrame=add_date_info(reducedMapBandsFeatureCollectionDataFrame)
  ####################generate imageThumburl
  BandMean=mapBands.mean()
  BandMean=BandMean.clip(aoi)
  if (BandName=='LST_Day_1km' or 'LST_Night_1km'):
    BandMean=BandMean.multiply(0.02)
    BandMean=BandMean.add(-273.15)
  # here we assigns the min and max of the color palette to the min and max of the band respectively, other statistical measures such as:
  #  std(), mean(),median(),quantile(0.1) which is 10th percentile,quantile(0.9) which is 90th percentile can be used also. 
  url = BandMean.getThumbUrl({
    'min':reducedMapBandsFeatureCollectionDataFrame[BandName].min(), 'max':reducedMapBandsFeatureCollectionDataFrame[BandName].max(),
     'dimensions': 512, 'region': aoi,
    'palette': ['blue', 'yellow', 'orange', 'red']})
  return(reducedMapBandsFeatureCollectionDataFrame, url)





def egetImageCollectionbyCountry(CountryName,ImageCollectionName,BandName,StartDate,EndDate):
  aCountry = ee.FeatureCollection("FAO/GAUL/2015/level0").filter(ee.Filter.inList('ADM0_NAME', CountryName))
  aoi=aCountry.geometry()
  date_range=ee.DateRange(StartDate, EndDate)
  mapBands = ee.ImageCollection(ImageCollectionName).filterDate(date_range).select(BandName)
  reducedMapBands = create_reduce_region_function(
    geometry=aoi, reducer=ee.Reducer.mean(), scale=1000, crs='EPSG:3310')
  reducedMapBandsFeatureCollection = ee.FeatureCollection(mapBands.map(reducedMapBands)).filter(
    ee.Filter.notNull(mapBands.first().bandNames()))
  reducedMapBandsFeatureCollectionDictionary = fc_to_dict(reducedMapBandsFeatureCollection).getInfo()
  reducedMapBandsFeatureCollectionDataFrame = pandas.DataFrame(reducedMapBandsFeatureCollectionDictionary)
  reducedMapBandsFeatureCollectionDataFrame[BandName]=reducedMapBandsFeatureCollectionDataFrame[BandName]/10000
  reducedMapBandsFeatureCollectionDataFrame=add_date_info(reducedMapBandsFeatureCollectionDataFrame)
  ####################generate imageThumburl
  BandMean=mapBands.mean()
  url = BandMean.getThumbUrl({
    'min': min(reducedMapBandsFeatureCollectionDataFrame[BandName]), 'max': max(reducedMapBandsFeatureCollectionDataFrame[BandName]),
     'dimensions': 512, 'region': aoi,
    'palette': ['blue', 'yellow', 'orange', 'red']})
  return(reducedMapBandsFeatureCollectionDataFrame, url)
"""
