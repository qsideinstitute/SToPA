### Imports ###
import pandas as pd
import numpy as np
import folium
import csv
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim

### Functions ###

def add_state_zip(v):
    """This is a helper function to add state and zip code for geolocating."""
    if pd.isna(v):
        return v
    return v + ", Williamstown, 01267"

def geolocate(v,geo,cache_dict):
    """This is a helper function to turn addresses into coordinates."""
    if pd.isna(v):
        return None
    print("Getting geolocation data for " + v + ".")
    if v in cache_dict.keys():
        return cache_dict[v]
    else:
        try:
            result = geo.geocode(v)
            cache_dict[v] = result
            return result
        except:
            cache_dict[v] = None
            return None

def get_coords(df):
    """This function reads in a dataframe and finds coordinates for addresses."""
    df["street"] = df["street"].apply(add_state_zip)
    geolocator = Nominatim(user_agent="sbrooks_williamstown_ma_usa")
    from geopy.extra.rate_limiter import RateLimiter
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    cache_dict = {}
    df["loc"] = df["street"].apply(geolocate, args = (geolocator, cache_dict))
    df["point"]= df["loc"].apply(lambda loc: tuple(loc.point) if loc else None)
    df[["latitude", "longitude", "altitude"]] = pd.DataFrame(df["point"].to_list(), index=df.index)
    # Cache geolocation data
    df.to_csv("df_with_geo_data.csv")

def read_coords():
    """This helper function reads cached coordinates from a csv file."""
    return pd.read_csv("df_with_geo_data.csv")

def make_map(df):
    """This function generates an html map from a dataframe."""
    # center to the mean of all points
    m = folium.Map(location=df[["latitude", "longitude"]].mean().to_list(), zoom_start=12)

    # if the points are too close to each other, cluster them, create a cluster overlay with MarkerCluster
    marker_cluster = MarkerCluster().add_to(m)

    # draw the markers and assign popup and hover texts
    # add the markers the the cluster layers so that they are automatically clustered
    for i,r in df.iterrows():
        if not(pd.isna(r["street"])) and not(pd.isna(r["latitude"])):
            location = (r["latitude"], r["longitude"])
            picture = "info"
            col = "blue"
            
            if ("motor" in r["call_reason"].lower() or "traffic" in r["call_reason"].lower() or "parking" in r["call_reason"].lower() or "vehicle" in r["call_reason"].lower()):
                picture = "car"
                col = "purple"
                
            elif ("building" in r["call_reason"].lower()):
                picture = "building"
                col = "black"

            elif ("animal" in r["call_reason"].lower()):
                picture = "bug"
                col = "pink"

            elif ("fire" in r["call_reason"].lower()):
                picture = "fire"
                col = "red"

            elif ("death" in r["call_reason"].lower()):
                picture = "ambulance"
                col = "darkred"

            elif ("utility" in r["call_reason"].lower()):
                picture = "wrench"
                col = "gray"

            folium.Marker(location=location,
                          popup = str(r["log_num"]) + ", " + str(r["call_reason"]) + ": " + str(r["narrative"]),
                          tooltip = str(r["street"]) + ": " + str(r["call_datetime"]),
                          icon = folium.Icon(color = col,icon = picture, prefix = 'fa'))\
            .add_to(marker_cluster)

    # save to a file
    m.save("map.html")
