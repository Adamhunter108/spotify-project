from spotify_creds import *
from Spotify_API import *
from Query_Search import *


# authorizes creds for the Spotify API
spotify = Spotify_API(client_id, client_secret)


# lets user search for an artist
user_input = spotify.user_input

# validates user's search to confirm they searched for an artist
# Query_Search.artist_validation(user_input)

# returns json data of searched artist
artist_id = spotify.get_artist_id(user_input)
artist_url = spotify.artist_search(user_input)['artists']['items'][0]['external_urls']['spotify']

print("\n" + spotify.recent_albums_header(artist_id) + "\n")

spotify.recent_albums(artist_id)

print(f"\n{user_input.title()}'s Top Tracks on Spotify: \n")

spotify.artists_top_tracks(artist_id)

print(f"\nVisit {user_input.title()}'s Spotify page via: {artist_url}\n")