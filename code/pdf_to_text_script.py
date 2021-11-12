import logging
import sys
import os

from PIL import Image
import pytesseract
from pdf2image import pdfinfo_from_path,convert_from_path

logging.basicConfig(level=logging.INFO)


YEAR = 2019 #2020
PATH_TO_DATA = "data/primary_datasets/Logs{}.pdf".format(YEAR)


def main(argv):

    logging.info("\n Retrieving Pages")

    info = pdfinfo_from_path(PATH_TO_DATA, userpw=None, poppler_path=None)

    maxPages = info["Pages"]

    n = 1

    for page in range(1, maxPages+1, 10) :
        pages = convert_from_path(PATH_TO_DATA, 
                              dpi=300, 
                              first_page=page, 
                              last_page = min(page+10-1,maxPages),
                              thread_count = 10)
            

        logging.info("\n Retrieved Pages {} to {}.".format(n, n + len(pages)))

        for page in pages:
            # Write pdf to image file.
            img_file = 'data/{}_jpg_logs/out_{}.jpg'.format(YEAR,n)
            page.save(img_file.format(n),"JPEG")


            # Write image file to text file.
            text_file = open('data/{}_text_logs/page_{}.txt'.format(YEAR,n), 'w')
            text=str(pytesseract.image_to_string(Image.open(img_file),lang='eng', config='--psm 12'))  # 12
            text=text.replace("\n"," ") # make spaces instead of lose info

            text_file.write(text)
            text_file.close()
            
            
            #and delete image file
            os.remove(img_file)

            n += 1


if __name__ == "__main__":
    main(sys.argv[1:])
