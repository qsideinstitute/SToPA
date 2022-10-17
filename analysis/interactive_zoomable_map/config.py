"""Config file containing default parameters. To use these default parameters in your own code, import config. See main.py for examples.
"""


### DataFrame Defaults ###

# The name of the file where the original data was stored.
df_origin = "data.csv"

# The name of the file where the appended dataframe (address and coordinates/latitute/longitude) will be stored (address data is cached to prevent repeated Nominatim requests).
appended_df_filename = "addresses.csv"

# The name of the column in df_origin containing address (number and street) data.
address_colname = "street"


### Geolocator Defaults ###

# The Nominatim user agent name.
user_agent_name = "qside_stopa_lab"

# Additional address data to be appended to each address entry before attempting to geolocate.
state_zip = ", Williamstown, MA 01267"


### MapWriter Defaults ###

# The output file path for the interactive map.
target_path = "./output_map.html"

# A dictionary of data for use in generating JavaScript selector boxes. Each dictionary entry consists of the df column name (from df_origin) to use to generate the options for the selector, and the default option name.
selector_data = {
    "call_reason": "All reasons",
    "call_taker": "All call takers",
    "street": "All streets"
}

# The coordinates to center the map when it is first opened.
coords = [42.7, -73.2]

# The initial zoom level of the map.
init_zoom = 12

# The path to primary data, if you wish to link to primary data from popups on the map.
# This must be relative to the location from which the map is to be OPENED and viewed.
# For now, this path must be fixed in advance of the map being generated (since this path is hard-coded into the HTML for the map popups).
primary_data_path = "../../data/primary_datasets"
