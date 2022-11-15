"""OCR Tools for WPD Data
"""
import cv2 as cv
import git
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import pandas as pd
import pytesseract

from deskew import determine_skew
from pdf2image import convert_from_path
from skimage import io
from skimage.transform import rotate

import src.settings as settings
from src.processing_tools import get_log_numbers




def get_pages_from_pdf(year = 2019, first_page =1, last_page = 5, plot = False): 
    """ Performs OCR with tesseract on given pages.

    INPUTS: 
        year: (int) 2019 or 2020
        first_page: (int) pdf page on which to start.
        last_page: (int) pdf page on which to end.
        plot: (bool) Saves plots to file if True.

    RETURNS: 
        Dataframe with tesseeract output for given pages.
    """ 
    # obtain image from pdf
    pdfpath = f"{settings.PROJECT_FOLDER}/data/primary_datasets/Logs{year}.pdf"
    pages = convert_from_path(pdfpath,
                                  dpi = 300,
                                  first_page = first_page,
                                  last_page = last_page,
                                  thread_count = 4)

    df = pd.DataFrame()
    for i,page in enumerate(pages):
        img = np.array(page) # convert PIL Image to numpy array

        # deskew image
        angle = determine_skew(img)
        img = rotate(img, angle, resize=True) * 255
        img = img.astype(np.uint8) # re-cast to unsigned integer; skimage.transform.rotate apparently changes this

        # clip scanning boundaries
        img = img[50:-50,50:-50]
        
        # denoise image
        img = cv.fastNlMeansDenoising(img, h = 50)

        # binary threshold
        _ ,img  = cv.threshold(img,150,255,cv.THRESH_BINARY)

        # complete ocr
        df_ocr=pytesseract.image_to_data(img,
                                output_type = pytesseract.Output.DATAFRAME,
                                lang='eng',
                                config=settings.CONFIG)
        df_ocr.dropna(subset = ["text"], axis = 0, inplace = True)
        
        #Check that page has contents.
        if df_ocr.shape[0] > 0:

            # Round top boundary to the nearst 25.
            df_ocr["top"] = [int(y/25) * 25 for y in df_ocr["top"]]
            df_ocr["height"] = df_ocr["height"] + 25
            
            # Remove margins
            left_bound = df_ocr["left"].min()
            right_bound = (df_ocr["left"] + df_ocr["width"]).max()
            top_bound = df_ocr["top"].min()
            bottom_bound = (df_ocr["top"].max() + df_ocr["height"]).max()

            
            img = img[top_bound:bottom_bound + 1,left_bound:right_bound]
            df_ocr["left"] = df_ocr["left"] - left_bound
            df_ocr["top"] = df_ocr["top"] - top_bound
            cv.imwrite(f'{settings.PROJECT_FOLDER}/data/{year}_image_logs/page_{first_page + i}.png',img)

            # Sort values.
            df_ocr.sort_values(by = ["top","left"], inplace = True)
            df_ocr.reset_index(drop = True, inplace = True)
            df_ocr["pdf_page"] = first_page + i

            df = pd.concat([df,df_ocr])
            
            if plot == True:

                # plot output and save to file
                plt.ioff()
                fig, ax = plt.subplots(figsize = (15,20))
                ax.imshow(img)
                for idx in df_ocr.index:
                    left = df_ocr.loc[idx,"left"]
                    top = df_ocr.loc[idx,"top"]
                    w = df_ocr.loc[idx,"width"]
                    h = df_ocr.loc[idx,"height"]
                    ax.annotate(xy = (left,top), text = idx)
                    # Create a Rectangle patch
                    rect = patches.Rectangle((left, top), w, h, linewidth=1, edgecolor='r', facecolor='none')

                    # Add the patch to the Axes
                    ax.add_patch(rect)
                plt.savefig(f'{settings.PROJECT_FOLDER}/data/{year}_image_bbox_logs/page_{first_page + i}.png')
                plt.close(fig)
            
        
    return df

def confirm_parsed_log_entry(df, entry_index = None): 
    """ prints image of log entry

    INPUTS: 
        entry_index: (int) index value from parsed_df, if None,
            choose one at random.
        df: (dataframe) parsed logs 

    RETURNS: 
        Plot with log entry and dataframe row.
    """ 
    if entry_index is None:
        entry_index = np.random.choice(df.index)

    entry = df.iloc[[entry_index],:]
    year = entry["date"].iloc[-1].year
    pdf_page = entry["pdf_page"].iloc[-1]
    log_num = entry["log_num"].iloc[-1]

    # obtain image from pdf
    pdfpath = f"{settings.PROJECT_FOLDER}/data/primary_datasets/Logs{year}.pdf"
    page = convert_from_path(pdfpath,
                                  dpi = 300,
                                  first_page = pdf_page,
                                  last_page = pdf_page,
                                  thread_count = 4)

    page[0].save(f'out.png', 'png')

    # deskew image
    img = io.imread(f'out.png')
    angle = determine_skew(img)
    img_rotated = rotate(img, angle, resize=True) * 255
    io.imsave(f'out.png', img_rotated.astype(np.uint8))

    # clip scanning boundaries
    img_clipped = img[50:-50,50:-50]
    cv.imwrite(f'out.png',img_clipped)

    # denoise image
    img = io.imread('out.png')
    img_denoised = cv.fastNlMeansDenoising(img, h = 50)

    # binary threshold
    _ ,img  = cv.threshold(img_denoised,150,255,cv.THRESH_BINARY)

    # complete ocr
    df_ocr=pytesseract.image_to_data(img,
                            output_type = pytesseract.Output.DATAFRAME,
                            lang='eng',
                            config=settings.CONFIG)
    df_ocr.dropna(subset = ["text"], axis = 0, inplace = True)

    #Check that page has contents.
    if df_ocr.shape[0] > 0:

        # Round top boundary to the nearst 25.
        df_ocr["top"] = [int(y/25) * 25 for y in df_ocr["top"]]
        df_ocr["height"] = df_ocr["height"] + 25

        # Remove margins
        left_bound = df_ocr["left"].min()
        right_bound = (df_ocr["left"] + df_ocr["width"]).max()
        top_bound = df_ocr["top"].min()
        bottom_bound = (df_ocr["top"].max() + df_ocr["height"]).max()

        # Crop image.
        img = img[top_bound:bottom_bound + 1,left_bound:right_bound]
        df_ocr["left"] = df_ocr["left"] - left_bound
        df_ocr["top"] = df_ocr["top"] - top_bound

        # Sort values.
        df_ocr.sort_values(by = ["top","left"], inplace = True)
        df_ocr.reset_index(drop = True, inplace = True)
        df_ocr["pdf_page"] = pdf_page

        df = pd.concat([df,df_ocr])
        df_log, df_log_change = get_log_numbers(df)

        idx = df_log[df_log["text"] == log_num].index[0]
        y_max = df_log.loc[idx,"top"]
        if df_log.loc[idx:,].shape[0]>1:
            df_next = df_log.iloc[np.where(df_log.index == idx)[0][0] + 1:,]
            y_min = df_next["top"].iloc[0]
        else:
            y_min = df["top"].max()
        
        idx = df_ocr[df_ocr["text"] == log_num].index[0]
        left = df_ocr.loc[idx,"left"]
        top = df_ocr.loc[idx,"top"]
        w = df_ocr.loc[idx,"width"]
        h = df_ocr.loc[idx,"height"]
        
        # Make plot
        fig, ax = plt.subplots(figsize = (15,20))
        ax.imshow(img)
        rect = patches.Rectangle((left, top), w, h, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        ax.set_ylim(y_min, y_max)
        plt.show()
    os.remove(f"out.png")
        
    return entry
