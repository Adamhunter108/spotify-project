from spotify_creds import *
from Spotify_API import *
from Query_Search import *
from Artist_Return import *


# anything on this page that is out of flow, you can make a artist class
# artist class will handle the output we want to display

# authorizes creds for the Spotify API
spotify = Spotify_API(client_id, client_secret)

# lets user search for an artist
user_input = Query_Search.user_input

# validates user's search to confirm they searched for an artist
Query_Search.artist_validation(user_input)

# returns json data of searched artist
search_results = spotify.artist_search(Query_Search.user_input)

# if search_results == '' or search_results == {}:
	# print("Sorry That is not on Spotify.")

artist_id = search_results['artists']['items'][0]['id']
print(artist_id)

Artist_Return.recent_albums_header()

for album in spotify.get_artist_albums(artist_id):
	print(album)

print(f"\n{Query_Search.user_input.title()}'s Top Tracks on Spotify: \n")


print(f"\nVisit {Query_Search.user_input.title()}'s Spotify page via: {artist_url}\n")