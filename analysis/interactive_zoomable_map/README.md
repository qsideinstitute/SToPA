To create an interactive map:

0. Open `interactive_map.py` and edit your Nominatim user_agent name (no need to set this up elsewhere).
1. Load in a pandas dataframe `df` with a 'street' column containing addresses.
2. Navigate to this directory `/interactive_zoomable_map`, import maptools, and run `maptools.get_coords(df)`. This may take a while depending on the number of unique addresses in your dataset.
3. Step 2 generates an extended csv file called df_with_geo_data.csv. You can turn this directly into a map from a python shell with:

```
import maptools
maptools.make_map(maptools.read_coords())
```