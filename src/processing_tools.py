""" Data Processing Tools for WPD Data 
"""
import git
import numpy as np
import os
import pandas as pd
import re

from datetime import datetime, timedelta
from fuzzywuzzy import fuzz

import src.settings as settings

def read_known_data_lists():
    """ Load lists of known data for reasons, officers, actions and streets.
    """
    with open(f"{settings.PROJECT_FOLDER}/data/williamstown_known_reasons.txt") as file:
        lines = file.readlines()
        reasons = [line.rstrip() for line in lines][1:]

    with open(f"{settings.PROJECT_FOLDER}/data/williamstown_known_officers.txt") as file:
        lines = file.readlines()
        officers = [line.rstrip() for line in lines]

    with open(f"{settings.PROJECT_FOLDER}/data/williamstown_known_actions.txt") as file:
        lines = file.readlines()
        actions = [line.rstrip() for line in lines]
    
    with open(f"{settings.PROJECT_FOLDER}/data/williamstown_known_streets.txt") as file:
        lines = file.readlines()
        streets = [line.rstrip() for line in lines]
        
    return reasons, officers, actions, streets

def get_dates(df_parquet, year, plot = False):
    """ Returns dataframes with dates in dat change indices. 
    """
    allowed = set([str(d) for d in range(0,10)] + ["/"] + ["-"])
    df_date = df_parquet.copy()
    df_date.reset_index(drop = True, inplace = True)
    last_known_date = pd.to_datetime(f"{year}-01-01")
    dates = []
    change_idx = []
    
    for i in range(df_date.shape[0] - 2):
        if ("For" in df_date.loc[i,"text"]) & ("Date" in df_date.loc[i+1,"text"]):
            
            # Get bounding box around "For Date:"
            date_top = df_date.loc[i,"top"]
            date_pg = df_date.loc[i,"pdf_page"]
            
            df_i = df_date[df_date["pdf_page"] == date_pg]
            df_i = df_i[(df_i["top"] <= date_top + 50) &(df_i["top"] >= date_top - 50)]
            df_i = df_i[df_i["left"] < 1000]
            text = " ".join(df_i["text"].values)
            date = re.findall("\d{2}[^\w\d\r\n:]\d{2}[^\w\d\r\n:]\d{4}",text)
            dt = "date_unknown"
            if len(date) > 0:
                try:
                    dt = pd.to_datetime(date[0],infer_datetime_format = True)
                    dt = dt.replace(year = year)
                    if np.abs((dt - last_known_date).days) > 25:
                        dt = "date_unknown"
                except:
                    dt = "date_unknown"
            if dt == "date_unknown":
                dt = last_known_date + timedelta(days = 1)
            df_date.loc[i,"date"] = dt
            last_known_date = dt
            
            dates.append(dt)
            change_idx.append(i)
    
    df_date_change = pd.DataFrame()
    df_date_change["date"] = dates
    df_date_change["change_idx"] = change_idx
    
    df_date["date"] = df_date["date"].fillna(method = "ffill")
    df_date["date"] = df_date["date"].fillna(method = "bfill")
    
    if plot == True:
        fig, ax = plt.subplots(figsize = (10,15))
        for idx in df_date.index:
            text = df_date.loc[idx,"text"]
            x = df_date.loc[idx,"left"]
            y = df_date.loc[idx,"top"]
            ax.annotate(text = text, xy = (x,y))

        w = df_date["width"].max()
        h = df_date["height"].max()
        
        ax.set_xlim(df_date["left"].min(), df_date["left"].max() + w)
        ax.set_ylim(df_date["top"].max() + 25, df_date["top"].min() - h)


        # Create a Rectangle patch
        left = df_i["left"].min()
        top = df_i["top"].min() - df_i["height"].max()
        w = (df_i["left"] + df_i["width"]).max() - df_i["left"].min()
        h = 100
        rect = patches.Rectangle((left, top), w, h, 
            linewidth=2, edgecolor='b', facecolor='none')
        # Add the patch to the Axes
        ax.add_patch(rect)
        plt.show()
        
    return df_date, df_date_change

def get_log_numbers(df_parquet, plot = False):
    """ Returns dataframes with log numbers and log change indices.
    """
    df_log = df_parquet.copy()
    df_log.reset_index(drop = True, inplace = True)
    
    log_text = " ".join(df_log[df_log["left"] < 50]["text"])
    log_nums = re.findall("\d+[-+:]\d+",log_text)
    
    df_log = df_log[df_log["text"].isin(log_nums)]
    df_log["text"] = [l.replace("+","-") for l in df_log["text"]]
    
    if plot == True:
        fig, ax = plt.subplots(figsize = (10,15))
        for idx in df.index:
            text = df.loc[idx,"text"]
            x = df.loc[idx,"left"]
            y = df.loc[idx,"top"]
            ax.annotate(text = text, xy = (x,y))

        w = df["width"].max()
        h = df["height"].max()
        ax.set_xlim(df["left"].min(), df["left"].max() + w)
        ax.set_ylim(df["top"].max() + 25, df["top"].min() - h)
    
        for i in df_log.index:
            left = df_log.loc[i,"left"]
            top = df_log.loc[i,"top"] - df_log.loc[i,"height"]
            w = df_log.loc[i,"width"]
            h = df_log.loc[i,"height"]
            
            rect = patches.Rectangle((left, top), w, h, 
                linewidth=2, edgecolor='g', facecolor='none')
            # Add the patch to the Axes
            ax.add_patch(rect)
        
        plt.show()
        
    df_log_change = pd.DataFrame()
    df_log_change["log_num"] = df_log["text"].values
    df_log_change["change_idx"] = df_log.index
    
    return df_log, df_log_change

def get_call_time(df, df_parquet):
    """ Adds call times to df.
    """
    df["call_datetime"] = np.nan
    
    # Make sure times are of the form hh:mm:ss
    valid_times = '(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])'

    for i in df.index:
        dt = df.loc[i,"date"]
        start, end = _get_start_end(df, i)
        df_i = df_parquet.loc[start:end,]
        text = " ".join(df_i["text"])
        call_time = re.findall("\d{4} ",text)
        if len(call_time) > 0:
            hr = call_time[0][:2]
            mn = call_time[0][2:].strip(" ")
            time = f"{hr}:{mn}:00"
            reg = re.match(valid_times,time)
            if reg:
                y = dt.year
                m = dt.month
                d = dt.day
                df.loc[i,"call_datetime"] = pd.to_datetime(f"{y}-{m}-{d} {hr}:{mn}:00")
            
    return df

def get_call_reason(df, df_parquet, reasons):
    """ Adds call reasons to df.
    """
    df["call_reason"] = np.nan
    reason_length = max([len(r) for r in reasons])
    
    for i in df.index:
        start, end = _get_start_end(df, i)
        df_i = df_parquet.loc[start:end,]
        text = " ".join(df_i["text"])[:reason_length]
        
        # Check for direct containment
        check_in = np.where(np.array([r in text for r in reasons]) == True)[0]
        if len(check_in) > 0:
            reason = reasons[check_in[0]]

        # Otherwise do fuzzy matching
        else:
            reason = reasons[np.array([fuzz.partial_ratio(r,text) for r in reasons]).argmax()]
            
        call_type = reason.split(" - ")[0].strip(" ")
        call_reason = reason.split(" - ")[1].strip(" ")
        
        df.loc[i,"call_type"] = call_type
        df.loc[i,"call_reason"] = call_reason
        
            
    return df

def get_call_action(df, df_parquet, actions):
    """ Adds call actions to df.
    """
    df["call_action"] = np.nan

    for i in df.index:
        start, end = _get_start_end(df, i)
        df_i = df_parquet.loc[start:end,]
        text = " ".join(df_i["text"])

        # Check for direct containment
        check_in = np.where(np.array([a in text for a in actions]) == True)[0]
        if len(check_in) > 0:
            df.loc[i,"call_action"] = actions[check_in[0]]

        # Otherwise do fuzzy matching
        else:
            action = actions[np.array([fuzz.partial_ratio(a,text) for a in actions]).argmax()]
            df.loc[i,"call_action"] = action
            
    return df

def get_call_taker(df, df_parquet, officers):
    """ Adds call taker to df.
    """
    df["call_taker"] = np.nan
    for i in df.index:
        start, end = _get_start_end(df, i)
        df_i = df_parquet.loc[start:end,]
        df_i = df_i[df_i["top"] > df_i["top"].min()].copy()
        df_i = df_i[df_i["left"] > 400].copy()
        text = " ".join(df_i["text"])

        # Check for direct containment.
        check_in = np.where(np.array([o in text for o in officers]) == True)[0]
        if len(check_in) > 0:
            officer = officers[check_in[0]]
            df.loc[i,"call_taker"] = officer

        # Otherwise fuzzy matching.
        else:
            officer = officers[np.array([fuzz.partial_ratio(o,text) for o in officers]).argmax()]
            df.loc[i,"call_taker"] = officer
        
    return df

def get_arvd_clrd_time(df, df_parquet):
    """ Adds arrival and cleared times to df. 
    """
    df["disp_datetime"] = np.nan
    df["enrt_datetime"] = np.nan
    df["arvd_datetime"] = np.nan
    df["clrd_datetime"] = np.nan
    
    # Make sure times are of the form hh:mm:ss
    valid_times = '(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])'
    
    for i in df.index:
        start, end = _get_start_end(df, i)
        dt = df.loc[i,"date"]
        df_i = df_parquet.loc[start:end,]
        df_i = df_i[df_i["top"] > df_i["top"].min()].copy()
        df_i = df_i[df_i["left"] > 400].copy()
        text = " ".join(df_i["text"])
        
        times = re.findall(valid_times,text)
        if len(times) > 0:
            for t in times:
                hr = t[0]
                mn = t[1]
                sc = t[2]
                
                y = dt.year
                m = dt.month
                d = dt.day

                if (dt.hour > 12) & (int(hr) < 12):
                    dt = call_dt + timedelta(days = 1)
                    y = dt.year
                    m = dt.month
                    d = dt.day
        
                time = ":".join(t)
                time_pre = text.split(time)[0].lower()
                if fuzz.partial_ratio("disp",time_pre) > 95:
                    df.loc[i,"disp_datetime"] = pd.to_datetime(f"{y}-{m}-{d} {hr}:{mn}:{sc}")
                if fuzz.partial_ratio("enrt",time_pre) > 95:
                    df.loc[i,"enrt_datetime"] = pd.to_datetime(f"{y}-{m}-{d} {hr}:{mn}:{sc}")
                if fuzz.partial_ratio("arvd",time_pre) > 95:
                    df.loc[i,"arvd_datetime"] = pd.to_datetime(f"{y}-{m}-{d} {hr}:{mn}:{sc}")
                if fuzz.partial_ratio("clrd",time_pre) > 95:
                    df.loc[i,"clrd_datetime"] = pd.to_datetime(f"{y}-{m}-{d} {hr}:{mn}:{sc}")
                
                text = text.split(time)[-1]
    return df

def get_responding_units(df, df_parquet):
    """ Adds responding units to df.
    """
    df["responding_units"] = np.nan
    valid_units = '( [0-9][0-9] | [0-9][0-9]k | [0-9][0-9] )'
    for i in df.index:
        start, end = _get_start_end(df, i)
        df_i = df_parquet.loc[start:end,]
        df_i = df_i[df_i["top"] > df_i["top"].min()].copy()
        df_i = df_i[(df_i["left"] > 300)&(df_i["left"] < 600)].copy()
        text = " ".join(df_i["text"]).lower()
        
        units = re.findall(valid_units," "+ text + " ")
        if len(units) > 0:
            df.loc[i,"responding_units"] = ", ".join([u.strip(" ") for u in units])
                    
    return df

def get_streets(df, df_parquet, streets):
    """ Adds street names to df. 
    """
    df["street"] = np.nan
    for i in df.index:
        start, end = _get_start_end(df, i)
        df_i = df_parquet.loc[start:end,]
        df_i = df_i[df_i["top"] > df_i["top"].min()].copy()
        df_i = df_i[(df_i["left"] > 500)&(df_i["left"] < 1500)].copy()
        text = " ".join(df_i["text"])
        street = streets[np.array([fuzz.partial_ratio(s, text) for s in streets]).argmax()]
        df.loc[i,"street"] = street
        
    return df

def _get_start_end(df, idx):
    """ Gets start and end point of log entry.
    """
    start = df.loc[idx,"change_idx"] + 1
    
    if idx < df.shape[0] - 1:
        end = df.loc[idx+1,"change_idx"] - 1
    else:
        end = df.index[-1]
        
    return start, end

def get_narrative(df, df_parquet):
    """ Adds narrative text to df.
    """
    # Preprocessing
    df["narrative"] = np.nan
    for i in df.index:
        start, end = _get_start_end(df, i)
        df_i = df_parquet.loc[start:end,]

        # Find narrative text. Precondition: df_i contains all text and position information for log number i.
        text = " ".join(df_i["text"])
        text = text[text.find("Narrative:"):]
        df.loc[i,"narrative"] = text

    # Postprocessing
    df.loc[pd.isna(df["narrative"]),"narrative"] = ""
    return df

def parse_ocr_output(df_parquet, year):
    """ Parse parquet file generated in ocr step.
    """
    df_parquet.reset_index(drop = True, inplace = True)
    df_date, df_date_change = get_dates(df_parquet, year, plot = False)
    df_log, df_log_change = get_log_numbers(df_parquet, plot = False)
    
    # Merge Date and Log dataframes
    df = df_date_change.merge(df_log_change, how = "outer").sort_values(by = "change_idx")
    df["date"] = df["date"].fillna(method = "ffill")
    df.dropna(subset = ["log_num"], inplace = True)
    df.rename(columns = {"change_idx":"log_start_idx"})
    df.reset_index(drop = True, inplace = True)

    # Add pdf_page to columns
    df["pdf_page"] = df_parquet.loc[df["change_idx"].values,:]["pdf_page"].values

    # Read known data lists 
    reasons, officers, actions, streets = read_known_data_lists()

    # Get call times.
    df = get_call_time(df, df_parquet)
    df = get_arvd_clrd_time(df, df_parquet)

    # Get call reason
    df = get_call_reason(df, df_parquet, reasons)

    # Get call action
    df = get_call_action(df, df_parquet, actions)

    # Get call taker
    df = get_call_taker(df, df_parquet, officers)

    # Get responding units
    df = get_responding_units(df, df_parquet)

    # Get streets
    df = get_streets(df, df_parquet, streets)

    # Get narrative
    df = get_narrative(df, df_parquet)
    
    return df
