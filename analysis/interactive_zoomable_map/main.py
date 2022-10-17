import config
import maptools
import pandas as pd
import os

# Read original data from csv.
df = pd.read_csv("data.csv")
# Geolocate addresses from address column if needed.
g = maptools.Geolocator(state_zip = config.state_zip, user_agent_name = config.user_agent_name)
if not config.appended_df_filename in os.listdir():
    g.get_coords(df, address_colname = config.address_colname, outf = config.appended_df_filename)

# Read geolocation data and generate interactive filterable map.
df = g.read_coords()
mw = maptools.MapWriter(df_origin = config.df_origin,
                        target_path = config.target_path,
                        selector_data = config.selector_data,
                        coords = config.coords,
                        init_zoom = config.init_zoom,
                        latitude_colname = config.latitude_colname,
                        longitude_colname = config.longitude_colname,
                        primary_data_path = config.primary_data_path)
mw.write_template_to_html()
