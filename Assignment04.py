## Group II – the SHP/GIS-group
# IUCN: I-VI, no data values (not reported, Not Applicable)

#SQL query:
#   MARINE == 0
#   STATUS == established OR designated

# set spatial filter (intersect) loop over countries and append attributed of PA's

# needed variables:
#   country
#   MARINE      string  [0 (terrestrial), 1 (coastal), 2 (marine)];
#   IUCN_CAT    string  [1-VI, not reported, not applicable]
#   NAME        string
#   STATUS_YR   string
#   GIS_AREA    double
#   STATUS      string (only designated & established)

#buch s. 27
#clejae

# E-Mails
# britta.themann@hu-berlin.de
# poetzscf@hu-berlin.de
# juliastolper@hotmail.de

# #### LOAD REQUIRED LIBRARIES #### #
import time
try:
    from osgeo import ogr
except:
    import ogr

# #### SET TIME-COUNT #### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# #### FUNCTIONS #### #

# #### FOLDER PATHS & global variables #### #
#wd = 'O:/Student_Data/CJaenicke/04_SoSe_18/GeoPython/data/Assignment04/'
wd = 'D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 6 - Vector processing I/Assignment04_data/'

# #### PROCESSING #### #
#Open a shapefile
countries = ogr.Open(wd+"gadm36_dissolve.shp")
protected = ogr.Open(wd+"WDPA_May2018-shapefile-polygons.shp")
#Opening a layer
layer_countries = countries.GetLayer()
layer_protected = protected.GetLayer()

#OUR LOOP
feature_countries = layer_countries.GetNextFeature()
while feature_countries:
    # get info from country layer
    name = feature_countries.GetField('NAME_0')
    layer_countries.SetAttributeFilter("NAME_0 ='"+name+"'")
    feature_countries = layer_countries.GetNextFeature()
    country = feature_countries.geometry().Clone()
    layer_protected.SetSpatialFilter(country)
    feature_count = layer_protected.GetFeatureCount()           #works till here
    layer_protected.SetSpatialFilter(None)                      #no error, but doesn't do anything either
        # Probably in the next code line is the problem,
        # since the filter on the layer_countries is still active
        # which results in the layer containing only one feature.
        # I tried already to work with a second layer_countries,
        # but somewhoe this didn't work.
        # And it doesn't seem like a good solution.
    feature_countries = layer_countries.GetNextFeature()
    print('Name:', name, '#Protected Areas:', feature_count)
layer_countries.ResetReading() #necessary if looping again


# #### END TIME-COUNT AND PRINT TIME STATS #### #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")