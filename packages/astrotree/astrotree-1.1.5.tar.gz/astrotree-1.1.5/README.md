# Welcome to astrotree!

A lightweight, purely python package to handle reference trees.
This project evolved because of a personal urge to organize literature from my day-to-day.
Note that this is not a reference manager: if you are looking for a python-based reference manager, look no further than [Papis](https://pypi.org/project/papis/)!

This project helps you connect literature entries: given an article, you can choose to build a tree of other articles that connect to it. These are articles referenced in the article of interest (references), or works that cited it (citations). Trees can be built to arbitrary depths, limited only by resources available to python and records on the internet, at any level of the tree.

The project presently uses the NASA-ADS API (see [ADS Docs](https://ui.adsabs.harvard.edu/help/api/api-docs.html#servers)) to launch queries and is suited to my use case; any efforts to contribute and extend it to other APIs are welcome!

# Installation

Install directly through pip:

    pip install astrotree

# Prerequisite

Before you can start to use this application, you need to set an environment variable `ADSTOKEN`, which needs to point to your ADS API token.
Follow the instructions [here](https://ui.adsabs.harvard.edu/help/api/) to obtain your ADS API token.
You are subject to the [ADS API Terms of Service](https://ui.adsabs.harvard.edu/help/terms/) through your use of this application.

# Usage
The application is CLI-based and has two modes: you may choose to build either a reference tree or a citation tree.
To build a reference tree, use:

    astrotree -id <ADS id> --ref 

To build a citation tree, use:

    astrotree -id <ADS id> --cite


In either case the output is a list of ADS IDs and the respective article titles, in a tree format. The tool offers you the opportunity to ask to build a tree for any of the listed IDs, restricted to the same mode you started with.

Upon exit (press n when the application asks if you wish to continue), the tree is dumped to a text file containing the tree in the local directory, for future use.



 


