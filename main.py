from spotify_creds import *
from spotify_api import *
from query_search import *
from spotify_creds import *


# authorizes creds for the Spotify API
spotify = Spotify_API(client_id, client_secret)


# lets user search for an artist
user_input = Query_Search.user_input

# validates user's search to confirm they searched for an artist
# Query_Search.artist_validation(user_input)

# returns json data of searched artist
artist_id = spotify.artist_search(user_input)['artists']['items'][0]['id']
artist_url = spotify.artist_search(user_input)['artists']['items'][0]['external_urls']['spotify']

print("\n" + spotify.recent_albums_header(artist_id) + "\n")

spotify.recent_albums(artist_id)

print(f"\n{user_input.title()}'s Top Tracks on Spotify: \n")

spotify.artists_top_tracks(artist_id)

print(f"\nVisit {user_input.title()}'s Spotify page via: {artist_url}\n")