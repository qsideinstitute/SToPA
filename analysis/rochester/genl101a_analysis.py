import pandas
import seaborn
from matplotlib import pyplot as plt
from matplotlib import dates, ticker
#import numpy as np
import datetime

plt.style.use('bmh')


#

df = pandas.read_csv('rochester_genl101a_parsed.csv')
df['datetime_str'] = df['datetime']
df['datetime'] = [datetime.datetime.strptime(s, '%m/%d/%Y %I:%M %p') for s in df['datetime_str']]

df['tod'] = df['datetime'].dt.time
df['Hour of day'] = df['datetime'].dt.hour + 1/60*df['datetime'].dt.minute

##

fig,ax = plt.subplot_mosaic('''
AB
CD
''', figsize=(12,8), constrained_layout=True)

###
# Illustrate Genl101A records over time; by law code

# TODO: match tick positions and bin widths/positions to respect datetimes.
seaborn.histplot(ax=ax['B'], data=df, x='datetime', hue='law', multiple='stack')
ax['B'].tick_params(axis='x', labelrotation=45)
ax['B'].set_title('Genl101A records over time', loc='left')

####
# Illustrate Genl101A records by time of day; by law code.
seaborn.histplot(ax=ax['C'], data=df, x='Hour of day', hue='law', multiple='stack', bins=list(range(0,25,3)), binrange=[0,24])

#ax['C'].xaxis.set_major_locator(dates.HourLocator(interval=3))
#ax['C'].xaxis.set_major_formatter(dates.DateFormatter('%h:%m'))
ax['C'].xaxis.set_major_locator(ticker.MultipleLocator(3))

ax['C'].tick_params(axis='x', labelrotation=45)
ax['C'].set_title('Cited infraction by time of day', loc='left')

# ax['D'] ... what to do?

#ax['A'].set_visible(False)
# TODO: https://newyork.public.law/laws/n.y._vehicle_and_traffic_law_title_7
# match to 1163B, 1156A, 1236A, 1236B (short description of codes)
ax['A'].set(xticks=[], yticks=[])
ax['A'].set_title('Rochester codes', loc='left')
#ax['A'].text(0.05, 0.95, '1163B: "A signal of intention to turn right or left\nwhen required shall be given..." \n\n1156A: "Where sidewalks are provided...\nunlawful for any pedestrian to walk along...\n an adjacent roadway."\n\n1236A: "Every bicycle... after sunset...\nshall be equipped with a lamp..."\n\n1236B: "No person shall operate a bicycle\nunless it is equipped with a bell..."', transform=ax['A'].transAxes, va='top', ha='left')
descriptions = ['1163B: "A signal of intention to turn right or left\nwhen required shall be given..."',
'1156A: "Where sidewalks are provided...\nunlawful for any pedestrian to walk along...\n an adjacent roadway."',
'1236A: "Every bicycle... after sunset...\nshall be equipped with a lamp..."',
'1236B: "No person shall operate a bicycle\nunless it is equipped with a bell..."']

colors = [plt.cm.tab10(0), plt.cm.tab10(3), plt.cm.tab10(4), plt.cm.tab10(2)]

for col,descr in zip(colors, descriptions):
    ax['A'].scatter([],[], color=col, label=descr, marker='s', s=100)
ax['A'].legend(loc='upper left')
ax['A'].set(facecolor=[0,0,0,0])
for _s in ax['A'].spines.values():
    _s.set_visible(False)

# TODO
ax['D'].set_visible(False)

###########

fig.savefig('rochester_prelim_genl101a.pdf')
fig.savefig('rochester_prelim_genl101a.png')
fig.show()

