## Keyword Extraction and Analysis

`keyword_shell.py` is a utility for finding police logs that relate to an entered keyword.

This analysis utility is dependent on the parsed log files.

To use this utility, run `python keyword_shell.py` from the command line (but see Todo below). After a short while (about 30 seconds on my machine), the parsed logs will be loaded into a set of dictionaries that allow efficient querying by keyword. Here's an example:

```
$ keyword "north adams"
Keyword or Keyphrase: north adams
[2, 421, 450, 872, 1702, 1892, 2036, 2108, 2165, 2483, 2734, 2773, 2981, 3418, 3724, 3935, 4354, 4803, 5093, 5959, 6175, 6176, 6642, 6929, 7030, 7268, 7505, 7596, 7810, 8439, 8797, 9285, 9399, 10195, 10450, 10789, 10922, 11395, 11892, 12199, 12319, 12466, 12486, 12556, 12561, 12721, 12960, 13120, 13301, 13313, 13362, 13634, 13711, 13731, 13774, 14043, 14123, 14157, 14252, 14759, 15077, 15144, 15237, 15295, 15646, 15779, 15865, 15900, 15905, 15967, 16040, 16144, 16291, 16294, 16313, 16736, 16737, 16759, 17179, 17315, 17398]
$ log 97
---------- Log #97 ----------
page_num                                                                      22
call_number                                                               19-148
call_time                                                                   1043
original_call_reason_action    Phone - ASSIST OTHER AGENCY - POLICE  UNABLE T...
original_call_taker                                     PATROL DAVID JENNINGS, D
call_address                                        SIMONDS_RD_+_SAND_SPRINGS_RD
arvd_time                                                               10:51:54
clrd_time                                                               11:24:21
narrative_text                 Narrative:  Reports a silver chevy pick up wit...
referenced_citation                                                          NaN
call_taker                                              PATROL DAVID JENNINGS, D
call_reasons                                Phone - ASSIST OTHER AGENCY - POLICE
call_actions                                                    UNABLE TO LOCATE
keywords                       ['silver chevy pick', 'ct  plate c173880', 'br...
Name: 97, dtype: object
--------------------
Narrative for this log:
Narrative:  Reports a silver chevy pick up with a brake light out cT  plate C173880, unknown direction of travel. Believes the  parties in the vehicle are from North Adams. Visible of no  less than 4 blocks of heroin in the headliner of the vehicle  when looking through the windshield.
```

The keywords are generated from the parsed log files by `parse_keywords.py`. You can reparse for keywords from the log files by `python parse_keywords.py`.

Currently, the shell shows the integer keys associated with the logs that are associated with the entered keyword (see Todo below).

Type `exit` to exit the shell.

### Notes
- See Requirements.txt for requirements (you can use pip to install with `pip install -r Requirements.txt`, which recursively installs all requirements - consider using a virtual environment!).
- `stop.txt` is a list of stopwords for RAKE, the keyword extraction algorithm.

### Todo List

End Use/Features:

Structures and Algorithms/Code Maintenance:
- Improve automatic keyword extraction (this is the mathy/computer sciencey part of the project), including preprocessing. Currently using RAKE

Unrequested Features (Someday List):
- Implement searching by other fields and enabling printing of entire specific fields for an entry.
- Implement fuzzy matching for keyword search (maybe even tab for suggested completions?)
- Enter a keyword and list top logs by relevance score of that keyword, iterating through each log and finding a relevance score for that word/log combination.