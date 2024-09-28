import os, sys
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic

load_dotenv()

if not os.getenv('SPOTIFY_CLIENT_ID') or not os.getenv('SPOTIFY_CLIENT_SECRET'):
    print("Error: Spotify client ID and/or client secret not found.")
    sys.exit(1)

try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                                                   client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                                                   redirect_uri='https://localhost:8000',
                                                   scope='playlist-read-private'))
except Exception as e:
    print(f"Error authenticating with Spotify: {e}")
    print("Please check your client ID and client secret and try again.")
    sys.exit(1)

playlists = []
for index, playlist in enumerate(sp.current_user_playlists()['items'], start=1):
    print(f"{index}. {playlist['name']}")
    playlists.append(playlist['id'])

# Get user input for playlist selection
while True:
    try:
        playlist_index = int(input("Enter the Playlist No. you want to add to YouTube Music: ")) - 1
        if 0 <= playlist_index < len(playlists):
            spotify_playlist_ID = playlists[playlist_index]
            break
        else:
            print(f"Invalid input. Please enter a number between 1 and {len(playlists)}.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try again.")



songs = []
playlist_tracks = sp.playlist_tracks(spotify_playlist_ID)

for index, item in enumerate(playlist_tracks['items']):
    songs.append({
        'name': item['track']['name'],
        'artist': item['track']['artists'][0]['name']
    })

# Authenticate with YouTube Music
ytmusic = YTMusic('oauth.json')

playlist_name = input("Enter the name of the playlist you want to create on YouTube Music: ")

playlistID = ytmusic.create_playlist(playlist_name, "Imported songs from Spotify")

# Add songs to the playlist
for song in songs:
    search_results = ytmusic.search(song["name"] + " " + song["artist"], filter="songs")

    if search_results:
        video_id = search_results[0]['videoId']
        ytmusic.add_playlist_items(playlistID, [video_id])
        print(f"Added '{song["name"]} by {song["artist"]}' to the playlist")
    else:
        print(f"Could not find '{song}' on YouTube Music")

print("Finished adding songs to 'Spotify Songs' playlist")