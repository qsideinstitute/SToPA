import logging
import sys
import os

from PIL import Image
import pytesseract
from pdf2image import pdfinfo_from_path,convert_from_path

logging.basicConfig(level=logging.INFO)


def main(argv):

    year = argv[0]
    logging.info("Parsing logs for {}".format(year))

    path = "data/primary_datasets/Logs{}.pdf".format(year)

    logging.info("\n Retrieving Pages")

    info = pdfinfo_from_path(path, userpw=None, poppler_path=None)

    maxPages = info["Pages"]

    n = 1

    # Create temporary directory for image files.
    os.mkdir("data/temp_pdf_to_jpg")

    for page in range(1, maxPages+1, 10) :
        pages = convert_from_path(path, 
                              dpi=300, 
                              first_page=page, 
                              last_page = min(page+10-1,maxPages),
                              thread_count = 10)
            

        logging.info("\n Retrieved Pages {} to {}.".format(n, n + len(pages)))

        for page in pages:
            # Write pdf to image file.
            img_file = 'data/{}_jpg_logs/out_{}.jpg'.format(year,n)
            page.save(img_file.format(n),"JPEG")


            # Write image file to text file.
            text_file = open('data/{}_text_logs/page_{}.txt'.format(year,n), 'w')
            text=str(pytesseract.image_to_string(Image.open(img_file),lang='eng', config='--psm 12'))  # 12
            text=text.replace("\n"," ") # make spaces instead of lose info

            text_file.write(text)
            text_file.close()
            
            
            #and delete image file
            os.remove(img_file)

            n += 1

    # Delete temporary directory for image files.
    os.rmdir("data/pdf_to_jpg")

if __name__ == "__main__":
    main(sys.argv[1:])
