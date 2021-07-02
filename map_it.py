import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Wicked Free Wifi CSV: 
# https://data.boston.gov/dataset/wicked-free-wifi-locations/resource/50be2132-e83f-4197-b5d1-e83ef153a217
# Boston Transportation Districts Shapefile:
# https://data.boston.gov/dataset/boston-transportation-department-btd-districts1/resource/fe16d9d0-92ff-4f71-b021-9cceffba47ed

# Load data from CSV into a pandas dataframe
data_file = "./data/Wicked_Free_WiFi_Locations.csv"
columns_of_interest = ['device_lat', 'device_long'] #, 'neighborhood_name']
wifi_df = pd.read_csv(data_file, usecols=columns_of_interest)

# specify lat/long geometry
geometry = gpd.points_from_xy(wifi_df.device_lat, 
                              wifi_df.device_long)


wifi_df['coords'] = wifi_df[['device_long', 'device_lat']].values.tolist()
wifi_df['coords'] = wifi_df['coords'].apply(Point) 
# Note: Look at using a more efficient way than apply. (Probably fine w/such a small dataset though.)

# Load the Boston shapefile into a geopandas dataframe
boston_map = gpd.read_file('./data/Boston_Transportation_Department_(BTD)_Districts_.shp')
# print(boston_map.columns) -> Index(['OBJECTID_1', 'OBJECTID', 'PWD', 'NAME', 'COMBO', 'DIST',
#                                     'ShapeSTAre', 'ShapeSTLen', 'geometry'], dtype='object')
# print(boston_map.crs) -> epsg:2249
#print(boston_map.head(2)) ->    
#    OBJECTID_1  OBJECTID  ...     ShapeSTLen                                           geometry
# 0           1         0  ...  149217.158855  MULTIPOLYGON (((794239.584 2969271.287, 794678...
# 1           2         0  ...  115152.750832  POLYGON ((761410.429 2945147.110, 762081.631 2...

# destination crs
reprojected_boston_map = boston_map.to_crs({'init': 'epsg:4326'})
#print(t_map.head(2)) ->
#    OBJECTID_1  OBJECTID  ...     ShapeSTLen                                           geometry
# 0           1         0  ...  149217.158855  MULTIPOLYGON (((-70.98885 42.39470, -70.98725 ...
# 1           2         0  ...  115152.750832  POLYGON ((-71.11079 42.32898, -71.10832 42.327...


# Create geopandas dataframe for wifi data
geo_wifi_df = gpd.GeoDataFrame(wifi_df, 
                               crs=reprojected_boston_map.crs, 
                               geometry='coords')

# both CRS are epsg:2249 (MA mainland)

# Plot it
fig, ax = plt.subplots(figsize=(8, 5))

reprojected_boston_map.plot(ax=ax, alpha=0.4, color="blue")
geo_wifi_df.plot(ax=ax, alpha=0.9, color="red", markersize=4)

plt.title("Boston's Wicked Free Wifi Locations")

plt.xlim(-71.200, -70.983) # x = longitude
plt.ylim(42.220, 42.400) # y = latitude

plt.show()


"""
Credits to 
0. Changing coordinate reference system: 
https://gis.stackexchange.com/questions/276940/re-projecting-lat-and-long-in-python-geopandas-but-geometry-unchanged

1. https://towardsdatascience.com/how-to-read-csv-file-using-pandas-ab1f5e7e7b58
2. https://stackoverflow.com/questions/53233228/plot-latitude-longitude-from-csv-in-python-3-6
3. https://towardsdatascience.com/geopandas-101-plot-any-data-with-a-latitude-and-longitude-on-a-map-98e01944b972
4. https://medium.com/@ianforrest11/graphing-latitudes-and-longitudes-on-a-map-bf64d5fca391
"""

