import requests
import datetime
from urllib.parse import urlencode
import base64
import json

client_id = "b75dfd2aa89f4ed985eb2f20638c0633"
client_secret = "6f994b2726774f8d93146681bb7a7fcd"

class Spotify_API(object):
	access_token = None
	access_token_expires = datetime.datetime.now()
	access_token_did_expire = True
	client_id = None
	client_secret = None
	token_url = 'https://accounts.spotify.com/api/token'
	base_url = f'https://api.spotify.com/v1/artists/'
	
	def __init__(self, client_id, client_secret, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.client_id = client_id
		self.client_secret=client_secret
		
	def get_client_credentials(self):
		client_id = self.client_id
		client_secret = self.client_secret
		if client_secret == None or client_id == None:
			raise Exception("You must set client_id and client_secret.")
		client_creds = f'{client_id}:{client_secret}'
		client_creds_b64 = base64.b64encode(client_creds.encode())        
		return client_creds_b64.decode()
		
	def get_token_headers(self):
		client_creds_b64 = self.get_client_credentials()
		return {
			'Authorization':f'Basic {client_creds_b64}'
		}
	
	def get_token_data(self):
		return {
			'grant_type':'client_credentials'
		}
	
	def perform_auth(self):
		token_url = self.token_url
		token_data = self.get_token_data()
		token_headers = self.get_token_headers()
		r = requests.post(token_url, data=token_data, headers=token_headers)
		if r.status_code not in range(200, 299):
			raise Exception("Could not authenticate client.")
		data = r.json()
		now = datetime.datetime.now()
		access_token = data['access_token']
		expires_in = data['expires_in']
		expires = now + datetime.timedelta(seconds=expires_in)
		self.access_token = access_token
		self.access_token_expires = expires
		access_token_did_expire = expires < now
		return True
	
	def get_access_token(self):
		token = self.access_token
		expires = self.access_token_expires
		now = datetime.datetime.now()
		if expires < now:
			self.perform_auth()
			return self.get_access_token()
		elif token == None:
			self.perform_auth()
			return self.get_access_token()
		return token
	
	def get_resource_header(self):
		access_token = self.get_access_token()
		headers = {
			'Authorization':f'Bearer {access_token}'
		}
		return headers

	def get_artist_albums(self, searched_artist_id):
		base_url = self.base_url
		headers = self.get_resource_header()
		r = requests.get(base_url + searched_artist_id + '/albums', headers=headers, params={'include_groups': 'album'})
		album_data = r.json() # this is a dict.
		# print(json.dumps(album_data, indent=4)) # prints albums info
		searched_albums = []
		for album in album_data['items']:
			if album['name'] not in searched_albums:
				searched_albums.append(album['name'])  
		# i think the move here now is to instead put the album in a dict where key is the album name and the value is the album.lower(),
		# then i would go through the keys and if the count is greater than 1, remove the [-1] album (to get rid of the older album),
		# once that is all gone through, i would return just the keys of the dict. 
		return list(dict.fromkeys(searched_albums))[0:10] # this will return the artist's 10 most recent albums in a list

	def get_artists_top_tracks(self, searched_artist_id):
		base_url = self.base_url
		headers = self.get_resource_header()
		r = requests.get(base_url + searched_artist_id + '/top-tracks', headers=headers, params={'include_groups': 'top-track', 'country':'US', 'limit': 11})
		top_tracks = r.json()
		#print(json.dumps(top_tracks, indent=4))
		if len(top_tracks['tracks']) < 10:
			return [top_tracks['tracks'][x]['name'] for x in range(len(top_tracks['tracks']))]
		else:
			return [top_tracks['tracks'][x]['name'] for x in range(10)] # returns artist's top 10 tracks in a list

	def base_search(self, query_params):
		headers = self.get_resource_header()
		endpoint = 'https://api.spotify.com/v1/search'
		lookup_url = f'{endpoint}?{query_params}'
		r = requests.get(lookup_url, headers=headers)
		if r.status_code not in range(200,299):
			return {}
		return r.json()
		
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

def recent_albums_head():
	if len(spotify.get_artist_albums(searched_artist_id)) == 0:
		return f'{user_search.title()} has no albums with Spotify.'
	elif len(spotify.get_artist_albums(searched_artist_id)) == 1:
		return f"{user_search.title()}'s Album:"
	elif len(spotify.get_artist_albums(searched_artist_id)) < 10:
		return f"{user_search.title()}'s Albums:"
	else:
		return f"{user_search.title()}'s 10 Most Recent Albums:"


spotify = Spotify_API(client_id, client_secret)

user_search = input('Enter an artist here: ')

search_results = spotify.search(user_search, search_type='artist')
searched_artist_id = search_results['artists']['items'][0]['id'] # gets artist's ID
searched_artist_url = search_results['artists']['items'][0]['external_urls']['spotify']  # gets artist's URL 

print('\n')

print(recent_albums_head() + '\n')

for album in spotify.get_artist_albums(searched_artist_id):
	print(album)

print(f"\n{user_search.title()}'s Top Tracks on Spotify: \n")

if len(spotify.get_artists_top_tracks(searched_artist_id)) < 10:
  for x in range(1, (len(spotify.get_artists_top_tracks(searched_artist_id))+1)):
	  print(str(x) + ' - ' + (spotify.get_artists_top_tracks(searched_artist_id)[x-1]))
else: 
  for x in range(1,11):
	  print(str(x) + ' - ' + (spotify.get_artists_top_tracks(searched_artist_id)[x-1]))

print(f"\nVisit {user_search.title()}'s Spotify page via: {searched_artist_url}\n")