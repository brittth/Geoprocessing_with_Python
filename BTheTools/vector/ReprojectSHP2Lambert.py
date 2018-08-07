import geopandas as gpd
from osgeo import ogr

def ReprojectSHP2Lambert(file_path, wd, outfile_name): #tb tested
    ds = gpd.read_file(file_path)
    ds_lambert = ds.to_crs({'init': 'EPSG:3035'})
    ds_lambert.to_file(wd + outfile_name)
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds_pr = driver.Open(wd + outfile_name, 0)
    ds_pr = ds_pr.GetLayer()
    return ds_pr