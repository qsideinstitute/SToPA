import os   # build folder locations independent of operating system
import glob # used to search for file(s) using wildcard *
import shutil
import warnings

# Strings of absolute folder locations for the entire project.
# If you clone the repository, these match that structure, and nothing needs to be done.

PROJECT_FOLDER = os.path.abspath(
    os.path.dirname( os.path.dirname( __file__ ) ) # ../
)

DATA_FOLDER = os.path.abspath(
    os.path.join(PROJECT_FOLDER, 'data')    # '../data/'
)

PDF_FOLDER = os.path.abspath(
    os.path.join(DATA_FOLDER, 'primary_datasets') # ../data/primary_datasets/
)

CODE_FOLDER = os.path.abspath(
    os.path.join(PROJECT_FOLDER, 'code')  # ../code/
)

TEST_FOLDER = os.path.abspath(
    os.path.join(PROJECT_FOLDER, 'test') # ../test/
)

PDF_FILE_SEARCH = os.path.abspath(
    os.path.join(PDF_FOLDER, '*.pdf')
)

PDF_FILES = glob.glob(PDF_FILE_SEARCH)

# make dictionary which has shortened names for the pdf files.
# ex: Logs2019.pdf maps to its full location in the operating system.
PDF_DICT = {os.path.basename(fname) : fname for fname in PDF_FILES}

# Attempt to import pytesseract;
# if it fails, none of the variables will 
# be set and a warning will be displayed.
try:
    import pytesseract
    _pytesseract_imported = True
except:
    _pytesseract_imported = False
    warnings.warn("Failed to import pytesseract; OCR capabilities disabled.")

# Pytesseract settings below
# 
if _pytesseract_imported:
    from numpy import ones,uint8
    
    # whether to delete temporary files generated during the OCR process.
    CLEAN_TEMP_FILES = True
    BATCHSIZE = 4
    MAXTHREADS = 4
    DPI = 400
    
    # image processing parameters
    KERNEL = ones((3,3), uint8) # kernel for image denoising
    THRESH = 150 # thresholding for binary image, 0-255
    
    # ocr tuning parameters
    N_LINES = 66 # total number of lines to be read in the document for clustering
    LINE_LABELS = list(range(N_LINES)) # labels for line number
    BLACKLIST = ";{}&£~=%¥€" # characters we want to specifically exclude from the OCR
    
    #Pyesseract config string
    CONFIG = '-c tessedit_char_blacklist={} \
            --psm 1 \
            --dpi {} \
            --user-patterns eng.my-patterns \
            --user-words eng.my-words'.format(BLACKLIST,DPI)
    
    # Is the default "tesseract_cmd" an executable that the operating system recognizes?
    _is_tesseract_executable = os.access(shutil.which(pytesseract.pytesseract.tesseract_cmd), os.X_OK)
    if _is_tesseract_executable:
        # If yes, then set as executible command
        TESSERACT_CMD = pytesseract.pytesseract.tesseract_cmd
    else:
        # If no, then repalce with full path to the tesseract binary.
        TESSERACT_CMD = shutil.which(pytesseract.pytesseract.tesseract_cmd)
