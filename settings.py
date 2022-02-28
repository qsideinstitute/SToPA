import os   # build folder locations independent of operating system
import glob # used to search for file(s) using wildcard *
import sys

import pytesseract

# whether to delete temporary files generated during the OCR process.
CLEAN_TEMP_FILES = True
BATCHSIZE = 4
MAXTHREADS = 4
DPI = 400

# If you've installed tesseract manually, then you'll need to
# manually define the path to the executable here.
# By default, pytesseract assumes you can access this with the
# command "tesseract" in the command line.
TESSERACT_CMD = ""


# Specify tesseract location for pytesseract if its default
# location doesn't exist.

# Is the default "tesseract_cmd" an executable that the operating system recognizes?
_is_tesseract_executable = os.access( pytesseract.pytesseract.tesseract_cmd, os.X_OK )
if not _is_tesseract_executable:
    # Replace with the manually defined TESSERACT_CMD (this should be the full path to the tesseract binary).
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

# Strings of absolute folder locations for the entire project.
# If you clone the repository, these match that structure, and nothing needs to be done.
PROJECT_FOLDER = os.path.dirname( os.path.realpath(__file__) )          # get full path of this script
DATA_FOLDER = os.path.join(PROJECT_FOLDER, 'data')
PDF_FOLDER = os.path.join(DATA_FOLDER, 'primary_datasets') # ./data/primary_datasets/
CODE_FOLDER = os.path.join(PROJECT_FOLDER, 'code')  # ./code/

PDF_FOLDER = os.path.abspath(PDF_FOLDER)
CODE_FOLDER = os.path.abspath(CODE_FOLDER)

PDF_FILE_SEARCH = os.path.join(PDF_FOLDER, '*.pdf')
PDF_FILES = glob.glob(PDF_FILE_SEARCH)

#
TEXT_OUTPUT_FOLDER = os.path.join( DATA_FOLDER, 'text_logs' )

# make dictionary which has shortened names for the pdf files.
# ex: Logs2019.pdf maps to its full location in the operating system.
PDF_DICT = {os.path.basename(fname) : fname for fname in PDF_FILES}

# A couple manually defined entries for backwards compatibility.
try:
    PDF_DICT['2019'] = PDF_DICT['Logs2019.pdf']
    PDF_DICT['2020'] = PDF_DICT['Logs2020.pdf']
except:
    # Should get error only if Logs2019.pdf and Logs2020.pdf are not entries in PDF_DICT.
    # Probably only happens if the directory structure was changed.
    pass
