from configparser import ConfigParser
from elasticsearch import Elasticsearch
from server.config import Config

es = None

def init_client():
	global es
	if es is None:
		conf = Config()
		# TODO: Read config props here
		es_url = conf.es_url
		es = Elasticsearch([es_url])

def get_client():
	global es
	if es is None:
		init_client()
	return es