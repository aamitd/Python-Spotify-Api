import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get

load_dotenv()

# Fetching Spotify API credentials from environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    # Generating the authentication string for the Spotify API
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf_8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    # Spotify API token URL
    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": "Basic " + auth_base64,
               "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}

    # Requesting access token from Spotify API
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def top_songs_in_israel(token, playlist_id):
    # Fetching top songs from a specific playlist in Israel
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


token = get_token()
playlist_id = "37i9dQZEVXbJ5J1TrbkAF9"
playlist_tracks = top_songs_in_israel(token, playlist_id)
print(playlist_tracks)
print()
song_id = None

i = 1
if playlist_tracks.get("items"):
    for track in playlist_tracks["items"]:
        track_details = track.get("track")

        if track_details:
            # Print track details
            print(f"{i}. Track Name: {track_details['name']}")
            artists = track_details.get("artists")

            if artists:
                # Print artists performing the track
                print("     Performed By:")
                for artist in artists:
                    print(f"    - {artist['name']}")
            else:
                print("No artist information available.")

            album_details = track_details.get("album")
            if album_details:
                track_date = album_details.get("release_date")
                if track_date:
                    # Print track release date
                    print("     Release Date:")
                    print(f"     - {track_date}")

            song_id = track_details.get("id")
            if song_id:
                # Print track ID
                print("     Song ID:")
                print(song_id)

            external_urls = track_details.get("external_urls", {})
            spotify_url = external_urls.get("spotify")
            if spotify_url:
                # Print track's Spotify URL
                print("     Song URL:")
                print(spotify_url)
            else:
                print("No spotify url has been found.")

            i += 1
            print()

        else:
            print("No tracks found in the playlist or playlist not accessible.")

