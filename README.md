# thopter_foundry

A quick and dirty start towards a visual deckbuilder for mtg

## Setup:
 * python 3
 * Install elasticsearch and run on localhost.
 * set up a virtual environment, activate and pip install -r requirements.txt
 * (local dev) download the bulk data file from scryfall (https://archive.scryfall.com/json/scryfall-default-cards.json) and keep it somewhere
 * update scripts/import_config.ini with the relevant paths and ports
 * run scripts/import_data.py to populate the es. this will take a couple of minutes.

## Flask setup
 * simplest way to get constant updates is to set up a small script that will define env variables:  
export FLASK_APP=<path_to_repo>/server  
export FLASK_ENV=development  
flask run  