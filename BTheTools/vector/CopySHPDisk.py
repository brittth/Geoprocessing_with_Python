from osgeo import ogr

def CopySHPDisk(layer, outpath):
    drvV = ogr.GetDriverByName('ESRI Shapefile')
    outSHP = drvV.CreateDataSource(outpath) #outpath
    lyr = layer # .GetLayer() #shape
    sett90LYR = outSHP.CopyLayer(lyr, 'lyr')
    del lyr, sett90LYR, outSHP