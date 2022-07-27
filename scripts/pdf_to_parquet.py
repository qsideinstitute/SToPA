""" Script to write primary pdf to parquet
"""
import git
import numpy as np
import os
import pandas as pd
import PyPDF2

import sys
sys.path.append('..')
import src as tools

def main(argv):
    n_pages = 5
    year = argv[0]
    pdfpath = f"{tools.PROJECT_FOLDER}/data/primary_datasets/Logs{year}.pdf"
    file = open(pdfpath, 'rb')
    read_pdf = PyPDF2.PdfFileReader(file)
    total_pages = read_pdf.numPages
    first_pages = np.arange(1,total_pages,5)

    # Check that necessary directories exist and if not, create them.
    directories = ["image_bbox_logs","parquet_logs","image_logs","text_logs"]
    for d in directories:
        exists = os.path.exists(f"{tools.PROJECT_FOLDER}/data/{year}_{d}")
        if not exists:
            os.mkdir(f"{tools.PROJECT_FOLDER}/data/{year}_{d}")

    df_parsed = pd.DataFrame()
    print(f"Saving files to {tools.PROJECT_FOLDER}/data/{year}_parquet_logs/pages_xxxx_yyyy.pq")
    for i in range(len(first_pages)):
        first_page = first_pages[i]
        last_page = first_page+5-1
        if i == len(first_pages)-1:
            last_page = total_pages

        p1 = f'{first_page:04}'
        p2 = f'{last_page:04}'
        df_pages = tools.get_pages_from_pdf(year = year, first_page = first_page, last_page = last_page, plot = False)
        df_pages.to_parquet(f"{tools.PROJECT_FOLDER}/data/{year}_parquet_logs/pages_{p1}_{p2}.pq")
        print(f"Pages {p1} through {p2} saved to parquet.")

if __name__ == "__main__":
    main(sys.argv[1:])