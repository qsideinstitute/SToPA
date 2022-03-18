import logging
import sys
import os
import re
import itertools

from fuzzywuzzy.fuzz import ratio, partial_ratio
import usaddress

import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO)


taker_strs = "|".join(["Call Taker;", "‘Call Taker", "Call Taker", "Cail Taker", "Cali Taker", "call Taker", "Cajl Taker",
    "‘call Taker:", "Calli Taker:", "Call faker:", "Call Paker:"])
loc_strs = "|".join(["Location/Address", "Locatiion/Address", "Locat ion/Address", "Loctation/Address:", "Lo¢ation/Address:", 
    "Lo¢ation/Addregs","Lecation/Address", "Lecation/Address", "Lacation/Address:", "Lacation/Address", "Loration/Address", 
    "Logation/Address", "Leocation/Address:", "Loeation/Address", "Lodation/Address", "Location"])
narr_strs = "|".join(["Narrative:", "Narrative"])
vehicle_strs = "|".join(["Vehicle:", "Vehicle"])
owner_strs = "|".join(["Owner:", "Owner"])
operator_strs = "|".join(["Operator:", "Operator"])
arreset_strs = "|".join(["Juvenile Arrest", "Arrest:", "Arrest"])
summons_strs = "|".join(["Summons:", "Summons"])
charges_strs = "|".join(["Charges:", "Charges"])
citation_strs = "|".join(["Refer To Citation:", "Refer To Citation"])

unit_strs = "|".join(["Unit:", "Unit"])
arvd_strs = "|".join(['Arvd~', 'Arvd-', "Arv@-", "Arvd+"])
clrd_strs = "|".join(['Clrd-', 'Clrd~', 'Cird-', 'Clird-', 'Clrd+', "Clr@-", "Clré-"])
disp_strs = "|".join(['Disp-', 'Disp~', 'Disp+', "Dis@-"])
enrt_strs = "|".join(['Enrt-', 'Enrt~', 'Enrt+', "Enr@-", "Enrt~-"])

end_of_string_tol = 60

path = os.popen("git rev-parse --show-toplevel").read().strip("\n")+"/data/"

def main(argv):

    year = int(argv[0])
    logging.info("\n Parsing logs for {}".format(year))

    year_str = str(year)[:2]+"-"
    current_date = f"01/01/{str(year)}"

    parsed_pages = []
    all_vehicles = []
    all_people = []
    all_responding = []

    npages = len([fname for fname in os.listdir(os.path.join(path, '{}_text_logs/'.format(year))) if 'page' in fname])
    logging.info("\n Retrieving {} text pages.".format(npages))

    for ipage in range(1, npages + 1):
        with open(os.path.join(path, '{}_text_logs/page_{}.txt'.format(year, ipage)),'r') as infile:
            page_text = infile.read()

        if page_text != "blank page":
            # check for a new date on the page
            new_date = check_for_date(page_text)
            if new_date:
                current_date = new_date

            page_incidents = [log_idx.start() for log_idx in re.finditer(year_str, page_text)] + [-1]


            # now we worry about entries that start from the previous page
            initial_text = page_text[0:page_incidents[0]]
            if len(initial_text) > 0 and len(parsed_pages) > 0:
                #print(initial_text)
                str_entry = parse_entry(initial_text, year_str)
                
                parsed_pages[-1][2:] = replace_none_with_value(parsed_pages[-1][2:], str_entry)
                call_number = parsed_pages[-1][2]
                all_vehicles, all_people = process_vehicles(entry_text, call_number, all_vehicles, all_people)
                all_responding = process_units(entry_text, call_number, all_responding)

            for i_start in range(len(page_incidents)-1):

                entry_text = page_text[page_incidents[i_start]:page_incidents[i_start + 1]]
                
                str_entry = parse_entry(entry_text, year_str)
                
                if str_entry.count(None) < 5:
                    parsed_pages.append([current_date, ipage] + str_entry)
                    call_number = str_entry[0]
                    all_vehicles, all_people = process_vehicles(entry_text, call_number, all_vehicles, all_people)
                    all_responding = process_units(entry_text, call_number, all_responding)

    # done so make the data frame
    parsed_pages = pd.DataFrame(parsed_pages, 
                            columns = ['current_date', 'page_num', 'call_number', 'call_time', 
                                       'original_call_reason_action', 'original_call_taker', "call_address", 
                                       "arvd_time", "clrd_time", "narrative_text", "referenced_citation"])                

    # cleanup call_takers
    parsed_pages['original_call_taker'] = parsed_pages['original_call_taker'].str.replace(":", "").str.strip()

    # standardize the officer names
    parsed_pages = clean_officer_names(parsed_pages)

    # standarize the actions reasons
    parsed_pages = clean_call_actions(parsed_pages)

    # finish and save
    parsed_pages.to_csv('{}parsed_logs_{}.csv'.format(path,year), mode='w', index=False, header=True)



    all_vehicles = pd.DataFrame(all_vehicles, 
                            columns = ['call_number', "vehicles_color", "vehicles_year", "vehicles_model", "vehicles_vin"])

    all_vehicles.to_csv('{}parsed_vehicles_{}.csv'.format(path,year), mode='w', index=False, header=True)

    all_people = pd.DataFrame(all_people, 
                            columns = ['call_number', 'operator/owner', "vehicles_vin", "lastname", 
                            "firstname", "race", "sex", "stree", "city", "state", "zipcode"])                

    all_people.to_csv('{}parsed_people_{}.csv'.format(path,year), mode='w', index=False, header=True)

    all_responding = pd.DataFrame(all_responding, 
                            columns = ['call_number', 'unit', "disp_time", "enrt_time", "arvd_time", "clrd_time"])                

    all_responding.to_csv('{}parsed_responding_units_{}.csv'.format(path,year), mode='w', index=False, header=True)


def check_for_date(page_text):
    current_date = None 

    # check for updated date - we assume only once ever on the page
    date_end = [date_idx.end() for date_idx in re.finditer('For Date: ', page_text)]
    if len(date_end) > 1:
        print("Oh no, multiple days on the same page... this wont work.")
        adgasdgs
    
    # we found only one date so update
    elif len(date_end) == 1:
        current_date = re.search('([^\s]+)', page_text[date_end[0]:])
        if current_date:
            current_date = current_date.group(0).replace('-', "").strip()

    return current_date


def clean_officer_names(parsed_pages):
    with open('{}williamston_known_officers.txt'.format(path), 'r') as infile:
        known_officers = [line.replace("\n", "").strip() for line in infile]

    known_officer_ratio = np.array([ratio(o1,o2) for o1, o2 in itertools.combinations(known_officers, 2)])

    min_officer_ratio = known_officer_ratio.max() + 3

    parsed_pages['call_taker'] = [standardize_officers(oname, known_officers, min_officer_ratio) for oname in parsed_pages['original_call_taker'].values]

    return parsed_pages


def standardize_officers(s, known_officers, min_officer_ratio=100):
    if isinstance(s, str):
        for oname in known_officers:
            if partial_ratio(s, oname) > min_officer_ratio:
                return oname
    return None    

def find_between(entry_text, left_text, right_text):
    left_end = re.search(left_text, entry_text)
    right_start = re.search(right_text, entry_text)
    
    if left_end and right_start:
        return entry_text[left_end.end():right_start.start()].strip()
    else:
        return None

def find_next_word(entry_text, left_text):
    left_end = re.search(left_text, entry_text)
    
    if left_end:
        nextsearch = re.search('([^\s]+)', entry_text[left_end.end():])
        if nextsearch:
            return nextsearch.group(0)
    else:
        return None

def replace_none_with_value(left_list, right_list):
    return [l if not l is None else r for l, r in zip(left_list, right_list)]    



def parse_entry(entry_text, year_str):
    entry_words = [w for w in entry_text.split(' ') if len(w) > 0]
    
    
    if len(entry_words) <2:
        return [None]*6
    else:    
        # call number is always the first word of the entry
        call_number = entry_words[0]

        if re.search(year_str + '(?=[0-9])', call_number):
            # the next 'word' is always the time
            call_time = entry_words[1][:min(4, len(entry_words[1]))]
            for c in ['(', ')', "[", "]", "{", "}"]:
                call_time = call_time.replace(c, "")

            # call reason
            call_reason = find_between(entry_text, call_time, taker_strs)
            if call_reason is None:
                # see if its actually near the end of the string so call taker never appears
                if re.search(call_time, entry_text) and re.search(taker_strs, entry_text) is None:
                    
                    call_reason = entry_text[re.search(call_time, entry_text).end():]


            # call reasonaction is always the string between time and taker
            if re.search(taker_strs, entry_text):
                call_reason = find_between(entry_text, call_time, taker_strs)
            elif re.search(loc_strs, entry_text):
                call_reason = find_between(entry_text, call_time, loc_strs)
            elif re.search(unit_strs, entry_text):
                call_reason = find_between(entry_text, call_time, unit_strs)
            elif re.search(vehicle_strs, entry_text):
                call_reason = find_between(entry_text, call_time, vehicle_strs)
            elif re.search(narr_strs, entry_text):
                call_reason = find_between(entry_text, call_time, narr_strs)
            elif re.search(call_time, entry_text):
                # see if its actually near the end of the string so location doesnt appear
                if len(entry_text) - re.search(call_time, entry_text).end() < end_of_string_tol:
                    call_reason = entry_text[re.search(call_time, entry_text).end():]
                else:
                    call_reason = None
                    print("End of string?", entry_text)
            else:
                call_reason=None
        else:
            call_time = None
            call_reason = None 

        # call taker is always the string between taker and location
        has_taker = re.search(taker_strs, entry_text)
        if has_taker:
            # first try to locate between taker and location
            if re.search(loc_strs, entry_text):
                call_taker = find_between(entry_text, taker_strs, loc_strs)
            elif re.search(unit_strs, entry_text):
                call_taker = find_between(entry_text, taker_strs, unit_strs)
            elif re.search(vehicle_strs, entry_text):
                call_taker = find_between(entry_text, taker_strs, vehicle_strs)
            elif re.search(narr_strs, entry_text):
                call_taker = find_between(entry_text, taker_strs, narr_strs)
            else:
                # see if its actually near the end of the string so location doesnt appear
                if len(entry_text) - re.search(taker_strs, entry_text).end() < end_of_string_tol:
                    call_taker = entry_text[re.search(taker_strs, entry_text).end():]
                else:
                    call_taker = None
                    print("End of string?", len(entry_text) - re.search(taker_strs, entry_text).end(), entry_text)
                    print(re.search(taker_strs, entry_text) )
        else:
            #print(entry_text)
            call_taker = None
        
        #get address
        entry_text_ = entry_text.replace(" ","_").split("__")
        
        loc_series = pd.Series(entry_text_)[pd.Series(entry_text_).str.match(r'Location/Address*')]
        call_address = None
        if len(loc_series) > 0:
            loc_idx = loc_series.index[0]
            if loc_idx != len(entry_text_) -1:
                call_address = entry_text_[loc_idx +1]


        # first times for call
        arvd_time = find_next_word(entry_text, arvd_strs)
        clrd_time = find_next_word(entry_text, clrd_strs)
        if clrd_time and len(clrd_time) < 8:
            print(clrd_time)
            
        narrative_text = re.search(narr_strs, entry_text)
        if narrative_text:
            narrative_text = entry_text[narrative_text.start():]

        # citations
        citation_text = find_next_word(entry_text, citation_strs)

    return [call_number, call_time, call_reason, call_taker, call_address, arvd_time, clrd_time, narrative_text, citation_text]


def process_vehicles(entry_text, call_number, all_vehicles, all_people):

    vehicle_starts = [vloc.start() for vloc in re.finditer(vehicle_strs, entry_text)] + [-1]

    if len(vehicle_starts) > 1:

        for ivs in range(len(vehicle_starts) - 1):
            vehicle_entry = entry_text[vehicle_starts[ivs]:vehicle_starts[ivs+1]]
            #print(ivs, vehicle_entry)
            operator_txt = re.search(owner_strs, vehicle_entry)
            owner_txt = re.search(operator_strs, vehicle_entry)
            vehicle_txt = None 

            # now we have to worry about the ordering of operators / owners and if we have both info
            if operator_txt and owner_txt:
                
                # operator comes first
                if operator_txt.start() < owner_txt.start():
                    vehicle_txt = vehicle_entry[:operator_txt.start()]
                    operator_txt = vehicle_entry[operator_txt.end():owner_txt.start()]
                    owner_txt = vehicle_entry[owner_txt.end():]
                
                # owner comes first
                else:
                    vehicle_txt = vehicle_entry[:owner_txt.start()]
                    owner_txt = vehicle_entry[owner_txt.end():operator_txt.start()]
                    operator_txt = vehicle_entry[operator_txt.end():]
            
            # only operator
            elif operator_txt:
                vehicle_txt = vehicle_entry[:operator_txt.start()]
                operator_txt = vehicle_entry[operator_txt.end():]
            
            # only owner    
            elif owner_txt:
                vehicle_txt = vehicle_entry[:owner_txt.start()]
                owner_txt = vehicle_entry[owner_txt.end():]

            
            if vehicle_txt:
                vinfo = get_vehicle_info(vehicle_txt)
                all_vehicles.append([call_number] + get_vehicle_info(vehicle_txt))
            
            if operator_txt:
                all_people.append([call_number, 'operator', vinfo[3]] + get_person_info(operator_txt))
                
            if owner_txt:
                all_people.append([call_number, 'owner', vinfo[3]] + get_person_info(owner_txt))

    return all_vehicles, all_people

        
def get_vehicle_info(vehicle_txt):
    vehicle_words = [w for w in vehicle_txt.split(' ') if len(w) > 0]
    if len(vehicle_words) > 4:
        vcolor = vehicle_words[1]
        vyear = vehicle_words[2]
        
        if 'Reg:' in vehicle_words:
            regidx = vehicle_words.index('Reg:')
            vmodel = " ".join(vehicle_words[3:regidx])
        elif 'Reg' in vehicle_words:
            regidx = vehicle_words.index('Reg')
            vmodel = " ".join(vehicle_words[3:regidx])
        else:
            vmodel = None
            
        
        vinidx = len(vehicle_words)
        if 'VIN:' in vehicle_words: 
            vinidx = vehicle_words.index('VIN:')
        elif 'VIN' in vehicle_words:
            vinidx = vehicle_words.index('VIN')
        
        if vinidx < len(vehicle_words)-1:
            vin = vehicle_words[vinidx+1]
        else:
            vin = None

        return [vcolor, vyear, vmodel, vin]
    else:
        return [None]*4
        
    

def get_person_info(person_txt):
    lastname_idx = re.search(',', person_txt)
    if lastname_idx:
        lastname = person_txt[:lastname_idx.start()].strip()
    else:
        lastname = None
        
    firstname_idx = re.search('@', person_txt)
    if firstname_idx and lastname_idx:
        firstname = person_txt[lastname_idx.end():firstname_idx.start()].strip()
    else:
        firstname = None
    
    address = usaddress.parse(person_txt)
    st = " ".join([e[0] for e in address if e[1] in ['AddressNumber', 'StreetName', 'StreetNamePostType', 'OccupancyType', 'OccupancyIdentifier']])
    city = " ".join([e[0] for e in address if e[1] in ['PlaceName']])
    state = " ".join([e[0] for e in address if e[1] in ['StateName']])
    zipcode = " ".join([e[0] for e in address if e[1] in ['ZipCode']])
    
    race = find_next_word(person_txt, 'Race:')
    sex = find_next_word(person_txt, 'Sex:')
        
    return [lastname, firstname, race, sex, st, city, state, zipcode]

def standardize_partial(s, known_list, min_ratio):
        if isinstance(s, str):
            pmatch = np.array([partial_ratio(s, oname) for oname in known_list])
            argmatch = np.argmax(pmatch)
            if pmatch[argmatch] > min_ratio:
                return known_list[argmatch]
        return None 
    
def clean_call_actions(parsed_pages):

    with open('{}williamston_known_actions.txt'.format(path), 'r') as infile:
        known_actions = [line.replace("\n", "").strip() for line in infile]

    known_actions_ratio = np.array([ratio(a1,a2) for a1, a2 in itertools.combinations(known_actions, 2)])
    min_actions_ratio = known_actions_ratio.max()

    with open('{}williamston_known_reasons.txt'.format(path), 'r') as infile:
        known_reasons = [line.replace("\n", "").strip() for line in infile]

    known_reasons_ratio = np.array([ratio(a1,a2) for a1, a2 in itertools.combinations(known_reasons, 2)])
    min_reasons_ratio = known_reasons_ratio.max()

    parsed_pages['call_reasons'] = [standardize_partial(s, known_reasons, min_reasons_ratio) for s in parsed_pages['original_call_reason_action'].values]
    parsed_pages['call_actions'] = [standardize_partial(s, known_actions, min_actions_ratio) for s in parsed_pages['original_call_reason_action'].values]


    return parsed_pages

def process_units(entry_text, call_number, all_units):

    unit_starts = [uloc.start() for uloc in re.finditer(unit_strs, entry_text)] + [-1]
    if len(unit_starts) > 1:
        for iunits in range(len(unit_starts) - 1):
            
            unit_text = entry_text[unit_starts[iunits]:unit_starts[iunits+1]]
            
            unitnum = find_next_word(unit_text, unit_strs)
            disp_time = find_next_word(unit_text, disp_strs)
            enrt_time = find_next_word(unit_text, enrt_strs)
            arvd_time = find_next_word(unit_text, arvd_strs)
            clrd_time = find_next_word(unit_text, clrd_strs)
            
            all_units.append([call_number, unitnum, disp_time, enrt_time, arvd_time, clrd_time])
            
            
    return all_units

def process_arrest_summons(entry_text, call_number, all_people):

    arrest_starts = [aloc.start() for aloc in re.finditer(arrest_strs, entry_text)] + [-1]
    if len(unit_starts) > 1:
        for iunits in range(len(unit_starts) - 1):
            
            unit_text = entry_text[unit_starts[iunits]:unit_starts[iunits+1]]
            
            unitnum = find_next_word(unit_text, unit_strs)
            disp_time = find_next_word(unit_text, disp_strs)
            enrt_time = find_next_word(unit_text, enrt_strs)
            arvd_time = find_next_word(unit_text, arvd_strs)
            clrd_time = find_next_word(unit_text, clrd_strs)
            
            all_units.append([call_number, unitnum, disp_time, enrt_time, arvd_time, clrd_time])
            
            
    return all_units


if __name__ == "__main__":
    main(sys.argv[1:])
