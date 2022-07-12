""" Script to write parquet to csv with data processing steps. 
"""
import git
import os
import pandas as pd

from datetime import date
from os import listdir
from os.path import isfile, join

import sys
sys.path.append('..')
import src as tools

GIT_REPO = git.Repo(os.path.abspath(""), search_parent_directories=True)
PROJECT_FOLDER = GIT_REPO.git.rev_parse("--show-toplevel")

def main(argv):
    n_pages = 5
    year = argv[0]
    today = str(date.today()).replace("-","_")

    # Read available parquet files.
    my_path = f"{PROJECT_FOLDER}/data/{year}_parquet_logs"
    files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    files.sort()

    df_parquet = pd.DataFrame()
    for f in files:
        df_parquet = pd.concat([df_parquet,pd.read_parquet(f"{my_path}/{f}")])
        
    df_parquet.reset_index(drop = True, inplace = True)

    df = tools.parse_ocr_output(df_parquet, int(year))
    filepath = f"{PROJECT_FOLDER}/data/{today}_parsed_{year}.csv"
    df.to_csv(filepath)
    print(f"Data printed to {filepath}")

if __name__ == "__main__":
    main(sys.argv[1:])