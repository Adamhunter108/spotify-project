from spotify_creds import *
from Spotify_API import *
from Query_Search import *


# anything on this page that is out of flow, you can make a artist class
# artist class will handle the output we want to display


def recent_albums_header():
	if len(spotify.get_artist_albums(artist_id)) == 0:
		return f'{user_input.title()} has no albums with Spotify.'
	elif len(spotify.get_artist_albums(artist_id)) == 1:
		return f"{user_input.title()}'s Album:"
	elif len(spotify.get_artist_albums(artist_id)) < 10:
		return f"{user_input.title()}'s Albums:"
	else:
		return f"{user_input.title()}'s 10 Most Recent Albums:"

spotify = Spotify_API(client_id, client_secret)

user_input = input('\nEnter an artist here: ')

if user_input == '':
	print("\nDid you forget to type something?\n")
	exit()

search_results = spotify.artist_search(user_input, search_type='artist')

# if search_results == '' or search_results == {}:
	# print("Sorry That is not on Spotify.")

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

print(f"\n{user_input.title()}'s Top Tracks on Spotify: \n")

if len(spotify.get_artists_top_tracks(artist_id)) < 10:
  for x in range(1, (len(spotify.get_artists_top_tracks(artist_id))+1)):
	  print(str(x) + ' - ' + (spotify.get_artists_top_tracks(artist_id)[x-1]))
else: 
  for x in range(1,11):
	  print(str(x) + ' - ' + (spotify.get_artists_top_tracks(artist_id)[x-1]))

print(f"\nVisit {user_input.title()}'s Spotify page via: {artist_url}\n")