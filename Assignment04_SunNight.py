import time
from osgeo import ogr
import pandas

# #### SET TIME-COUNT #### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")


lycoun = 'D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 6 - Vector processing I/Assignment04_data/ctest.shp'
lypa   = 'D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 6 - Vector processing I/Assignment04_data/WDPA_May2018-shapefile-polygons.shp'

country = ogr.Open(lycoun)
pas     = ogr.Open(lypa)

cl = country.GetLayer()
pl = pas.GetLayer()
pl.SetAttributeFilter("MARINE='0'" and ("STATUS = 'Designated'" or "STATUS = 'Established'"))


k = ['Country ID', 'Country Name', 'PA Category', '# PAs', 'Mean area of PAs', 'Area of largest PA', 'Name of largest PA', 'Year of establ. of largest PA', 'PA Area', 'PA Name']
v = [[], [], [], [], [], [], [], [], [], []]
r = dict(zip(k, v))


for feat in cl:
    extr = feat.geometry().Clone()
    pl.SetSpatialFilter(extr)
    print(feat.GetField('Name_0'))
    r['PA Category'].append('ALL')

    for sub in pl:
        r['Country ID'].append(feat.GetField('ID_0'))
        r['Country Name'].append(feat.GetField('NAME_0'))
        r['PA Category'].append(sub.GetField('IUCN_CAT'))
        r['PA Name'].append(sub.GetField('NAME'))
        r['Year of establ. of largest PA'].append(sub.GetField('STATUS_YR'))
        r['PA Area'].append(sub.GetField('GIS_AREA'))

    # Ia
    pl.SetAttributeFilter("IUCN_CAT ='Ia'")
    countIa = pl.GetFeatureCount()
    meanIa = sum(r['PA Area']) / len(r['PA Area'])
    maxIa = max(r['PA Area'])
    index = r['PA Area'].index(maxIa)
    nameIa = (r['PA Name'][index])
    pl.SetAttributeFilter(None)
    pl.SetAttributeFilter("MARINE='0'" and ("STATUS = 'Designated'" or "STATUS = 'Established'"))

    # Ib
    pl.SetAttributeFilter("IUCN_CAT ='b'")
    countIb = pl.GetFeatureCount()
    meanIb = sum(r['PA Area']) / len(r['PA Area'])
    maxIb = max(r['PA Area'])
    index = r['PA Area'].index(maxIb)
    nameIb = (r['PA Name'][index])
    pl.SetAttributeFilter(None)
    pl.SetAttributeFilter("MARINE='0'" and ("STATUS = 'Designated'" or "STATUS = 'Established'"))

    # II
    pl.SetAttributeFilter("IUCN_CAT ='II'")
    countII = pl.GetFeatureCount()
    meanII = sum(r['PA Area']) / len(r['PA Area'])
    maxII = max(r['PA Area'])
    index = r['PA Area'].index(maxII)
    nameII = (r['PA Name'][index])
    pl.SetAttributeFilter(None)
    pl.SetAttributeFilter("MARINE='0'" and ("STATUS = 'Designated'" or "STATUS = 'Established'"))

    # III
    pl.SetAttributeFilter("IUCN_CAT ='III'")
    countIII = pl.GetFeatureCount()
    meanIII = sum(r['PA Area']) / len(r['PA Area'])
    maxIII = max(r['PA Area'])
    index = r['PA Area'].index(maxIII)
    nameIII = (r['PA Name'][index])
    pl.SetAttributeFilter(None)
    pl.SetAttributeFilter("MARINE='0'" and ("STATUS = 'Designated'" or "STATUS = 'Established'"))

    # IV
    pl.SetAttributeFilter("IUCN_CAT ='IV'")
    countIV = pl.GetFeatureCount()
    meanIV = sum(r['PA Area']) / len(r['PA Area'])
    maxIV = max(r['PA Area'])
    index = r['PA Area'].index(maxIV)
    nameIV = (r['PA Name'][index])
    pl.SetAttributeFilter(None)
    pl.SetAttributeFilter("MARINE='0'" and ("STATUS = 'Designated'" or "STATUS = 'Established'"))

    # V
    pl.SetAttributeFilter("IUCN_CAT ='V'")
    countV = pl.GetFeatureCount()
    meanV = sum(r['PA Area']) / len(r['PA Area'])
    maxV = max(r['PA Area'])
    index = r['PA Area'].index(maxV)
    nameV = (r['PA Name'][index])
    pl.SetAttributeFilter(None)
    pl.SetAttributeFilter("MARINE='0'" and ("STATUS = 'Designated'" or "STATUS = 'Established'"))

    # VI
    pl.SetAttributeFilter("IUCN_CAT ='VI'")
    countVI = pl.GetFeatureCount()
    meanVI = sum(r['PA Area']) / len(r['PA Area'])
    maxVI = max(r['PA Area'])
    index = r['PA Area'].index(maxVI)
    nameVI = (r['PA Name'][index])
    pl.SetAttributeFilter(None)
    pl.SetAttributeFilter("MARINE='0'" and ("STATUS = 'Designated'" or "STATUS = 'Established'"))

    # Not Applicable
    pl.SetAttributeFilter("IUCN_CAT ='Not Applicable'")
    countNotApplicable = pl.GetFeatureCount()
    meanNotApplicable = sum(r['PA Area']) / len(r['PA Area'])
    maxNotApplicable = max(r['PA Area'])
    index = r['PA Area'].index(maxNotApplicable)
    nameNotApplicable = (r['PA Name'][index])
    pl.SetAttributeFilter(None)
    pl.SetAttributeFilter("MARINE='0'" and ("STATUS = 'Designated'" or "STATUS = 'Established'"))

    # Not Reported
    pl.SetAttributeFilter("IUCN_CAT ='Not Reported'")
    countNotReported = pl.GetFeatureCount()
    meanNotReported = sum(r['PA Area']) / len(r['PA Area'])
    maxNotReported = max(r['PA Area'])
    index = r['PA Area'].index(maxNotReported)
    nameNotReported = (r['PA Name'][index])
    pl.SetAttributeFilter(None)
    pl.SetAttributeFilter("MARINE='0'" and ("STATUS = 'Designated'" or "STATUS = 'Established'"))

    ## PAs
    count = pl.GetFeatureCount()
    r['# PAs'].append(count)
    r['# PAs'].append(countIa)
    r['# PAs'].append(countIb)
    r['# PAs'].append(countII)
    r['# PAs'].append(countIII)
    r['# PAs'].append(countIV)
    r['# PAs'].append(countV)
    r['# PAs'].append(countVI)
    r['# PAs'].append(countNotApplicable)
    r['# PAs'].append(countNotReported)

    #Mean Area of PA
    mean = sum(r['PA Area'])/len(r['PA Area'])
    r['Mean area of PAs'].append(mean)
    r['Mean area of PAs'].append(meanIa)
    r['Mean area of PAs'].append(meanIb)
    r['Mean area of PAs'].append(meanII)
    r['Mean area of PAs'].append(meanIII)
    r['Mean area of PAs'].append(meanIV)
    r['Mean area of PAs'].append(meanV)
    r['Mean area of PAs'].append(meanVI)
    r['Mean area of PAs'].append(meanNotApplicable)
    r['Mean area of PAs'].append(meanNotReported)

    #Area of largest PA
    max = max(r['PA Area'])
    r['Area of largest PA'].append(max)
    r['Area of largest PA'].append(maxIa)
    r['Area of largest PA'].append(maxIb)
    r['Area of largest PA'].append(maxII)
    r['Area of largest PA'].append(maxIII)
    r['Area of largest PA'].append(maxIV)
    r['Area of largest PA'].append(maxV)
    r['Area of largest PA'].append(maxVI)
    r['Area of largest PA'].append(maxNotApplicable)
    r['Area of largest PA'].append(maxNotReported)

    #Name of largest PA
    index = r['PA Area'].index(max)
    name = (r['PA Name'][index])
    r['Name of largest PA'].append(name)
    r['Name of largest PA'].append(nameIa)
    r['Name of largest PA'].append(nameIb)
    r['Name of largest PA'].append(nameII)
    r['Name of largest PA'].append(nameIII)
    r['Name of largest PA'].append(nameIV)
    r['Name of largest PA'].append(nameV)
    r['Name of largest PA'].append(nameVI)
    r['Name of largest PA'].append(nameNotApplicable)
    r['Name of largest PA'].append(nameNotReported)

    pl.SetSpatialFilter(None)

#only needed for loop
del r['PA Area']
del r['PA Name']

df = pandas.DataFrame(data=r)

df.to_csv('D:/Britta/Documents/HU Berlin/SS 18/Geoprocessing with Python/Week 6 - Vector processing I/Assignment04_data/inter.csv', sep=',',index=False)

cl.ResetReading() # sets country's starting feature to zero


# #### END TIME-COUNT AND PRINT TIME STATS #### #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")