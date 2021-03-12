import requests
import datetime
from urllib.parse import urlencode
import base64
import json

client_id = "b75dfd2aa89f4ed985eb2f20638c0633"
client_secret = "6f994b2726774f8d93146681bb7a7fcd"


class Query_Search(object):

	base_url = 'https://api.spotify.com/v1/artists/'

	def search(self, query=None, operator=None, operator_query=None, search_type='artist'):
		if query == None:
			raise Exception("A query is required.")
		if isinstance(query, dict):
			query = ' '.join([f'{k}:{v}' for k,v in query.items()])
		# if operator != None and operator_query != None:
		# 	if operator.lower() == 'or' or operator.lower() == 'not':
		# 		operator = operator.upper()
		# 		if isinstance(operator_query, str):
		# 			query = f'{query} {operator} {operator_query}'
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


class Spotify_API(Query_Search):
	access_token = None
	access_token_expires = datetime.datetime.now()
	access_token_did_expire = True
	# client_id = None
	# client_secret = None
	
	
	def __init__(self, client_id, client_secret, *args, **kwargs):
		self.client_id = client_id
		self.client_secret = client_secret
		
	def get_client_credentials(self):
		# client_id = self.client_id
		# client_secret = self.client_secret
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

	def perform_auth(self):
		token_url = 'https://accounts.spotify.com/api/token'
		token_data = {'grant_type':'client_credentials'}
		token_headers = self.get_token_headers()
		r = requests.post(token_url, data=token_data, headers=token_headers)
		if r.status_code not in range(200, 299):
			raise Exception("Could not authenticate client.")
		token_data = r.json()
		now = datetime.datetime.now()
		self.access_token = token_data['access_token']
		expires_in = token_data['expires_in']
		self.access_token_expires = now + datetime.timedelta(seconds=expires_in)
	
	def get_access_token(self):
		if self.access_token_expires < datetime.datetime.now() or self.access_token == None:
			self.perform_auth()
			return self.get_access_token()
		return self.access_token
	
	def get_resource_header(self):
		access_token = self.get_access_token()
		headers = {
			'Authorization':f'Bearer {access_token}'
		}
		return headers


# take the rest of this code and lets turn it into a refined search results file. 

def recent_albums_header():
	if len(spotify.get_artist_albums(artist_id)) == 0:
		return f'{user_search.title()} has no albums with Spotify.'
	elif len(spotify.get_artist_albums(artist_id)) == 1:
		return f"{user_search.title()}'s Album:"
	elif len(spotify.get_artist_albums(artist_id)) < 10:
		return f"{user_search.title()}'s Albums:"
	else:
		return f"{user_search.title()}'s 10 Most Recent Albums:"

spotify = Spotify_API(client_id, client_secret)

user_search = input('\nEnter an artist here: ')

if user_search == '':
	print("I'm sorry, you did not enter anything.")
	exit()

search_results = spotify.search(user_search, search_type='artist')

# this is where we need to raise the exception for IndexError if the user enters an artist that is not on spotify
try:
	artist_id = search_results['artists']['items'][0]['id'] # gets artist's ID
	artist_url = search_results['artists']['items'][0]['external_urls']['spotify']  # gets artist's URL 
except IndexError as error:
	print("\nSorry, that artist is not on Spotify.\n")
	exit()

print('\n')

print(recent_albums_header() + '\n')

for album in spotify.get_artist_albums(artist_id):
	print(album)

print(f"\n{user_search.title()}'s Top Tracks on Spotify: \n")

if len(spotify.get_artists_top_tracks(artist_id)) < 10:
  for x in range(1, (len(spotify.get_artists_top_tracks(artist_id))+1)):
	  print(str(x) + ' - ' + (spotify.get_artists_top_tracks(artist_id)[x-1]))
else: 
  for x in range(1,11):
	  print(str(x) + ' - ' + (spotify.get_artists_top_tracks(artist_id)[x-1]))

print(f"\nVisit {user_search.title()}'s Spotify page via: {artist_url}\n")