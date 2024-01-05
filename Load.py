import Extract
import Transform
import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"

if __name__ == "__main__":

#Importing the songs_df from the Extract.py
    album_df, artist_df, track_df = Extract.search_for_track("Tom")
    check_song = Transform.song_df(album_df, artist_df, track_df)
    if(Transform.Data_Quality(check_song) == False):
        raise ("Failed at Data Validation")
    transformed_album, transformed_artist, transformed_track = Transform.Transform_df(album_df, artist_df, track_df)
    #The Three Data Frame that need to be Loaded in to the DataBase

#Loading into Database
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    #SQL Query to Create Track Songs
    sql_query_1 = """
    CREATE TABLE IF NOT EXISTS my_album(
        album_id VARCHAR(50),
        album_name VARCHAR(50),
        album_release_date DATE,
        PRIMARY KEY (album_id)
    )
    """
    #SQL Query to Create Most Listened Artist
    sql_query_2 = """
    CREATE TABLE IF NOT EXISTS my_artist(
        artist_id VARCHAR(50),
        artist_name VARCHAR(50),
        artist_type VARCHAR(20),
        PRIMARY KEY (artist_id)
    )
    """
    sql_query_3 = """
    CREATE TABLE IF NOT EXISTS my_track(
        track_id VARCHAR(50),
        track_name VARCHAR(50),
        track_top INT,
        PRIMARY KEY (track_name)
    )
    """
    cursor.execute(sql_query_1)
    cursor.execute(sql_query_2)
    cursor.execute(sql_query_3)
    print("Opened database successfully")

    #We need to only Append New Data to avoid duplicates
    try:
        transformed_album.to_sql("my_album", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")
    try:
        transformed_artist.to_sql("my_artist", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database2")
    try:
        transformed_track.to_sql("my_track", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database3")
    #cursor.execute('DROP TABLE my_album')
    #cursor.execute('DROP TABLE my_artist')

    conn.close()
    print("Close database successfully")
    
    