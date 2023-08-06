from math import radians, cos, sin, asin, sqrt
import rasterio
from matplotlib import pyplot
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask
from shapely.geometry import Point
import geopandas as gpd
import numpy as np
import pandas as pd

def plot(file):
    src = rasterio.open(file)
    show(src)

def plot_contour(file):
    src = rasterio.open(file)
    fig, ax = pyplot.subplots(1, figsize=(12, 12))
    show((src, 1), cmap='Greys_r', interpolation='none', ax=ax)
    show((src, 1), contour=True, ax=ax)
    pyplot.show()

def plot_hist(file, bin=50, title="Histogram"):
    src = rasterio.open(file)
    show_hist(
    src, bins=bin, lw=0.0, stacked=False, alpha=0.3,
    histtype='stepfilled', title=title)

    
def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:

    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers
    return c * r

def extract(rf, shp):
    
    # open shapefile as GeoDataFrame
    gdf = gpd.read_file(shp)
    # open raster file
    # with rasterio.open(rf) as src:
    src = rasterio.open(rf)
    pixel_coords = []
    k = 0
    for geom in gdf.geometry:
        if k == 0:
            # clip the raster to the shapefile polygons
            mask = rasterio.features.geometry_mask([geom], src.shape, transform=src.transform, invert=True, all_touched =True)
            
            # create dictionary to store data for each band
            data = {}
            for i in range(src.count):
                # band = clipped[i]
                band = src.read(i+1, masked=True)[mask]
                column_name = f'band_{i+1}'
                data[column_name] = band.flatten()

            row, col = np.where(mask == True)
            # row, col = np.where(clipped[0] != -10000) 
            coords = [Point(src.xy(r, c)) for r, c in zip(row, col)]
            
            # create a GeoDataFrame from the extracted data
            gdf_extracted = gpd.GeoDataFrame(data, geometry=coords,crs= 32760)              
            
        elif k>0:
                        
            mask = rasterio.features.geometry_mask([geom], src.shape, transform=src.transform, invert=True, all_touched =True)
            
            # create dictionary to store data for each band
            data = {}
            for i in range(src.count):
                # band = clipped[i]
                band = src.read(i+1, masked=True)[mask]
                column_name = f'band_{i+1}'
                data[column_name] = band.flatten()

            row, col = np.where(mask == True)
            
            coords = [Point(src.xy(r, c)) for r, c in zip(row, col)]
                                
            gdf_k = gpd.GeoDataFrame(data, geometry=coords,crs= 32760)   
            
            gdf_extracted = pd.concat([gdf_extracted, gdf_k])
            
        k += 1
        
    return gdf_extracted
