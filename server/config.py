
class Config:
	es_url = 'http://localhost:9200'
	environment = 'dev'

	cards_index = 'cards'
	card_object = 'card'
	decks_index = 'decks'
	deck_object = 'deck'

	# TODO: read the secret key from a file.
	SECRET_KEY = 'change_me'