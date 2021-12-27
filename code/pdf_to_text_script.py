import logging
import sys
import os

# hacky reference to parent directory with settings.

# TODO: decide whether we want project structure to work this way.
# Alternative is to force users to always interact with the top-level directory 
# only, and import stuff in the "code" subdirectory rather than running it directly.
sys.path.append(os.path.abspath('..'))
import settings

from PIL import Image
pytesseract = settings.pytesseract
from pdf2image import pdfinfo_from_path,convert_from_path

#
pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_EXECUTABLE

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

    # Create temporary directory for image files.
    TEMP_FOLDER = os.path.join( settings.DATA_FOLDER, 'TEMP' )
    _soft_mkdir( TEMP_FOLDER )

    # subfolder for specific year's logs as jpg files
    TEMP_JPG_FOLDER = os.path.join( TEMP_FOLDER, "{}_jpg_logs".format(year) )
    _soft_mkdir( TEMP_JPG_FOLDER )

    # subfolder for specific year's text files.
    _soft_mkdir( settings.TEXT_OUTPUT_FOLDER )
    TEMP_TXT_FOLDER = os.path.join( settings.TEXT_OUTPUT_FOLDER, "{}_text_logs".format(year) )
    _soft_mkdir( TEMP_TXT_FOLDER )
    
    

    # TODO: consider moving these to optional arguments of the function and/or argv[1], sys.argv[2]
    FIRST_PAGE = 1
    LAST_PAGE = 10   # use max_pages for entire pdf file's logs.
    for pagenum in range(FIRST_PAGE, LAST_PAGE+1, settings.BATCHSIZE):
        BATCHSIZE = settings.BATCHSIZE
        pages = convert_from_path(pdfpath, 
                              dpi = settings.DPI, 
                              first_page = pagenum, 
                              last_page = min(pagenum + settings.BATCHSIZE - 1, LAST_PAGE),
                              thread_count = settings.MAXTHREADS)
            

        logging.info("\n Retrieved Pages {} to {}.".format(pagenum, pagenum + len(pages) - 1))

        for i,page in enumerate(pages):
            # Write pdf to image file.
            IMG_FILENAME = os.path.join( TEMP_JPG_FOLDER, "out_{}.jpg".format(pagenum+i) )
            page.save(IMG_FILENAME, "JPEG")
            logging.log(VERBOSE_LOGLEVEL, "Image written: {}".format(os.path.basename(IMG_FILENAME)))


            # Write image file to text file.
            TXT_FILENAME = os.path.join( TEMP_TXT_FOLDER, "page_{}.txt".format(pagenum+i) )
            text_file = open( TXT_FILENAME, 'w')
            
            text=str(pytesseract.image_to_string(Image.open(IMG_FILENAME), lang='eng', config='--psm 12'))  # 12
            
            # TODO: look over/validate this choice.
            text=text.replace("\n"," ") # make spaces instead of lose info

            text_file.write(text)
            logging.log(VERBOSE_LOGLEVEL, "Text written: {}".format(os.path.basename(TXT_FILENAME)))
            
            text_file.close()
            
            #and delete image file
            if settings.CLEAN_TEMP_FILES:
                os.remove(IMG_FILENAME)
                logging.log(VERBOSE_LOGLEVEL, "Image deleted: {}".format(os.path.basename(IMG_FILENAME)))
        # end for
    # end for
    
    # Finished.
    # Delete temporary directory for image files.
    if settings.CLEAN_TEMP_FILES:
        # if there is any other content in the same TEMP_JPG_FOLDER, then *don't* delete everything;
        # only the tmep files related to the file for the current call to the function.
        if len( settings.glob.glob( os.path.join(TEMP_FOLDER, '*') ) ) > 1:
            logging.info("Other folders in {}; only deleted relevant temp data for this run.".format(TEMP_JPG_FOLDER))
            os.rmdir( TEMP_JPG_FOLDER )
            logging.log(VERBOSE_LOGLEVEL, "Folder deleted: {}".format(TEMP_JPG_FOLDER))
        else:
            # delete all temp data.
            os.rmdir( TEMP_JPG_FOLDER )
            logging.log(VERBOSE_LOGLEVEL, "Folder deleted: {}".format(TEMP_JPG_FOLDER) )
            os.rmdir( TEMP_FOLDER )
            logging.log(VERBOSE_LOGLEVEL, "Folder deleted: {}".format(TEMP_FOLDER) )
    
    logging.info("Finished processing with inputs {}".format(sys.argv[1:]))

if __name__ == "__main__":
    main(sys.argv[1:])
