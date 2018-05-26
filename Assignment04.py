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
# #   GIS_AREA    double
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
    layer_protected.SetAttributeFilter("MARINE='0'" and ("STATUS='Designated' or STATUS='Established'"))
    feature_count = layer_protected.GetFeatureCount()

    #Protected Category Filters
        # IUCN_CAT
    # Ia
    layer_protected.SetAttributeFilter("IUCN_CAT = 'Ia'")
    feature_countIa=layer_protected.GetFeatureCount()
    layer_protected.SetAttributeFilter(None)
    # Ib
    layer_protected.SetAttributeFilter("MARINE='0'" and ("STATUS='Designated' or STATUS='Established'"))
    layer_protected.SetAttributeFilter("IUCN_CAT = 'Ib'")
    feature_countIb = layer_protected.GetFeatureCount()
    layer_protected.SetAttributeFilter(None)
    # II
    layer_protected.SetAttributeFilter("MARINE='0'" and ("STATUS='Designated' or STATUS='Established'"))
    layer_protected.SetAttributeFilter("IUCN_CAT = 'II'")
    feature_countII = layer_protected.GetFeatureCount()
    layer_protected.SetAttributeFilter(None)
    # III
    layer_protected.SetAttributeFilter("MARINE='0'" and ("STATUS='Designated' or STATUS='Established'"))
    layer_protected.SetAttributeFilter("IUCN_CAT = 'III'")
    feature_countIII = layer_protected.GetFeatureCount()
    layer_protected.SetAttributeFilter(None)
    # IV
    layer_protected.SetAttributeFilter("MARINE='0'" and ("STATUS='Designated' or STATUS='Established'"))
    layer_protected.SetAttributeFilter("IUCN_CAT = 'IV'")
    feature_countIV = layer_protected.GetFeatureCount()
    layer_protected.SetAttributeFilter(None)
    # V
    layer_protected.SetAttributeFilter("MARINE='0'" and ("STATUS='Designated' or STATUS='Established'"))
    layer_protected.SetAttributeFilter("IUCN_CAT = 'V'")
    feature_countV = layer_protected.GetFeatureCount()
    layer_protected.SetAttributeFilter(None)
    # VI
    layer_protected.SetAttributeFilter("MARINE='0'" and ("STATUS='Designated' or STATUS='Established'"))
    layer_protected.SetAttributeFilter("IUCN_CAT = 'VI'")
    feature_countVI = layer_protected.GetFeatureCount()
    layer_protected.SetAttributeFilter(None)
    # Not Applicable
    layer_protected.SetAttributeFilter("MARINE='0'" and ("STATUS='Designated' or STATUS='Established'"))
    layer_protected.SetAttributeFilter("IUCN_CAT = 'Not Applicable'")
    feature_countNotApplicable = layer_protected.GetFeatureCount()
    layer_protected.SetAttributeFilter(None)
    # Not Reported
    layer_protected.SetAttributeFilter("MARINE='0'" and ("STATUS='Designated' or STATUS='Established'"))
    layer_protected.SetAttributeFilter("IUCN_CAT = 'Not Reported'")
    feature_countNotReported = layer_protected.GetFeatureCount()
    layer_protected.SetAttributeFilter(None)
        #GIS_AREA
    layer_protected.SetAttributeFilter("MARINE='0'" and ("STATUS='Designated' or STATUS='Established'"))
    #Weiß nicht wie man eine ganze Spalte gleichzeitig anspricht, bzw. geht ja eigentlich nicht in dieser for schleife
    # meanArea
    # maxArea
    # maxAreaName
        #STATUS_YR
    layer_protected.SetAttributeFilter("MARINE='0'" and ("STATUS='Designated' or STATUS='Established'"))
    #statusYr = layer_protected.GetField('STATUS_YR') #ERROR

    layer_protected.SetSpatialFilter(None)
    print('Country ID: ',id,'\n',
          'Country Name:',name,'\n',
          '# PAs:', feature_count,'\n',
          'PA Category Ia: ', feature_countIa,'\n',
          'PA Category Ib: ', feature_countIb,'\n',
          'PA Category II: ', feature_countII, '\n',
          'PA Category III: ', feature_countIII, '\n',
          'PA Category IV: ', feature_countIV, '\n',
          'PA Category V: ', feature_countV, '\n',
          'PA Category VI: ', feature_countVI, '\n',
          'PA Category Not Applicable: ', feature_countNotApplicable, '\n',
          'PA Category Not Reported: ', feature_countNotReported, '\n',
          'Mean area of PAs: meanArea -> noch nichts','\n',
          'Area of largest PA: maxArea -> noch nichts','\n',
          'Name of largest PA: maxAreaName -> noch nichts','\n',
          'Year of etsabl. of largest PA: statusYr ERROR\n\n') #ERROR

# #### END TIME-COUNT AND PRINT TIME STATS #### #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")