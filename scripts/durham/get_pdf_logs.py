""" Script to obtain Durham PD records
"""
import os
import pandas as pd
import sys

from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join

sys.path.append('../..')
import src as tools

def get_pdf_logs(start_date, end_date):
	"""
	Arguments: 
		start_date: (str) date in format YYYY-mm-dd
		end_date: (str) date in format YYYY-mm-dd

	Returns:
		Downloads and saves all reports from <start_date> through <end_date>
		and saves them in ../../data/durham/<year>/.
	"""
	start = pd.to_datetime(start_date)
	stop = pd.to_datetime(end_date)

	#track the dates that did not work
	fail_list=[]
	while start < stop:

	    #get the pdfs
	    cnt=0
	    # Attempt to scrape a date up to 10 times
	    success=False
	    while cnt<10:
	        scrape=tools.download_pdfs(start.strftime("%m/%d/%Y"))
	        if scrape==1:
	            print(start.strftime("%m/%d/%Y"), 'scrape succeeded')
	            success=True
	            break
	        else:
	            print(start.strftime("%m/%d/%Y"), 'scrape failed')
	            cnt += 1
	    #If the scrape for the date fails 10 times add it to a list
	    if not success:
	        fail_list.append(start.strftime("%m/%d/%Y"))

	    start = start + timedelta(days=1)  # increase day one by one

	print(fail_list)

if __name__ == "__main__":
	start_date = sys.argv[1]
	end_date = sys.argv[2]
	get_pdf_logs(start_date, end_date)

	year = start_date.split("-")[0]
	dir_path = f"../../data/durham/{year}"
	dir_list = [f for f in os.listdir(dir_path) if not isfile(f)]
	dir_list.sort()
	for d in dir_list:
		month = d[:2]
		day = d[2:]
		report_date = f"{day}/{month}/{year}"
		tools.split_arrests_and_incidents(report_date)

	tools.merge_reports_by_type(year)