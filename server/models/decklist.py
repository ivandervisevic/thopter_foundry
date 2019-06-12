import json

class Decklist:

	def __init__(self):
		self.mainboard = {}
		self.mainboard_cards = 0
		self.sideboard = {}
		self.sideboard_cards = 0
		self.name = ''
		self.id = ''

	def add_card(self, cardinfo, sideboard):
		# check if card is already in the cards
		if sideboard:
			if cardinfo['name'] in self.sideboard:
				# TODO: decide if we're sending total counts or adding a single card when we do this
				self.sideboard_cards = self.sideboard_cards + cardinfo['count'] - self.sideboard[cardinfo['name']]['count']
				self.sideboard[cardinfo['name']]['count'] = cardinfo['count']
			else:
				self.sideboard[cardinfo['name']] = cardinfo
				self.sideboard_cards += cardinfo['count']
		else:
			if cardinfo['name'] in self.mainboard:
				# TODO: decide if we're sending total counts or adding a single card when we do this
				self.mainboard_cards = self.mainboard_cards + cardinfo['count'] - self.mainboard[cardinfo['name']]['count']
				self.mainboard[cardinfo['name']]['count'] = cardinfo['count']
			else:
				self.mainboard[cardinfo['name']] = cardinfo
				self.mainboard_cards += cardinfo['count']

	def to_json(self):
		output = {}
		output['mainboard'] = self.mainboard
		output['mainboard_cards'] = self.mainboard_cards
		output['sideboard'] = self.sideboard
		output['sideboard_cards'] = self.sideboard_cards
		output['name'] = self.name
		output['id'] = self.id
		return output
		# TODO: what other things do we need? Author, last edited, edit history maybe?

	def from_json(self, json_input):
		return None