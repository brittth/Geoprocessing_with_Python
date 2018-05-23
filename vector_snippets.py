# #### LOAD REQUIRED LIBRARIES #### #
import time
try:
    from osgeo import ogr
except:
    import ogr

# E-Mails
# britta.themann@hu-berlin.de
# poetzscf@hu-berlin.de
# juliastolper@hotmail.de

# #### FUNCTIONS #### #
# prints all available layers in a folder
def print_layers(fn):
    ds = ogr.Open(fn, 0)
    if ds is None:
        raise OSError('Could not open {}'.format(fn))
    for i in range(ds.GetLayerCount()):
        lyr = ds.GetLayer(i)
        print('{0}: {1}'.format(i, lyr.GetName()))

# #### FOLDER PATHS & global variables #### #
wd = 'O:/Student_Data/CJaenicke/04_SoSe_18/GeoPython/data/Assignment04/'

# #### PROCESSING #### #
# prints the available layers in the workind directory
print_layers(wd)

#Open a shapefile
countries = ogr.Open(wd+"gadm36_dissolve.shp")
protected = ogr.Open(wd+"WDPA_May2018-shapefile-polygons.shp")

#Opening a layer
layer_countries = countries.GetLayer()
layer_protected = protected.GetLayer()

#Get number of features in layer
#Attention: overload for python
numFeatures = layer_countries.GetFeatureCount()
print('Feature count: ' + str(numFeatures))

#Get extent as tuple
extent = layer_countries.GetExtent()
print('Extent:', extent)

#Get a specfic Feature via Index
feature_countries = layer_countries.GetFeature(1)

#Getting a features attribute, in this case simply the ID
id = feature_countries.GetField('ID_0')
name = feature_countries.GetField('NAME_0')
print('ID:', id, '\n Name:', name)

#Loops over all features, extracts and prints the ID and the name
feature_countries = layer_countries.GetNextFeature()
while feature_countries:
    #processing steps
    id = feature_countries.GetField('ID_0')
    name = feature_countries.GetField('NAME_0')
    print('ID:', id, '\n Name:', name)
    feature_countries = layer_countries.GetNextFeature()
layer_countries.ResetReading() #necessary if looping again

#Getting a feature's geometry
geometry = feature.GetGeometryRef()
geometry_countries = feature_countries.GetGeometryRef()

#FILTER
#This should work now like this, just takes some time.
#only example for one country
#See Garrard page 27 pp

#Set Spatial Filter
layer_countries.SetAttributeFilter("NAME_0 = 'Germany'") #filters the countries layer for Germany
feature_countries = layer_countries.GetNextFeature() #gets the first feature from the filtered layer
country = feature_countries.geometry().Clone() #copies geometry of this feature so that python will not try to change the actual feature
layer_protected.SetSpatialFilter(country) #then sets the spatial filter in the protected areas layer with help of the copied geometry

#further processing, e.g. counting the features in the filter
feat_count = layer_protected.GetFeatureCount() #this should count all protected areas in germany

#destroy objects for data management purposes
feature.Destroy()
dataSource.Destroy()