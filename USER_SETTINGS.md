# OCR Settings and User-Input Dictionaries 

### Overview
The settings file defines the path structure of the PDF processing and various image processing and OCR parameters that should be tuned for each dataset. To learn about what OCR is, how it is used, and what the image processing pipeline is doing, see   this [overview of OCR and Pytesseract](https://nanonets.com/blog/ocr-with-tesseract/#ocr-with-pytesseract-and-opencv), the [Tesseract manual](https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc), and this [guide to image quality improvement](https://tesseract-ocr.github.io/tessdoc/ImproveQuality). 

### User-input words and patterns
Two files allow a user amend the default dictionary with patterns or words specific to their application: `eng.my-patterns` and `eng.my-words`. Each file should contains patterns or words separated by a line return. For a simple example, see the [Tesseract documentation](https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc). The pattern are input as a limit regular expression search, for details on valid patterns, see [the description here](https://github.com/tesseract-ocr/tesseract/blob/main/src/dict/trie.h#L184). If you edit these, make sure that the files maintain the .my-pattern extension, rather than converting to eng.my-pattern.rtf! Blacklisting or whitelisting characters may also be helpful, and is described below.

### Parameters 
When using `pdf_to_text_script.py`, make sure you check that the following parameters in `settings.py` work well for your dataset:

| Parameter      | Description |
| ----------- | ----------- |
| DPI      | dots per inch to convert PDF to image       |  
| KERNEL   | denoising kernel, change from 3 to any odd number if text is fuzzy or disappearing, see [OpenCV Image Transformations](https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html)
| THRESH      | BW image threshold, pixels > THRESH go to 255, see [OpenCV Image Thresholding](https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html#thresholding)
| N_LINES      | total possible lines of text in your PDF file, including empty lines, for binning
| BLACKLIST | list of characters to try to exclude from search library 
| CONFIG | PyTesseract configuration parameters, change page segmentation method (PSM) if desired 
