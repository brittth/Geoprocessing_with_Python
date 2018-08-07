from osgeo import osr

def SpatialReferenceFromRaster(ds):
    #Returns SpatialReference from raster dataset
    pr = ds.GetProjection()
    sr = osr.SpatialReference()
    sr.ImportFromWkt(pr)
    return sr