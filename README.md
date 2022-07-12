# SToPA Research Lab Repository

This is the official repository for the Small Town Police Accountability (SToPA) Research Lab. This research lab is co-organized by: 
* [Manuchehr Aminian](https://www.cpp.edu/~maminian/)
* [Anna Haensch](https://annahaensch.com)
* [Ariana Mendible](https://www.arianamendible.com/)

and the [Institute for the Quantitative Study of Inclusion, Diversity, and Equity (QSIDE)](https://qsideinstitute.org/).

# Getting Started with the SToPA library

## Setting Up your Environment

Before you get started, you'll need to create a new environment using `conda` (in case you need it, [installation guide here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)). If you use `conda` you can 
create a new environment (we'll call it `stopa_env`) with

```
conda create --name stopa_env
```

and activate your new environment, with

```
conda activate stopa_env
```

Now you can install the necessary requirements for accessing the base functionality of the SToPA library using the following command.

```
conda install pip
pip install -U -r requirements.txt
```

## Installing the OCR engine

If you wish to use the Optical Character Recognition (OCR) tool to parse the original pdf files, you'll need to carry out the following additional installation steps.

#### For Mac Users
If you are using a mac and you plan to run the OCR engine, you will also need to make sure that `tesseract` is added to your path my installing it with homebrew.
```
brew install tesseract
```

#### For Everyone
The following steps should install all remaining necessary requirements and dependencies.

```
conda install -c conda-forge poppler
pip install -U -r requirements_ocr.txt
```

# Using the SToPA Library

## How to OCR the Williamstown Policing Data

The 2019 and 2020 police logs were handed over as printed pdf which were scanned and saved as `Logs2019.pdf` and `Logs2020.pdf`.  These can be found in `data/primary_datasets/`.  During the [2021 QSIDE Datathon4Justice](https://qsideinstitute.org/events/datathon4justice/), we constructed an OCR pipeline to convert these documents to a readable text format. You can do this too, from the `STOPA` directory in a terminal, run

```
>cd code 
>python pdf_to_text_script.py 2019
```

or replace 2019 with whichever year you're interested in.  This will take awhile to run, so be patient.

## How to Parse the Text Files

After OCR the 2019 and 2020 police logs can be parsed using a script written by [Alexander Gates](https://github.com/ajgates42) (updated slightly for this repository).  To parse the logs for any year, from the `STOPA` directory in your terminal, run

```
>cd code
>python parse_text_logs_script.py 2019
```
or replace 2019 with whichever year you're interested in.  If this raises errors it might be the case that you are missing some dependencies, these can be installed using pip (or whatever package management software you prefer).

## Contact

If you'd like to be added to this repository, please email annahaensch@gmail.com with your Github username and the reason you'd like to be added. 
