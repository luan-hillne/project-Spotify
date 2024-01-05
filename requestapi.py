from dotenv import load_dotenv
from requests import post,get
import json
import os
import base64  # Import base64 module
import pandas as pd
import requests
from datetime import datetime
import datetime
import logging as logger
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,  # Add space after "Basic"
        "Content-Type": "application/x-www-form-urlencoded",  # Correct spelling
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def search_for_artist(token, artist_name):
    url ="https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_res = json.loads(result.content)["artists"]["items"]

    if len(json_res) == 0:
        print("No artist with this name exist...")
        return None
    
    return json_res[0]
    #print(json_res)
def search_for_album(token, album_name):
    url ="https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={album_name}&type=album&limit=10"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_res = json.loads(result.content)["albums"]["items"]

    if len(json_res) == 0:
        print("No artist with this name exist...")
        return None
    id_album = []
    name_album =[]
    artist_name = []
    artist_id = []
    total_tracks = []

    for song in json_res:
        id_album.append(song['id'])
        name_album.append(song['name'])
        artist_name.append(song["artists"][0]["name"])
        artist_id.append(song["artists"][0]["id"])
        total_tracks.append(song['total_tracks'])

    album_dict = {
        "id_album":id_album,
        "name_album": name_album,
        "artist_name":artist_name,
        "artist_id": artist_id,
        "total_track": total_tracks
    }
    album_df = pd.DataFrame(album_dict, columns=['id_album','name_album','artist_name','artist_id','total_track'])

    return album_df

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        print(result.text)
        return None

    json_result = json.loads(result.content)

    if 'tracks' in json_result:
        return json_result['tracks']
    else:
        print("No 'tracks' key found in the response:")
        print(json_result)
        return None


token = get_token()

res = search_for_album(token,"a")
print(res)
# res = search_for_artist(token,"A")
# artist_id = res["id"]
# print(artist_id)
# songs = get_songs_by_artist(token,artist_id)
#print(songs)
#print(token)

# for idx,song in enumerate(songs):
#     print(f"{idx+1}.{song['name']}") 