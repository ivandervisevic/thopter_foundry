from configparser import ConfigParser
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from server.elasticsearch import utils

def random_card():
	es = utils.get_client()
	s = Search(using=es, index='cards').query("match_all")
	response = s.execute()
	return response[0].to_dict()