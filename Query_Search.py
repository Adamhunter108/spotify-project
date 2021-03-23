from spotify_creds import *
import requests
from urllib.parse import urlencode
import json

class Query_Search(object):

	base_url = f'https://api.spotify.com/v1/artists/'

	# user_input = input('\nEnter an artist here: ')

	# def __init__(self, artist_id):
	# 	artist_id = self.get_artist_id(self.user_input)

	def get_artist_albums(self, artist_id):
		base_url = self.base_url
		headers = self.get_resource_header()
		r = requests.get(base_url + self.get_artist_id(self.user_input) + '/albums', headers=headers, params={'include_groups': 'album'})
		album_data = r.json()
		searched_albums = []
		for album in album_data['items']:
			if album['name'].lower() not in searched_albums:
				searched_albums.append(album['name'].lower()) 
		top_albums = [' '.join([word.capitalize() for word in album.split(' ')]) for album in searched_albums] 
		return top_albums[0:10]

	def recent_albums_header(self, artist_id):
		if len(self.get_artist_albums(artist_id)) == 0:
			return f'{self.user_input.title()} has no albums with Spotify.'
		elif len(self.get_artist_albums(artist_id)) == 1:
			return f"{self.user_input.title()}'s Album:"
		elif len(self.get_artist_albums(artist_id)) < 10:
			return f"{self.user_input.title()}'s Albums:"
		else:
			return f"{self.user_input.title()}'s 10 Most Recent Albums:"

	def recent_albums(self, artist_id):
		for album in self.get_artist_albums(artist_id):
			print(album)

	def get_artists_top_tracks(self, artist_id):
		base_url = self.base_url
		headers = self.get_resource_header()
		r = requests.get(base_url + artist_id + '/top-tracks', headers=headers, params={'include_groups': 'top-track', 'country':'US', 'limit': 11})
		top_tracks = r.json()
		if len(top_tracks['tracks']) < 10:
			return [top_tracks['tracks'][x]['name'] for x in range(len(top_tracks['tracks']))]
		else:
			return [top_tracks['tracks'][x]['name'] for x in range(10)] # returns artist's top 10 tracks in a list

	def artists_top_tracks(self, artist_id):
		if len(self.get_artists_top_tracks(artist_id)) < 10:
			for x in range(1, (len(self.get_artists_top_tracks(artist_id))+1)):
				print(str(x) + ' - ' + (self.get_artists_top_tracks(artist_id)[x-1]))
		else: 
			for x in range(1,11):
				print(str(x) + ' - ' + (self.get_artists_top_tracks(artist_id)[x-1]))