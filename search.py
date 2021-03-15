from client_id_and_secret import *
import requests
from urllib.parse import urlencode
import json

class Query_Search(object):

	base_url = f'https://api.spotify.com/v1/artists/'

	def search(self, query=None, operator=None, operator_query=None, search_type='artist'):
		if query == None:
			raise Exception("A query is required.")
		if isinstance(query, dict):
			query = ' '.join([f'{k}:{v}' for k,v in query.items()])
		if operator != None and operator_query != None:
			if operator.lower() == 'or' or operator.lower() == 'not':
				operator = operator.upper()
				if isinstance(operator_query, str):
					query = f'{query} {operator} {operator_query}'
		query_params = urlencode({'q':query, 'type':search_type.lower()})
		return self.base_search(query_params)

	def base_search(self, query_params):
		headers = self.get_resource_header() #if we split this into another class, we need to change self
		endpoint = 'https://api.spotify.com/v1/search'
		lookup_url = f'{endpoint}?{query_params}'
		r = requests.get(lookup_url, headers=headers)
		if r.status_code not in range(200,299):
			return {}
		return r.json()

	def get_artist_albums(self, artist_id):
		base_url = self.base_url
		headers = self.get_resource_header()
		r = requests.get(base_url + artist_id + '/albums', headers=headers, params={'include_groups': 'album'})
		album_data = r.json()
		searched_albums = []
		for album in album_data['items']:
			if album['name'].lower() not in searched_albums:
				searched_albums.append(album['name'].lower()) 
		top_albums = [' '.join([word.capitalize() for word in album.split(' ')]) for album in searched_albums] 
		return top_albums[0:10]

	def get_artists_top_tracks(self, artist_id):
		base_url = self.base_url
		headers = self.get_resource_header()
		r = requests.get(base_url + artist_id + '/top-tracks', headers=headers, params={'include_groups': 'top-track', 'country':'US', 'limit': 11})
		top_tracks = r.json()
		if len(top_tracks['tracks']) < 10:
			return [top_tracks['tracks'][x]['name'] for x in range(len(top_tracks['tracks']))]
		else:
			return [top_tracks['tracks'][x]['name'] for x in range(10)] # returns artist's top 10 tracks in a list