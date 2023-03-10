#
# Functions for matching a specific field given the tesseract OCR of 
# the Rochester Genl101A forms.
#
import re

def null(sl):
    '''sl: list of strings coming from OCR'''
    return ''

def matcher(pattern,sl):
    # TODO: this is very inefficient because every function needs to 
    # scan the entire document (O(n^2)). *Knowing* the order, build a class
    # which tracks the index to turn the overall scan to an O(n) operation.
    # (only a single scan through is needed)
    for l in sl:
        m = re.match(pattern,l)
        if m:
            return m.groups(0)[0]
    return ''

def defendant(sl):
    flag = False
    for l in sl:
        if l=='VS':
            flag = True
            continue
        if flag and len(l)>0:
            return l
    return ''

def utt_number(sl):
    pattern = 'UTT NUMBER ([A-Z0-9]{1,})'
    return matcher(pattern,sl)


def officer(sl):
    pattern = 'Officer ([a-zA-Z\ ]{1,}) of the '
    return matcher(pattern,sl)

def law(sl):
    pattern = '1. \(Law/Section/Subsection\) ([A-Z0-9]{1,})'
    return matcher(pattern,sl)

def description(sl):
    pattern = '2. Description of Violation (.+)'
    return matcher(pattern,sl)

# passing on 3. and 4. because i need to capture multiple groups
def direction(sl):
    pattern = '5. General Direction of Travel by Defendant: ([A-Z]{1,})'
    return matcher(pattern,sl)

def highway(sl):
    pattern = '6. Highway (Type/Name) (.+)'
    return matcher(pattern,sl)

def charge_base(sl):
    pattern = "7. Charge based on Officer's (.+)"
    return matcher(pattern,sl)

def officer_narrative(sl):
    flag = False
    narrative = []
    for l in sl:
        if l=='8. Additional Information:':
            flag = True
            continue
        if l=='TO THE ABOVE NAMED DEFENDANT:':
            break
        if flag and len(l)>0:
            narrative.append(l)
    narrative = ' '.join(narrative) # join the lines with a white space
    return narrative

