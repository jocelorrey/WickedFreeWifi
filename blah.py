import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Wicked Free Wifi CSV: 
# https://data.boston.gov/dataset/wicked-free-wifi-locations/resource/50be2132-e83f-4197-b5d1-e83ef153a217
# Boston Transportation Districts Shapefile:
# https://data.boston.gov/dataset/boston-transportation-department-btd-districts1/resource/fe16d9d0-92ff-4f71-b021-9cceffba47ed

# Load data from CSV into a oandas dataframe
data_file = "./data/Wicked_Free_WiFi_Locations.csv"
columns_of_interest = ['device_lat', 'device_long', 'neighborhood_name']
wifi_location_df = pd.read_csv(data_file, usecols=columns_of_interest)

# Load the shapefile into a geopandas dataframe
boston_map = gpd.read_file('./data/Boston_Transportation_Department_(BTD)_Districts_.shp')

# Unclear why this is needed:
#geometry = [Point(xy) for xy in zip(wifi_location_df['device_long'], wifi_location_df['device_lat'])]
# create GeoPandas dataframe
my_crs = boston_map.crs
print(my_crs)
geometry = gpd.points_from_xy(wifi_location_df.device_lat, wifi_location_df.device_long)
geo_df = gpd.GeoDataFrame(wifi_location_df, crs=my_crs, geometry=geometry)

#print(geo_df)

# Plot it
fig, ax = plt.subplots(figsize=(8, 5))

boston_map.plot(ax=ax, alpha=0.2, color="blue")
geo_df.plot(ax=ax, alpha=0.9, color="red")

plt.title("Boston's Wicked Free Wifi Locations")

#plt.xlim(70.985278, 71.191306) # x = longitude
#plt.ylim(42.225861, 42.398000) # y = latitude

#plt.show()
# Credits to 
# 1. https://towardsdatascience.com/how-to-read-csv-file-using-pandas-ab1f5e7e7b58
# 2. https://stackoverflow.com/questions/53233228/plot-latitude-longitude-from-csv-in-python-3-6
# 3. https://towardsdatascience.com/geopandas-101-plot-any-data-with-a-latitude-and-longitude-on-a-map-98e01944b972
# 4. https://medium.com/@ianforrest11/graphing-latitudes-and-longitudes-on-a-map-bf64d5fca391


