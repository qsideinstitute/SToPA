# STOPA Research Lab Repository

This is the official repository for the Small TOwn Police Accountability (STOPA) Research Lab. This research lab is co-organized by: 
* [Manuchehr Aminian](https://www.cpp.edu/~maminian/)
* [Anna Haensch](https://annahaensch.com)
* [Ariana Mendible](https://www.arianamendible.com/)

and the [Institute for the Quantitative Study of Inclusion, Diversity, and Equity (QSIDE)](https://qsideinstitute.org/).

## How to OCR the Williamstown Policing Data

The 2019 and 2020 police logs were handed over as printed pdf which were scanned and saved as `Logs2019.pdf` and `Logs2020.pdf`.  These can be found in `data/primary_datasets/`.  During the [2021 QSIDE Datathon4Justice](https://qsideinstitute.org/events/datathon4justice/), we constructed an OCR pipeline to convert these documents to a readable text format. You can do this too, from the `STOPA` directory in a terminal, run

```
python code/pdf_to_text_script.py 2019
```

or replace 2019 with whichever year you're interested in.  This will take awhile to run, so be patient.

## How to Parse the Text Files


## Contact

If you'd like to be added to this repository, please email annahaensch@gmail.com with your Github username and the reason you'd like to be added. 