from spotify_creds import *
from spotify_api import *
from query_search import *
from artist_return import *


# anything on this page that is out of flow, you can make a artist class
# artist class will handle the output we want to display

# authorizes creds for the Spotify API
spotify = Spotify_API(client_id, client_secret)

# lets user search for an artist
user_input = Query_Search.user_input

# validates user's search to confirm they searched for an artist
Query_Search.artist_validation(user_input)

# returns json data of searched artist
artist_id = spotify.artist_search(user_input)['artists']['items'][0]['id']


album_head = Artist_Return.recent_albums_header()

print(album_head)

for album in spotify.get_artist_albums(artist_id):
	print(album)

print(f"\n{user_input.title()}'s Top Tracks on Spotify: \n")


print(f"\nVisit {user_input.title()}'s Spotify page via: {artist_url}\n")