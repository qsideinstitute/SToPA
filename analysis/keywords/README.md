## Keyword Extraction and Analysis

`keyword_shell.py` is a utility for finding police logs that relate to an entered keyword.

This analysis utility is dependent on the parsed log files.

To use this utility, run `python keyword_shell.py` from the command line (but see Todo below). After a short while (about 30 seconds on my machine), the parsed logs will be loaded into a set of dictionaries that allow efficient querying by keyword. Here's an example:

```
$ keyword "north adams"
Keyword or Keyphrase: north adams
[2, 421, 450, 872, 1702, 1892, 2036, 2108, 2165, 2483, 2734, 2773, 2981, 3418, 3724, 3935, 4354, 4803, 5093, 5959, 6175, 6176, 6642, 6929, 7030, 7268, 7505, 7596, 7810, 8439, 8797, 9285, 9399, 10195, 10450, 10789, 10922, 11395, 11892, 12199, 12319, 12466, 12486, 12556, 12561, 12721, 12960, 13120, 13301, 13313, 13362, 13634, 13711, 13731, 13774, 14043, 14123, 14157, 14252, 14759, 15077, 15144, 15237, 15295, 15646, 15779, 15865, 15900, 15905, 15967, 16040, 16144, 16291, 16294, 16313, 16736, 16737, 16759, 17179, 17315, 17398]
```

Currently, the shell shows the integer keys associated with the logs that are associated with the entered keyword (see Todo below).

Type `exit` to exit the shell.

### Notes
- Paths may only work on Windows.
- See Requirements.txt for requirements (install with pip e.g.).
- `stop.txt` is a list of stopwords for RAKE, the keyword extraction algorithm.

### Todo List

End Use/Features:
- Implement searching by other fields (and show keywords, see below)
- Show keywords by entry (e.g. enter "2019-04265" and get the fields and the keywords)
- Consider scalability - what data structures do we need for about a million entries? Does a relational database make sense or is this shell ok for our purposes?
- Implement fuzzy matching for keyword search (maybe even tab for suggested completions?)
- Provide better feedback about Exceptions in shell


Structures and Algorithms/Code Maintenance:
- Actually `get` the entry, not just its index (see data structures bullet above)
- Improve automatic keyword extraction (this is the mathy/computer sciencey part of the project), including preprocessing. Currently using RAKE
- Generate text files in a separate module, load the text files to dicts in this module (loading currently takes about 30 seconds for our dataset of roughly 17000 entries)
- Choose the right data structures - clean up the dictionaries for time and space complexity
- IMPROVE HASHING by using a data type for the year-log number data as key