from spotify_creds import *
from query_search import *
import requests
import datetime
import base64
import json

class Spotify_API(Query_Search):
	access_token = None
	access_token_expires = datetime.datetime.now()
	access_token_did_expire = True
		
	def __init__(self, client_id, client_secret, *args, **kwargs):
		self.client_id = client_id
		self.client_secret = client_secret
		
	def get_client_credentials(self):
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

	def artist_search(self, query):
		query_params = urlencode({'q':query, 'type':'artist'})
		headers = self.get_resource_header() 
		endpoint = 'https://api.spotify.com/v1/search'
		lookup_url = f'{endpoint}?{query_params}'
		r = requests.get(lookup_url, headers=headers)
		if r.status_code not in range(200,299):
			return {}
		return r.json()