from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
import re

from server.elasticsearch import utils
from server.models.decklist import Decklist

# List of fields to return for deckbuilding
deck_fields = ['arena_id', 'cmc', 'collector_number', 'color_identity', 'colors', 'id', 'image_uris', 'mana_cost', 'name', 'rarity', 'set', 'set_name', 'type_line']

# This is a trivial search by 
def search_by_name(name):
	es = utils.get_client()
	q = Q("match", name=name)
	s = Search(using=es, index='cards').query(q)
	response = s.execute()
	return response


# TODO: do an actual proper search here after it's done
def do_search(params):
	return search_by_name(params)

def find_card_from_arena(cardname):
	# The card format is NUM <cardname> (<setname>) collector's number
	# The pattern looks like ^\d+ .* \(.*\) \d+
	pattern = '(\d+) (.*) \((.*)\) (\d+)'
	match = re.search(pattern, cardname)
	count = int(match.group(1))
	name = match.group(2)
	setname = match.group(3).lower()
	col_num = str(match.group(4))
	# Dumb fix for dominaria
	if setname == 'dar':
		setname = 'dom'
	es = utils.get_client()
	q = Q('bool', filter=[Q('match', name=name), Q('match', collector_number=col_num), Q('match', set=setname), Q('match', lang='en')])
	s = Search(using=es, index='cards').query(q).source(fields=deck_fields)
	response = s.execute()
	if response.success() and response.hits.total.value > 0:
		card_json = response.hits[0].to_dict()
		card_json['count'] = count
	else:
		card_json = {}
		card_json['error'] = 'not_found'
		card_json['name'] = name
		card_json['setname'] = setname
		card_json['col_num'] = col_num 
	return card_json

def find_from_arena_import(decklist):
	cardlist = decklist.splitlines()
	found_cards = []
	missing_cards = []
	sideboarding = False
	deck = Decklist()
	deck_json = []
	# Important for arena. There is a newline, and everything after goes into the sideboard
	for card in cardlist:
		if not card:
			sideboarding = True
			#found_cards.append('Sideboard')
		else:
			# actually find the card
			card_json = find_card_from_arena(card)
			if 'error' not in card_json:
				deck.add_card(card_json, sideboarding)
				deck_json.append(card_json)
			else:
				# log an error
				missing_cards.append(card_json)
	return deck.to_json()