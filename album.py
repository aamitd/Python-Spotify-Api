# Importing necessary libraries
import json
import base64
from requests import post, get
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


# Function to get the access token for Spotify API
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf_8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": "Basic " + auth_base64,
               "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


# Function to generate the authorization header
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


# Function to search for an artist by name
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artists with this name exists...")
        return None

    return json_result[0]


# Function to get top tracks by artist
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=IL"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


# Function to get albums by artist
def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result


# Obtaining access token
token = get_token()

# Searching for an artist and getting their ID
result = search_for_artist(token, "Osher Cohen")
artist_id = result["id"]

# Getting top tracks and albums by the artist
songs = get_songs_by_artist(token, artist_id)
albums = get_albums_by_artist(token, artist_id)

# print(albums)
print()

# Displaying album information
for album in albums:
    print("Album Name: ", album["name"])
    # Accessing the 'total_tracks' attribute within the album object
    total_tracks = album.get("total_tracks", {})
    if total_tracks is not None:
        print("Total Tracks: ", total_tracks)

    # Accessing the 'external_urls' dictionary within the album object
    external_urls = album.get("external_urls", {})
    # Checking if Spotify has an 'external_urls' link.
    spotify_url = external_urls.get("spotify")

    if spotify_url:
        print("Link to the Album:", spotify_url)
    else:
        print("No spotify URL found for this album.")

    # Accessing the release_date directly from the album object
    album_release = album.get("release_date")
    if album_release:
        print("Album Release Date:", album_release)

    print()

# Displaying top tracks by the artist
for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")

