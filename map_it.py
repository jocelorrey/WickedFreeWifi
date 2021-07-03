import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from shapely.geometry import Point

"""
DATA SOURCES:
Wicked Free Wifi Locations - CSV:
https://data.boston.gov/dataset/wicked-free-wifi-locations/resource/50be2132-e83f-4197-b5d1-e83ef153a217

Boston Transportation Districts - Shapefile:
https://data.boston.gov/dataset/boston-transportation-department-btd-districts1/resource/fe16d9d0-92ff-4f71-b021-9cceffba47ed
"""

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

# Reproject map to align with lat/long of wifi locations
reprojected_boston_map = boston_map.to_crs({'init': 'epsg:4326'})

# Create geopandas dataframe for wifi data
geo_wifi_df = gpd.GeoDataFrame(wifi_df, 
                               crs=reprojected_boston_map.crs, 
                               geometry='coords')

# Plot them together
fig, ax = plt.subplots()

reprojected_boston_map.plot(ax=ax, alpha=0.2, color="blue")
geo_wifi_df.plot(ax=ax, alpha=0.2, color="red", marker='o', markersize=25)

plt.title("Boston's Wicked Free Wifi Locations", fontweight="bold")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.xlim(-71.200, -70.983)
plt.ylim(42.220, 42.400)
plt.xticks(rotation=65) # rotate x-axis labels
plt.gca().xaxis.set_major_formatter(FormatStrFormatter(u'%.2f\u00B0')) # show deg symbol
plt.gca().yaxis.set_major_formatter(FormatStrFormatter(u'%.2f\u00B0'))
plt.tight_layout()
plt.show()

"""
Useful resources:
1. https://towardsdatascience.com/how-to-read-csv-file-using-pandas-ab1f5e7e7b58
2. https://stackoverflow.com/questions/53233228/plot-latitude-longitude-from-csv-in-python-3-6
3. https://towardsdatascience.com/geopandas-101-plot-any-data-with-a-latitude-and-longitude-on-a-map-98e01944b972
4. https://medium.com/@ianforrest11/graphing-latitudes-and-longitudes-on-a-map-bf64d5fca391
5. https://gis.stackexchange.com/questions/276940/re-projecting-lat-and-long-in-python-geopandas-but-geometry-unchanged
6. https://stackoverflow.com/questions/3927389/add-unit-to-yaxis-labels-in-matplotlib
7. https://matplotlib.org/stable/api/markers_api.html
"""

