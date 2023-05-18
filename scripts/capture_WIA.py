

import pandas
import numpy as np
import re

# todo: OS-agnostic paths
df1 = pandas.read_csv('../data/Archive/parsed_logs_2019.csv')
df2 = pandas.read_csv('../data/Archive/parsed_logs_2020.csv')

df = pandas.concat([df1,df2])

# pull raw OCR location/address.
locations = df['call_address']

# pull up complete encoding dataset.
codes = pandas.read_csv('williamstown_address_codes.csv')
prefixes = codes['Jur'].unique()

code_prefix = '(' + '|'.join( list(prefixes) ) + ')'
# 

pattern = '.*' + code_prefix + '_([0-9A-Z]{1,4}).*'

hascodes = locations.str.match(pattern) # true/false/nan (why pandas, why??)
hascodes.replace(np.nan, False, inplace=True)

fraction = sum(hascodes)/len(hascodes)
print('Total logs: ', df.shape[0])
print('Fraction of logs matching regex: ', fraction)

matches = locations.str.findall(pattern)
wia_codes = np.array(['_'.join(e[0]) if type(e)==list and len(e)>0 else '' for e in matches])

