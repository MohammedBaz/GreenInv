import ee
import pandas

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
