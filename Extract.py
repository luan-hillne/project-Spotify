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
track_name = "do"
# Creating an function to be used in other pyrhon files
def search_for_track():
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
    release_date_precision =[]
    release_date =[]
    uri = []
    #restriction =[]
    #artist_id = []
    artist_name = []
    #track_id =[]
    name_track =[]
    popularity_track =[]
    artist_type = []
    for song in json_res:
        album_id.append(song["album"]["id"])
        release_date_precision.append(song["album"]["release_date_precision"])
        release_date.append(song["album"]["release_date"])
        uri.append(song["uri"])
        #restriction.append(song["restrictions"][0]["reason"])
        #artist_id.append(song["artists"]["id"])
        artist_name.append(song["artists"][0]["name"])
        artist_type.append(song["artists"][0]["type"])
        #track_id.append(song["id"])
        name_track.append(song["name"])
        popularity_track.append(song["popularity"])

    album_dict = {
        "id_album":album_id,
        "release_date_precision": release_date_precision,
        "release_date":release_date,
        "uri": uri,
        # "restriction": restriction,
        "artist_type":artist_type,
        "artist_name":artist_name,
        #"track_id": track_id,
        "name_track": name_track,
        "popularity_track": popularity_track
    }
    album_df = pd.DataFrame(album_dict, columns=['id_album','name_track','release_date','uri','artist_type','artist_name','release_date_precision','popularity_track'])

    return album_df



# res = search_for_track(token,"Do")
# print(res)