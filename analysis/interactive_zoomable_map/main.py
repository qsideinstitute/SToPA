import maptools
import pandas as pd
import os

df = pd.read_csv("data.csv")
g = maptools.Geolocator()
if not "addresses.csv" in os.listdir():
    g.get_coords(df, address_colname = "street")

df = g.read_coords()
mw = maptools.MapWriter()
mw.write_template_to_html()
