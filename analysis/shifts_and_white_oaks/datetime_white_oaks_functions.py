# this module contains the functions for White Oaks exploration
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas
import datetime
from datetime import datetime
import time

def shift_number(item):
    """
    This function takes in a datetime object and converts it to a shift number.
    Shift 1: 9:00-17:00
    Shift 2: 17:00-24:00
    Shift 3: 24:00-9:00

    Return: integer shift number or NaN
    """
    
    ts9 = datetime(2000, 1, 1, 9, 0, 0).time()
    ts17 = datetime(2000, 1, 1, 17, 0, 0).time()
    ts24 = datetime(2000, 1, 1, 23, 59, 59).time()
    try:
        tscall = item.time()
        if ts9 <= tscall <= ts17:
            shiftnumber = 1
        elif ts17 <= tscall <= ts24:
            shiftnumber = 2
        else:
            shiftnumber = 3
        return shiftnumber
    except:
        return np.NaN

def strings_to_datetime(df,column_name):
    """
    This function takes in a pandas dataframe ds and the name of the column to be converted into a datetime object.
    Returns an array of float corresponding to the number of rows in the data frame.
    """
    
    date_and_time = []
    for i in range(df.shape[0]):
        if type(df.iloc[i][column_name]) == str:
            datetime_object = datetime.strptime(df.iloc[i][column_name], '%Y-%m-%d %H:%M:%S')
            date_and_time.append(datetime_object)
        else:
            date_and_time.append(np.NaN)
    return date_and_time

def raw_count_bar_chart(dfall,dfin,dfout,column_name,figsize=(5,8),labelin='White Oaks',labelout='Not White Oaks'):
    """
    Takes in three databases: dfall, dfin (e.g. in White Oaks), and dfout (e.g. not in White Oaks), and a column name.
    Compares the counts in dfin to the ones in df_out by raw count.
    Returns a horizontal bar chart.
    """

    #compute dictionaries
    all=dfall[column_name].value_counts().to_dict()
    WO=dfin[column_name].value_counts().to_dict()
    notWO=dfout[column_name].value_counts().to_dict()
    WO=add_missing_keys(all,WO)
    notWO=add_missing_keys(all,notWO)

    ind = np.arange(len(notWO))
    width = 0.4
    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(ind + width, list(notWO.values()), width, label=labelout)
    ax.barh(ind, list(WO.values()), width, label=labelin)
    ax.set(yticks=ind + width, yticklabels=WO.keys())
    ax.legend()
    plt.title('Raw count comparison by '+str(column_name))
    plt.show()
    return fig


def add_missing_keys(dict1,dict2):
    #adds missing keys to the smaller dictionary dict2 from dict1 with value 0 for easier comparison. Returns dict2.
    missing_keys = set(dict1.keys()) - set(dict2.keys())
    for k in missing_keys:
        dict2[k] = 0
    return dict2

def percentage_bar_chart(dfall,dfin,dfout,column_name,figsize=(5,8),labelin='White Oaks',labelout='Not White Oaks'):
    """
    Takes in three databases: dfall, dfin (e.g. in White Oaks), and dfout (e.g. not in White Oaks), and a column name.
    Compares the counts in dfin to the ones in df_out by proportion.
    Returns a horizontal bar chart.
    """

    #compute dictionaries
    all=dfall[column_name].value_counts().to_dict()
    WO=dfin[column_name].value_counts().to_dict()
    notWO=dfout[column_name].value_counts().to_dict()
    WO=add_missing_keys(all,WO)
    notWO=add_missing_keys(all,notWO)
    percentagesWO=list(WO.values())/np.sum(list(WO.values()))
    percentagesnotWO=list(notWO.values())/np.sum(list(notWO.values()))

    ind = np.arange(len(notWO))
    width = 0.4
    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(ind + width, percentagesnotWO, width, label=labelout)
    ax.barh(ind, percentagesWO, width, label=labelin)
    ax.set(yticks=ind + width, yticklabels=WO.keys())
    ax.legend()
    plt.title('Proportion comparison by '+str(column_name))
    plt.show()
    return fig

def generate_officer_shift_distributions(df,column_name):
    """
    Takes in a dataframe and a column name, returns a dictionary with officer names as keys and shift count vectors as values.
    The shift count vectors are of the format [number of first shifts, number of second shifts, number of third shifts]
    """
    #generate a dictionary
    officers=df[column_name].value_counts().to_dict()

    #generate a vector of shift counts for each officer 
    for key in officers:
        mask = df[column_name] == str(key)
        df_subset = df[mask]
        for i in range(df_subset.shape[0]):
            shift1=[df_subset[df_subset['Shift_Number'] == 1].shape[0]]
            shift2=[df_subset[df_subset['Shift_Number'] == 2].shape[0]]
            shift3=[df_subset[df_subset['Shift_Number'] == 3].shape[0]]
            officers.update([(key, [shift1,shift2,shift3])])

    return officers

def comparevalues(df, col1, col2, newcol):
    """
    This function takes in a dataframe and three column names: two existing columns to compare and a new column to append.
    The new column contains the difference: col1-col2=newcol, in the datetime format.
    Returns the updated dataframe
    """
    a = np.empty(df.shape[0], dtype = pandas._libs.tslibs.timestamps.Timestamp)
    for i in range(df.shape[0]):
        try:
            number = pandas.to_datetime(df.iloc[i][col1], errors = 'ignore')-pandas.to_datetime(df.iloc[i][col2], errors = 'ignore')
            a[i] = number
        
        except: 
            a[i] = np.NaN
    df[newcol] = a
    return df


def seconds(df, col, newcol):
    """
    Takes in a dataframe, an existing column name and new column name. Converts the dataframe format in the old column
    to a float format in the new column, in seconds. 
    Returns dataframe.
    """
    import numpy as np
    a = np.empty(df.shape[0])
    for i in range(df.shape[0]):
        try:
            number = df.iloc[i][col]
            a[i] = number.total_seconds()
        except:
            a[i] = np.NaN
        df[newcol] = a
    return df
        