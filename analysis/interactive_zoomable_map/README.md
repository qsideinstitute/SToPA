# Interactive Maps

Create interactive, filterable maps using Leaflet.js. By default, run `python main.py` from this folder and check out the output in `output_map.html` using a browser.

If address data cannot be found in `addresses.py`, running `main.py` also generates a new csv file (`addresses.csv` by default) that contains an augmented version of the original data, including the old csv columns as well as a few columns with csv data.

## Using `config.py` options

0. If you wish to fetch latitude/longitude data based on addresses, in `config.py`, edit your Nominatim `user_agent_name` (no need to set this up elsewhere - read the Nominatim terms of use for more information). Address data for the SToPA Williamstown dataset exists by default in the project folder in `addresses.csv`. Fetching coordinates may take a few minutes.
1. If you wish to create a map with your own data from scratch, you will need to edit some options in `config.py`. You will notably need to edit the `df_origin`, `address_colname`, `state_zip`, `selector_data`, `coords`, and perhaps `primary_data_path` fields. The form and function of each of these fields is documented in `config.py`.
2. Then, run `python main.py` from this folder to generate a new `addresses.csv` file and map output.

## `maptools` module

If you wish to work with geolocation and map creation in a more modular way, you can `import maptools` from a Python shell or use a Jupyter notebook (the notebook `maptools_notebook.ipynb` is included in the project folder and contains a "getting started" example similar to the code in `main.py`). In either case, you can directly create instances of `Geolocator` and `MapWriter` and invoke functions.