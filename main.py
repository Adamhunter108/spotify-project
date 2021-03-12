from client_id_and_secret import *
from query import *
from search import *
import requests
import datetime
from urllib.parse import urlencode
import base64
import json



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
	print("\nDid you foget to type something?\n")
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