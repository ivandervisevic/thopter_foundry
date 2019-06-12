from configparser import ConfigParser
import datetime
from elasticsearch import Elasticsearch
import json
from pathlib import Path
import requests

def main():
	# TODO: add options to create a new index and alias from scratch instead of updating cards one by one.
	update = False

	parser = ConfigParser()
	parser.read('../import_config.ini')
	es_url = parser.get('SETTINGS', 'url')
	# TODO: make sure to change the import_config.ini value to where your file is actually kept. Absolute path should work best

	card_file = parser.get('SETTINGS', 'local_cards')
	cards_url = parser.get('SETTINGS', 'cards_url')
	env = parser.get('SETTINGS', 'environment')

	# TODO: add error handling and alerting here. Is the elasticsearch even available?
	es = Elasticsearch([es_url], timeout=3600)
	
	cards = None
	# Get the data from scryfall (ALWAYS use locally downloaded file for dev)
	if env == 'production':
		#Download, load into the file
		print('NO BAD NO')
		data = requests.get(cards_url)
		cards = json.loads(data.text)
		# do some extra logging and error handling here?
	else:
		# Making sure this works between OSes
		localdata = Path(card_file)
		if localdata.is_file():
			cards = json.loads(localdata.read_text(encoding='utf-8'))
		else:
			print('error, did not find file: ', card_file)
			sys.exit()
	if cards is None:
		print('something went wrong, not updating')
		sys.exit()

	# Now we have the list of cards, we have a connection to ES, let's index or update all of them
	cards_index = parser.get('ES', 'cards_index')
	alias_exists = es.indices.exists_alias(name=cards_index)
	if alias_exists and update: 
		print(cards_index, 'index already exists, updating cards, card by card')
		update_cards(es, cards, cards_index)
	else:
		index_name = cards_index + '_' + datetime.date.today().isoformat()
		print(cards_index, 'alias not found or creation of new one requested. Adding index', index_name, 'and aliasing it')
		# TODO: create a new alias. This won't work if we run it more than once a day. figure out a better way.
		if es.indices.exists(index=index_name):
			print('Already created that index today. Fix this!')
			# Maybe don't do this in production
			sys.exit()
		if alias_exists:
			es.indices.delete_alias(index='_all', name=cards_index)
		es.indices.create(index=index_name)
		es.indices.put_alias(index=index_name, name=cards_index)
		update_cards(es, cards, cards_index)

def update_cards(es, cards, index):
	# TODO: make better. for now, just dump... everything? Use the id as _id
	# TODO: decide how each field should or should not be analyzed and maybe make a hardcoded index mapping?
	count = 0
	for card in cards:
		es_id = card['id']
		es.index(index=index, body=card, id=es_id, timeout='1h')
		count += 1
		if count % 1000 == 0:
			print('updated', count, 'objects')


if __name__ == "__main__":
    main()