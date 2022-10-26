### Imports ###
import pandas as pd
from geopy.geocoders import Nominatim

### Functions ###

class Geolocator():
    """A class for augmenting an existing csv file with latitude and longitude data (based on addresses).

    Parameters
    ----------
    state_zip : string
        A string to be appended to each address in the original dataframe before geolocating (usually consists of city/state/zip or similar).
    user_agent_name : string
        The user agent name used with Nominatim.
    """

    
    slots = ("_cache_dict", "_state_zip", "_user_agent_name")

    
    def __init__(self, state_zip, user_agent_name):
        self._cache_dict = {}
        self._state_zip = state_zip
        self._user_agent_name = user_agent_name

        
    @staticmethod
    def add_state_zip(v, string_to_append):
        if pd.isna(v):
            return v
        else:
            return v + string_to_append

        
    @staticmethod
    def read_coords(inf):
        """This helper function reads cached coordinates from a csv file."""
        return pd.read_csv(inf)


    def geolocate(self, v, geo):
        """Turns addresses into coordinates."""
        if pd.isna(v):
            # TODO: print warning
            return None
        print("Getting geolocation data for " + v + ".")
        if v in self._cache_dict.keys():
            return self._cache_dict[v]
        else:
            try:
                result = geo.geocode(v)
                self._cache_dict[v] = result
                return result
            except:
                self._cache_dict[v] = None
                return None

            
    def get_coords(self, df, address_colname, outf, lat_colname = "latitude", long_colname = "longitude", alt_colname = "altitude"):
        """Finds coordinates for addresses in a dataframe and writes an augmented dataframe to csv."""
        if self._state_zip is not None:
            # if addresses don't have state/zip data, add state/zip data
            df[address_colname] = df[address_colname].apply(self.add_state_zip, args=(self._state_zip,))
        
        geolocator = Nominatim(user_agent=self._user_agent_name)
        from geopy.extra.rate_limiter import RateLimiter
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

        # Add loc, point, latitude, longitude, and altitude columns to df and write to csv
        df["loc"] = df[address_colname].apply(self.geolocate, args = (geolocator,))
        df["point"]= df["loc"].apply(lambda loc: tuple(loc.point) if loc else None)
        df[[lat_colname, long_colname, alt_colname]] = pd.DataFrame(df["point"].to_list(), index=df.index)
        df.to_csv(outf)
