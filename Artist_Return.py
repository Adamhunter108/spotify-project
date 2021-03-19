from spotify_api import *
from query_search import *
from spotify_creds import *



class Artist_Return(Spotify_API):

	spotify = Spotify_API(client_id, client_secret)
	artist_id = spotify.artist_search(user_input)['artists']['items'][0]['id']
	artist_url = spotify.artist_search(user_input)['artists']['items'][0]['external_urls']['spotify']

	def __init__(self, artist_id):
		self.artist_id = artist_id

	def recent_albums_header(self):
		spotify = self.spotify
		artist_id = self.artist_id
		if len(spotify.get_artist_albums(artist_id)) == 0:
			return f'{user_input.title()} has no albums with Spotify.'
		elif len(spotify.get_artist_albums(artist_id)) == 1:
			return f"{user_input.title()}'s Album:"
		elif len(spotify.get_artist_albums(artist_id)) < 10:
			return f"{user_input.title()}'s Albums:"
		else:
			return f"{user_input.title()}'s 10 Most Recent Albums:"



# 	def __init__(self, artist_id, artist_url=None):
# 		self.artist_id = artist_id

# this will return top tracks from artist
# 	def get_top_tracks(self):
# 		pass

# 	def get_album_head(self):
# 		pass

# this will return albums from artist
# 	def get_album_format(self):
# 		pass





# spotify = Spotify_API(client_id, client_secret)

# user_input = input('\nEnter an artist here: ')

# if user_input == '':
# 	print("\nDid you forget to type something?\n")
# 	exit()

# search_results = spotify.artist_search(user_input, search_type='artist')

# # if search_results == '' or search_results == {}:
# 	# print("Sorry That is not on Spotify.")

# try:
# 	artist_id = search_results['artists']['items'][0]['id'] # gets artist's ID
# 	artist_url = search_results['artists']['items'][0]['external_urls']['spotify']  # gets artist's URL 
# except IndexError as error:
# 	print("\nSorry, that artist is not on Spotify.\n")
# 	exit()





# # how we determine how many albums are returned 
# print(recent_albums_header() + '\n')

# for album in spotify.get_artist_albums(artist_id):
# 	print(album)



# # how we were returning the top tracks to the user

# print(f"\n{user_input.title()}'s Top Tracks on Spotify: \n")

# if len(spotify.get_artists_top_tracks(artist_id)) < 10:
#   for x in range(1, (len(spotify.get_artists_top_tracks(artist_id))+1)):
# 	  print(str(x) + ' - ' + (spotify.get_artists_top_tracks(artist_id)[x-1]))
# else: 
#   for x in range(1,11):
# 	  print(str(x) + ' - ' + (spotify.get_artists_top_tracks(artist_id)[x-1]))

# print(f"\nVisit {user_input.title()}'s Spotify page via: {artist_url}\n")