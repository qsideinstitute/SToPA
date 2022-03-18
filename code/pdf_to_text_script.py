import logging
import sys
import os

# import settings.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath("settings.py"))))
import settings

import cv2 as cv
import pandas as pd
from numpy import array

import pytesseract
from pdf2image import pdfinfo_from_path,convert_from_path

# Check path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

# TODO: put the level of 5 as a parameter in the settings. (note: this is below logging.DEBUG, at 10)
VERBOSE_LOGLEVEL = 5    # for logging.log() messages about individual file creation/deletion

logging.basicConfig(level = VERBOSE_LOGLEVEL) # display messages with level (priority) >= level defined here.
# note by default:
# logging.DEBUG -> 10
# logging.INFO -> 20
# logging.ERROR -> 40

def _soft_mkdir(fname):
    '''
    Checks to see if folder exists; if yes, displays warning. Otherwise makes folder.
    Then returns the input.
    '''
    if not os.path.exists(fname):
        os.mkdir(fname)
    else:
        logging.warning("Folder {} already exists; temp files may be overwritten.".format(fname))
    return

def main(argv):

    year = argv[0]
    logging.info("Parsing logs for {}".format(year))

    try:
        pdfpath = settings.PDF_DICT[ year ]
    except:
        logging.error("Error finding logs. Expecting data in location:")
        logging.error("[PROJECT_FOLDER]/data/primary_datasets/Logs{}.pdf\n".format(year))
        raise Exception("Failed to load logs for input year {}.".format(year))


    logging.info("\n Retrieving Pages")

    pdf_info = pdfinfo_from_path(pdfpath, userpw=None, poppler_path=None)

    max_pages = pdf_info["Pages"]

    # subfolder for specific year's text files.
    _soft_mkdir( settings.DATA_FOLDER )
    TEMP_TXT_FOLDER = os.path.join( settings.DATA_FOLDER, "{}_text_logs".format(year) )
    _soft_mkdir( TEMP_TXT_FOLDER )

    # TODO: consider moving these to optional arguments of the function and/or argv[1], sys.argv[2]
    first_page_to_parse = 1
    last_page_to_parse = max_pages # use max_pages for entire pdf file's logs.
    for pagenum in range(first_page_to_parse, last_page_to_parse+1, settings.BATCHSIZE):
        pages = convert_from_path(pdfpath,
                              dpi = settings.DPI,
                              first_page = pagenum,
                              last_page = min(pagenum + settings.BATCHSIZE - 1, last_page_to_parse),
                              thread_count = settings.MAXTHREADS)

        logging.info("\n Retrieved Pages {} to {}.".format(pagenum, pagenum + len(pages) - 1))

        for i,page in enumerate(pages):

            # Write image file to text file.
            TXT_FILENAME = os.path.join( TEMP_TXT_FOLDER, "page_{}.txt".format(pagenum+i) )
            text_file = open( TXT_FILENAME, 'w')

            # preprocess the image a bit
            tmp,img  = cv.threshold(array(page),settings.THRESH,255,cv.THRESH_BINARY)
            img = cv.dilate(img, settings.KERNEL, iterations=1)
            img = cv.erode(img, settings.KERNEL, iterations=2)

            # run tesseract OCR to dataframe with bounding box location
            df=pytesseract.image_to_data(img,
                                          output_type = pytesseract.Output.DATAFRAME,
                                          lang='eng',
                                          config=settings.CONFIG)

            # use box location to correctly order words
            df['mean_y']=df.top+0.5*df.height # compute mean y box location
            df['binned'] = pd.cut(df['mean_y'], settings.N_LINES, labels=settings.LINE_LABELS) # bin by line number
            df = df.sort_values(['binned', 'left']).dropna() # sort by line number bin, then by x location
            # df.to_csv('data/frames/page_{}.csv'.format(n))  # save dataframe to csv if desired, bounding box included
            df = df.groupby(['binned'],observed=True)['text'].apply(' '.join).reset_index() # join text strings by line
            text = df['text'].str.strip().str.cat(sep="\n") # clean up string data

            # TODO: look over/validate this choice. Kept as of 2/25 to be compatible with parsing script
            text=text.replace("\n"," ") # make spaces instead of lose info

            text_file.write(text)
            logging.log(VERBOSE_LOGLEVEL, "Text written: {}".format(os.path.basename(TXT_FILENAME)))

            text_file.close()

        # end for
    # end for

    # Finished.
    logging.info("Finished processing with inputs {}".format(sys.argv[1:]))

if __name__ == "__main__":
    main(sys.argv[1:])
