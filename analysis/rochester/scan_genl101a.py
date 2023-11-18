
# BIG todo: modularize ocr_tools.py and what I use here 
# to flexibly... enough? make the same tools useable between 
# (e.g.) Rochester pdf files, and Williamstown files, and others.

from collections import OrderedDict

# my local scripts
import inventory
import parse

####################

import numpy as np
import pandas

'''
python packages to install via pip...

opencv-python (may need to update numpy)
pdf2image
deskew
pytesseract
'''

import cv2 # for denoising and thresholding -- pip install opencv-python


import pdf2image # convert pdf file to 3D array

import deskew # for estimating an angle the document may be rotated by
import skimage # for rotating the image by a pre-determined angle.

import pytesseract # for main OCR step (image to text dataframe)

#################

#########################################################
TESS_BLACKLIST = ";{}&£~=%¥€@|" # characters we want to specifically exclude from the OCR

DPI = 300

#Pyesseract config string
TESS_CONFIG = '-c tessedit_char_blacklist={} \
        --psm 1 \
        --dpi {} \
        --user-patterns eng.my-patterns \
        --user-words eng.my-words'.format(TESS_BLACKLIST,DPI)
###############



def row_ize(arr):
    '''
    Work with the dataframe output of the OCR ("df['text'].values")
    and parse consecutive lines; np.nan marks line breaks, while strings 
    mark elements within one line.
    
    Outputs a list of strings.
    '''
    import numpy as np
    rows = []
    row = []
    for t in arr:
        if not type(t)==str:
#        if np.isnan(t):
            rows.append(' '.join(row))
            row = []
        else:
            row.append(t)
    return rows

def process_all_genl101a(df_tess):
    '''
    Purpose: process the output of tesseract on the Rochester Genl101A forms.
    Inputs: 
        df_tess: pandas.DataFrame
    Outputs: 
        info: cleaned dataframe with the following columns. Note these are 
        directly based on the form's top fields as well as items 1. through 8.
            "field" - 
                defendant
                utt_number
                officer
                law
                description
                date
                time
                C/T/V
                vehicle_year
                vehicle_make
                direction_travel
                highway_type/name
                charge_base
                officer_narrative
            "value" -
                string associated with each of the above.
    Items 1 through 8 in the form are inferred from the dataframe 
    based on the regularity of the form (string numbers 1. through 8. 
    immediately followed by their values.)
    '''
    import re
    
    
    df_tess.sort_values(['top', 'left'], inplace=True) # row-order sorting if not already
    for row in df_tess.iloc:
        
#        match 
        pass
    pass


def process_genl101a(genl101a_pdf_path):
    '''
    Input: genl101a_pdf_path: string; location of pdf file assumed to 
    follow format of Genl101a files.
    
    Output: dictionary with key/values:
        'img' : numpy array of processed/cleaned pdf as image, dtype uint8
        'df_ocr' : DataFrame of identified text elements via pytesseract
        'elements' : DataFrame with summarized elements (work in progress)
    '''
    
    #
    matchy = OrderedDict({
        'defendant' :           {'op': parse.defendant, 'value':''},
        'utt_number' :          {'op': parse.utt_number, 'value':''},
        'officer' :             {'op': parse.officer, 'value':''},
        'law' :                 {'op': parse.law, 'value':''},
        'description' :         {'op': parse.description, 'value':''},
        'date' :                {'op': parse.date, 'value':''},
        'time' :                {'op': parse.time, 'value':''},
        
        'C/T/V' :               {'op': parse.null, 'value':''},
        'vehicle_year' :        {'op': parse.null, 'value':''},
        'vehicle_make' :        {'op': parse.null, 'value':''},
        
        'direction_travel' :    {'op': parse.direction, 'value':''},
        'highway_type/name' :   {'op': parse.highway, 'value':''},
        'charge_base' :         {'op': parse.charge_base, 'value':''},
        'officer_narrative' :   {'op': parse.officer_narrative, 'value':''}
    })

    pages = pdf2image.convert_from_path(genl101a_pdf_path,
                                  dpi = DPI,
                                  first_page = 1,
                                  last_page = 1,
                                  thread_count = 4)

    pg = pages[0]

    # cast image to numpy array
    img = np.array(pg)
    # rotate (deskew)
    angle = deskew.determine_skew(img)
    img = skimage.transform.rotate(img, angle, resize=True)*255
    # cast back to uint8
    img = img.astype(np.uint8)
    # denoise image
    img = cv2.fastNlMeansDenoising(img, h = 50)
    # threshold to binary values (currently manually done)
    _ ,img  = cv2.threshold(img,150,255, cv2.THRESH_BINARY)

    # pandas dataframe of page elements.
    df_ocr = pytesseract.image_to_data(
        img, 
        output_type=pytesseract.Output.DATAFRAME, 
        lang='eng', 
        config=TESS_CONFIG
    )

    ######################

    text_rows = row_ize(df_ocr['text'].values)

    for k in matchy.keys():
        matchy[k]['value'] = matchy[k]['op'](text_rows)
    #    print(k, matchy[k]['value'])
    
    row = [genl101a_pdf_path] + [v['value'] for v in matchy.values()]

    df_pdf_elements = pandas.DataFrame([row], columns=['path'] + list(matchy.keys()))
    
    output = {
        'img' : img,
        'df_ocr' : df_ocr,
        'elements' : df_pdf_elements
    }
    
    return output
#

##################


if __name__=="__main__":

    output = []
    subset = inventory.df[ inventory.df['form_type']=='Genl101A' ]
    for row in subset.iloc:
        print(row['filename'])
        quoi = process_genl101a( row['filename'] )
#        output.append( [pdfpath] + [v['value'] for v in matchy.values()] )
        output.append(quoi['elements'])

    df = pandas.concat(output, ignore_index=True)

    if False:
        from matplotlib import pyplot
        fig,ax = pyplot.subplots()
        ax.imshow(img, cmap=pyplot.cm.Greys_r)
        fig.show()


