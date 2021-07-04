import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from shapely.geometry import Point

# Define data files
csv_file = './data/Wicked_Free_WiFi_Locations.csv'
shp_file = './data/Boston_Transportation_Department_(BTD)_Districts_.shp'

# Load data from CSV into a pandas dataframe
columns_of_interest = ['device_lat', 'device_long'] #, 'neighborhood_name']
wifi_df = pd.read_csv(csv_file, usecols=columns_of_interest)

# Specify lat/long geometry
geometry = gpd.points_from_xy(wifi_df.device_lat, wifi_df.device_long)
wifi_df['coords'] = wifi_df[['device_long', 'device_lat']].values.tolist()
wifi_df['coords'] = wifi_df['coords'].apply(Point) 

# Load shapefile into a geopandas dataframe
boston_map = gpd.read_file(shp_file)

# Reproject map to align with lat/long of wifi locations
boston_map = boston_map.to_crs({'init': 'epsg:4326'})

# Create geopandas dataframe for wifi data
geo_wifi_df = gpd.GeoDataFrame(wifi_df, crs=boston_map.crs, geometry='coords')

# Plot them together
fig, ax = plt.subplots()

boston_map.plot(ax=ax, alpha=0.15, color="blue")
geo_wifi_df.plot(ax=ax, alpha=0.55, cmap='prism', marker='o', markersize=25)

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
8. https://matplotlib.org/stable/tutorials/colors/colormaps.html
"""

