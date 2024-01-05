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

def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

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

token = get_token()
track_name = "tom"
# Creating an function to be used in other pyrhon files
def search_for_track(track_name):
    url ="https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={track_name}&type=track&limit=10"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_res = json.loads(result.content)["tracks"]["items"]

    if len(json_res) == 0:
        print("No artist with this name exist...")
        return None
    album_id  = []
    album_name = []
    album_release_date =[]

    artist_id = []
    artist_name = []
    artist_type = [] 

    track_id =[]
    track_name =[]
    popularity_track =[]
    
    for song in json_res:
        album_id.append(song["album"]["id"])
        album_name.append(song["album"]["name"])
        album_release_date.append(song["album"]["release_date"])

        artist_id.append(song["artists"][0]["id"])
        artist_name.append(song["artists"][0]["name"])
        artist_type.append(song["artists"][0]["type"])

        track_id.append(song["id"])
        track_name.append(song["name"])
        popularity_track.append(song["popularity"])

    album_dict = {
        "album_id":album_id,
        "album_name": album_name,
        "album_release_date":album_release_date,
    }

    artist_dict = {
        "artist_id":artist_id,
        "artist_name":artist_name,
        "artist_type":artist_type
    }

    track_dict = {
        "track_id": track_id,
        "track_name": track_name,
        "popularity_track": popularity_track
    }
    album_df = pd.DataFrame(album_dict, columns=['album_id','album_name','album_release_date'])
    artist_df = pd.DataFrame(artist_dict, columns=['artist_id','artist_name','artist_type'])
    track_df = pd.DataFrame(track_dict, columns = ['track_id','track_name','popularity_track'])

    return album_df,artist_df,track_df


#res = search_for_track("tom")
#print(res)