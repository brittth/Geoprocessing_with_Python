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
ctest = ogr.Open(wd+"ctest.shp")

#Opening a layer
layer_countries = countries.GetLayer()
layer_protected = protected.GetLayer()
layer_ctest = ctest.GetLayer()

#OUR LOOP
num_countries = layer_ctest.GetFeatureCount()
nums = list(range(0,num_countries))
#print(nums)

clist = []
for index in nums:
    #Get a specfic Feature via Index
    clist.append(layer_countries.GetFeature(index))
#print(clist)

for country in clist:
    #Country Spatial Filter
    id = country.GetField('ID_0')
    name = country.GetField('NAME_0')
    layer_countries.SetAttributeFilter("NAME_0 ='" + name + "'")
    countryshp = country.geometry().Clone()
    layer_protected.SetSpatialFilter(countryshp)
    #Protected Basic Attribute Filter
    layer_protected.SetAttributeFilter("STATUS = 'Designated'")#   STATUS == Established OR Designated --> Established muss noch dazu, hat mit OR nicht funktioniert
    layer_protected.SetAttributeFilter("MARINE = '0'")#   MARINE string [0 (terrestrial), 1 (coastal), 2 (marine)];
    feature_count = layer_protected.GetFeatureCount()
    #Protected Category Filters
    # Ia
    layer_protected.SetAttributeFilter("IUCN_CAT = 'Ia'")# IUCN_CAT    string  [1-VI, not reported, not applicable] --> Andere Kategorien fehlen noch
    feature_countIa=layer_protected.GetFeatureCount()
    layer_protected.SetAttributeFilter(None)
    # Ib
    layer_protected.SetAttributeFilter("STATUS = 'Designated'")# Wiederholt von oben
    layer_protected.SetAttributeFilter("MARINE = '0'")
    layer_protected.SetAttributeFilter("IUCN_CAT = 'Ib'")
    feature_countIb = layer_protected.GetFeatureCount()
    layer_protected.SetAttributeFilter(None)
    # HIER KOMMEN ALLE ANDEREN FILTER NOCH NACH DEM GLEICHEN PRINZIP
    layer_protected.SetSpatialFilter(None)
    print('Country ID: ',id,'\n',
          'Country Name:',name,'\n',
          'PA Category: noch nichts','\n',
          '# PAs:', feature_count,'\n',
          'PA Category Ia: ', feature_countIa,'\n',
          'PA Category Ib: ', feature_countIb,'\n',
          'Mean area of PAs: noch nichts','\n',
          'Area of largest PA: noch nichts','\n',
          'Name of largest PA: noch nichts','\n',
          'Year of etsabl. of largest PA: noch nichs\n\n')




# #### END TIME-COUNT AND PRINT TIME STATS #### #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")