#
# Functions for matching a specific field given the tesseract OCR of 
# the Rochester Genl101A forms.
#
import re
import datetime

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
            gg = m.groups()
            if len(gg)==1:
                return gg[0]
            else:
                return gg
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

# handle these date and time fields specially
def date(sl):
    pattern = '3. Date[\ ]+([0-9\/]{2,})'
    result = matcher(pattern,sl)
    
#    obj = datetime.datetime(year=int(result[2]), month=int(result[0]), day=int(result[1]))
    try:
        obj = datetime.datetime.strptime(result, '%m/%d/%Y')
    except:
        obj = result
    return obj

def time(sl):

    # TODO: a few times are missing AM/PM (likely PM); handle in some way.
    # may have to be an ugly heuristic.
    pattern = '.+Time[\ ]+([0-9A-Z\:]{1,})'
    result = matcher(pattern,sl)
    try:
        obj = datetime.datetime.strptime(result, '%I:%M%p')
    except:
        obj = result
    return obj

def datetime(sl):
    # e.g., "3. Date 01/20/2022    Time 7:08 PM"
    pattern = '3. Date[\ ]+([0-9\/]{2,}).+Time[\:\ ]+([0-9\:]{1,})[\ ]{0,}([A-Z]{0,})'
    result = matcher(pattern,sl)
    # TODO: some entries still don't match; investigate manually.
    if len(result)!=3:
        return date(sl) # just capture calendar date only
    
    dmy,hm,ampm = result
    if len(ampm)==0:
        apmpm='PM' # TODO: how else to handle this? Heuristic regardless, if not included.
    try:
        obj = datetime.datetime.strptime(' '.join([dmy,hm,ampm]), '%m/%d/%Y %I:%M%p')
    except:
        obj = ' '.join([dmy,hm,ampm])
    return obj
#

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
            flag = True # begin joining words scanned on the next iteration
            continue
        if l=='TO THE ABOVE NAMED DEFENDANT:':
            # this is the start of the "footer" of the form; so the narrative
            # is over at this point.
            break
        if flag and len(l)>0:
            narrative.append(l)
    narrative = ' '.join(narrative) # join the lines with a white space
    return narrative

