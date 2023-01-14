""" Data Processing Tools for Durham Data 

These tools were originally written in R by the SToPA-Durham
group.  They were translated into Python by Anna Haensch.

"""


import datetime
import os
import pandas as pd
import pdfplumber
import shutil
import time

from pathlib import Path
from os import listdir
from os.path import isfile, join

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def download_pdfs(report_date):
    """ Print report pdfs from to file.
    
    Arguments: 
        report_date: (str) date of the form dd/mm/YYYY
        
    Returns: 
        Auto pings the Durham PD citizen portal and downloads all arrests 
        and incident reports for report_date.  All pdfs will be moved into
        the directory ../data/durham/YYYY/mmdd and enumerated.
    """
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
    "download.default_directory": "~/Downloads", #Change default directory for downloads
    "download.prompt_for_download": False, #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
    })
    
    # Load Page
    driver = webdriver.Chrome(options = options)
    driver.get("https://durhampdnc.policetocitizen.com/eventsearch")
    wait = WebDriverWait(driver, 10)
    
    # Click Accept
    driver.implicitly_wait(2)
    try:
        accept_button = wait.until(
        	EC.element_to_be_clickable((
        		By.XPATH, 
        		"//*[@id='disclaimerDialog']/md-dialog-actions/button[2]/span"
        							  )))
        accept_button.click()
    except:
        accept_button = wait.until(
        	EC.element_to_be_clickable((
        		By.XPATH, 
        		"//*[@id='disclaimerDialog']/md-dialog-actions/button[2]/span"
        							  )))
        accept_button.click()

    # Click Reports
    driver.implicitly_wait(2)
    try:
        report_button = wait.until(
        	EC.element_to_be_clickable((
        		By.XPATH,
        		"//*[@id='byReportInformation-card']/md-card-title/md-card-title-text/span[1]"
        							   )))
        report_button.click()
    except: 
        report_button = wait.until(
        	EC.element_to_be_clickable((
        		By.XPATH,
        		"//*[@id='byReportInformation-card']/md-card-title/md-card-title-text/span[1]"
        							   )))
        report_button.click()
        
    # Fill in Dates
    driver.implicitly_wait(3)
    date_picker = driver.find_elements(By.CLASS_NAME, "md-datepicker-input")
    start_picker = date_picker[0]
    end_picker = date_picker[1]

    start_picker.clear()
    start_picker.send_keys(report_date)

    end_picker.clear()
    end_picker.send_keys(report_date)

    # Click Search
    driver.implicitly_wait(2)
    search_button = wait.until(EC.element_to_be_clickable((By.ID,"search-button")))
    search_button.click()

    # Allow Loading
    load_flag = True
    while load_flag == True:
        try:
            load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='event-search-results']/event-search-results/div/div[2]/div[3]/button/span")))
            load_more_button.click()
        except:
            load_more_button = driver.find_elements(
            	By.XPATH, 
            	"//*[@id='event-search-results']/event-search-results/div/div[2]/div[3]/button/span"
            										)
            assert len(load_more_button) == 0
            load_flag = False

    # Get Results 
    results = driver.find_elements(
    			By.CSS_SELECTOR,
    			"div.p2c-eventSearch-result > md-card:nth-child(1) > md-card-content:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > i:nth-child(1)"
    							   )
    for i in range(len(results)):
        results[i].click()
        time.sleep(1)

    # Results will be printed to director ../data/durham/YYYY/mmdd
    date = pd.to_datetime(report_date, format = "%m/%d/%Y")
    year = str(date.year)
    folder = str("{:02d}".format(date.month))+str("{:02d}".format(date.day))
    
    # Check that durham/YYYY directory exists
    is_dir = os.path.exists(f"../data/durham/{year}")
    if not is_dir:
        os.mkdir(f"../data/durham/{year}")

    # Check that durham/YYYY/mmdd exists.
    is_dir = os.path.exists(f"../data/durham/{year}/{folder}")    
    if not is_dir:
        os.mkdir(f"../data/durham/{year}/{folder}")
    
    # Move Results
    downloads_path = str(Path.home()/"Downloads")
    pdfs = [f for f in listdir(downloads_path) if isfile(
    							join(downloads_path, f))]
    for p in range(len(pdfs)):
        file = "{:04d}.pdf".format(p)
        origin = f'{downloads_path}/{pdfs[p]}'
        destination = f'../data/durham/{year}/{folder}/{file}'
        shutil.move(origin, destination)
    
    # Close Browser
    driver.quit()


def split_arrests_and_incidents(report_date):
    """ split arrests and incidents by date.
    
    Arguments: 
        report_date: (str) date of the form dd/mm/YYYY
        
    Returns: 
        Auto pings the Durham PD citizen portal and downloads all arrests 
        and incident reports for report_date.  All pdfs will be moved into
        the directory ../data/durham/YYYY/mmdd and enumerated.
    """
    arrests = 0
    incidents = 0
    unknown = 0
    
    date = pd.to_datetime(report_date)
    year = date.year
    day = "{:02d}".format(date.day)
    month = "{:02d}".format(date.month)
    dir_path = f"../data/durham/{year}/{month}{day}"

    arrest_dir = f"{dir_path}/arrests"
    if not os.path.exists(arrest_dir):
        os.mkdir(arrest_dir)
    incident_dir = f"{dir_path}/incidents"
    if not os.path.exists(incident_dir):
        os.mkdir(incident_dir)

    file_list = [f for f in os.listdir(dir_path) if isfile(join(dir_path,f))]
    file_list.sort()

    for f in file_list:
        file = join(dir_path,f)
        pdf = pdfplumber.open(file)
        page = pdf.pages[0]
        text = page.extract_text()
        if text.split("\n")[0] == 'INCIDENT/INVESTIGATION':
            count = "{:04d}".format(incidents)
            destination = f"{dir_path}/incidents/{count}.pdf"
            incidents += 1
            shutil.move(file, destination)
        elif text.split("\n")[0] == 'ARREST REPORT':
            count = "{:04d}".format(arrests)
            destination = f"{dir_path}/arrests/{count}.pdf"
            arrests += 1
            shutil.move(file, destination)
        
    return arrests, incidents