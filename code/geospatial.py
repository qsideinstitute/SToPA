import williamstown_map as wmap

import numpy as np

# While still experimenting...


###

switch = 0


###

if switch==0:
    # 0. Determine if we are within a polygon 
    # (I think geopandas has a built-in for this)
    
    # see
    # https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoSeries.contains.html
    import shapely
    np.random.seed(1)
    
    x0,x1 = wmap.ax.get_xlim()
    y0,y1 = wmap.ax.get_ylim()
    _xs = np.random.uniform(x0,x1, 100)
    _ys = np.random.uniform(y0,y1, 100)
    #points = [shapely.geometry.Point(_x,_y)
    _points = wmap.geopandas.GeoSeries(
        [shapely.geometry.Point(_x,_y) for _x,_y in zip(_xs,_ys)],
        crs='EPSG:4326'
    )
    
    # pick arbitrary region.
    gdf = wmap.gdfs['natural.json']
    #row = gdf[gdf['name'] == 'Linear Park']
    row = gdf.iloc[[gdf.area.argmax()]]
    flags = row.contains( _points, align=False)
    #row['in_region'] = flags
    
    # visualize!
    row.plot(ax=wmap.ax, color='#080', lw=0, zorder=-100)
    _points.plot(c=flags, ax=wmap.ax)
    
    
elif switch==1:
    # 1. Get all points within __ distance of (lon,lat)
    # (requires some learning of map projections)
    pass
elif switch==2:
    # 2. Get the distance function to a polygon, towards
    # answering "region within X miles of polygon"
    # (ex: within 0.5 miles of Williams College)
    pass
#
