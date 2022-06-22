
'''
Purpose: Create template maps using the geojson 
data located in ../data/maps/

This module is intended to only create a background; 
not follow up with any specific police data.
'''
import geopandas
from matplotlib import pyplot
import settings
import os


pyplot.style.use('bmh')

fig,ax = pyplot.subplots(1,1, figsize=(8,8), constrained_layout=True)

layers = ['railways.json', 'waterways.json', 'buildings.json']
lcols = ['#333', '#229', '#000']
lws = [0.5, 1, 5]
zorders=[-100, -100, 100]

# TODO: do we want to bother with this dictionary 
# at all, if the road types will still all get their 
# own special variables?
gdfs = {}
for i,(layer,col,lw,zorder) in enumerate(zip(layers,lcols,lws,zorders)):
    gdfs[layer] = geopandas.read_file( os.path.join(settings.MAPS_FOLDER, layer) )
    gdfs[layer].plot(ax=ax, color=col, lw=lw, zorder=zorder)

# Handle the roads carefully to try to highlight important roads the most.
gdf_road = geopandas.read_file(os.path.join(settings.MAPS_FOLDER, 'roads.json'))

gdf_road_primary = gdf_road[ gdf_road['type'] == 'primary' ]
gdf_road_secondary = gdf_road[ gdf_road['type'] == 'secondary' ]
gdf_road_other = gdf_road[ ~ gdf_road['type'].isin(['primary', 'secondary']) ]

gdf_road_primary.plot(ax=ax, color='#222', lw=1, zorder=-100)
gdf_road_secondary.plot(ax=ax, color='#333', lw=0.6, zorder=-100)
gdf_road_other.plot(ax=ax, color='#444', lw=0.2, zorder=-100)

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Williamstown', loc='left')

# TODO: 1-mile (or 1-kilometer) scalebar.
# See:
# https://geopandas.org/en/stable/gallery/matplotlib_scalebar.html

if __name__=='__main__':
    fig.savefig('williamstown.pdf')
