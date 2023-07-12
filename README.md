# The SToPA Research Lab

This is the official repository for the Small Town Police Accountability (SToPA) Research Lab. This research lab is co-organized by: 
* [Manuchehr Aminian](https://www.cpp.edu/~maminian/)
* [Anna Haensch](https://annahaensch.com)
* [Ariana Mendible](https://www.arianamendible.com/)

and the [Institute for the Quantitative Study of Inclusion, Diversity, and Equity (QSIDE)](https://qsideinstitute.org/).

# Getting Started with the SToPA library


## Forking the Repository

To get a copy of the SToPA repository you'll need to fork this repository. You can do this from the `Fork` button on the upper right of the repository landing page.  Once you've forked, you will see that the repository name on the upper left is now `<your_username>/SToPA`.   You can now clone the respository to your local machine with 

```
$ git clone https://github.com/<your_username>/SToPA.git 
```
for example if your username is annahaensch, it would be 

```
$ git clone https://github.com/annahaensch/SToPA.git 
```
From your terminal you can change into the SToPA directory with 

```
$ cd SToPA
```

## Setting Up your Environment

Before you get started, you'll need to create a new environment using `conda` (in case you need it, [installation guide here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)). If you use `conda` you can 
create a new environment (we'll call it `stopa_env`) with

```
$ conda create --name stopa_env
```

and activate your new environment, with

```
$ conda activate stopa_env
```

Now you can install the necessary requirements for accessing the base functionality of the SToPA library using the following command.

```
$ conda install pip
$ pip install -U -r requirements.txt
```

## Installing the parsing engine

If you wish to use the Optical Character Recognition (OCR) and parsing tools to build the csv files, you'll need to carry out the following additional installation steps.

#### For Mac Users
If you are using a mac and you plan to run the OCR engine, you will also need to make sure that `tesseract` is added to your path my installing it with homebrew.
```
$ brew install tesseract
```

#### For Everyone
The following steps should install all remaining necessary requirements and dependencies.

```
$ conda install -c conda-forge poppler
$ pip install -U -r requirements_ocr.txt
```

# Using the SToPA Library

## How to OCR the Williamstown Policing Data

The 2019 and 2020 police logs were originally received as printed pdf pages which were scanned and saved as `Logs2019.pdf` and `Logs2020.pdf`.  These can be found in `data/primary_datasets/`.  During the [2021 QSIDE Datathon4Justice](https://qsideinstitute.org/events/datathon4justice/), we began the preliminary construction of an OCR pipeline to convert these documents to a readable text format. You can do this too, from the `STOPA` directory in a terminal, run

```
$ cd scripts 
$ python pdf_to_parquet.py 2019
```

or replace 2019 with whichever year you're interested in.  This will take awhile to run, so be patient.  Pages xxxx through yyyy of the pdf will be printed as [parquet](https://www.databricks.com/glossary/what-is-parquet) files to 

```
SToPA/data/2019_parquet_logs/pages_xxxx_yyyy.pq
```

and the analogous for 2020.  _If you want to skip this step, you can find the pre-OCR'd [parquet files in google drive here](https://drive.google.com/drive/folders/1hX4BCCQmcWqxmLGIuPRC2x-6CxXd9adB?usp=sharing)._  

## How to Parse the Text Files

After performing the OCR steop, 2019 and 2020 police log parquet files can be parsed as a nice easy-to-read csv.  To parse the logs for any year, from the `STOPA` directory in your terminal, run

```
>cd scripts
>python parquet_to_csv.py 2019
```
or replace 2019 with whichever year you're interested in.  If this raises errors it might be the case that you are missing some dependencies, these can be installed using pip (or whatever package management software you prefer).  This will take a couple of minutes to run.  The output files will be printed as csv files to 

```
SToPA/data/<today's date>_parsed_2019.csv
```
or the analogous for 2020. _If you want to skip this step, you can fine the pre-parsed [csv files in google drive here](https://drive.google.com/drive/folders/1hX4BCCQmcWqxmLGIuPRC2x-6CxXd9adB?usp=sharing)._

## Getting Started with the Data

Once the data is parsed, you can interact with it in a Jupyter notebook.  If you installed all of the necessary dependencies when setting up your environment, you should be able to launch a Jupyter server from the top level directory of this repository with 

```
$ jupyter notebook
```

This will load a Jupyter environment in a web browser.  If you navigate to `notebooks`, you will find `Getting_Started_with_the_Data.ipynb`.  Just open that, and off you go! 

## Mapping Tools

If you're interested in making maps, then navigate to `analysis/interactive_zoomable_map/` and start there with the associated README.

# Contributing to SToPA

If you have code in your fork which you'd like to add you can do this using the `contribute` in the Github interface.  Alternatively, you can add the `qsideinstitute` repository as your `upstream` remote with 
```
git remote add upstream https://github.com/qsideinstitute/SToPA.git
```
and if you run `git remote -v` you shoudl see something like

```
origin	https://github.com/<username>/SToPA.git (fetch)
origin	https://github.com/<username>/SToPA.git (push)
upstream	https://github.com/qsideinstitute/SToPA.git (fetch)
upstream	https://github.com/qsideinstitute/SToPA.git (push)
```
Now you can push your changes, open a pull request, and get your cool new work merged into the SToPA project.  

## Contact

If you'd like to be added to this repository, please email annahaensch@gmail.com with your Github username and the reason you'd like to be added. 
