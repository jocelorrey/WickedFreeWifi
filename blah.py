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
wifi_location_df = pd.read_csv(data_file, usecols=columns_of_interest)

# specify lat/long geometry
geometry = gpd.points_from_xy(wifi_location_df.device_lat, 
                              wifi_location_df.device_long)


wifi_location_df['coords'] = wifi_location_df[['device_long', 'device_lat']].values.tolist()
wifi_location_df['coords'] = wifi_location_df['coords'].apply(Point)
wifi_location_df

# Load the Boston shapefile into a geopandas dataframe
boston_map = gpd.read_file('./data/Boston_Transportation_Department_(BTD)_Districts_.shp')

# Create geopandas dataframe for wifi data
geo_df = gpd.GeoDataFrame(wifi_location_df, 
                          crs=boston_map.crs, 
                          geometry='coords')

# Ensure the coordinate reference systems are the same
print("Wifi Locations:", geo_df.crs)
print("Boston Map:", boston_map.crs) # both epsg:2249 (MA mainland)

#print(geo_df)

# Plot it
fig, ax = plt.subplots(figsize=(8, 5))

boston_map.plot(ax=ax, alpha=0.4, color="blue")
geo_df.plot(ax=ax, alpha=0.9, color="red")
print(geo_df)
plt.title("Boston's Wicked Free Wifi Locations")

plt.xlim(-71.191306, -70.985278) # x = longitude
plt.ylim(42.225861, 42.398000) # y = latitude

plt.show()
# Credits to 
# 1. https://towardsdatascience.com/how-to-read-csv-file-using-pandas-ab1f5e7e7b58
# 2. https://stackoverflow.com/questions/53233228/plot-latitude-longitude-from-csv-in-python-3-6
# 3. https://towardsdatascience.com/geopandas-101-plot-any-data-with-a-latitude-and-longitude-on-a-map-98e01944b972
# 4. https://medium.com/@ianforrest11/graphing-latitudes-and-longitudes-on-a-map-bf64d5fca391


