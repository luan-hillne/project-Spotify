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
    load_df=Extract.search_for_track()
    if(Transform.Data_Quality(load_df) == False):
        raise ("Failed at Data Validation")
    Transformed_df=Transform.Transform_df(load_df)
    #The Two Data Frame that need to be Loaded in to the DataBase

#Loading into Database
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    #SQL Query to Create Track Songs
    sql_query_1 = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        id_album VARCHAR(50),
        name_track VARCHAR(200),
        uri VARCHAR(50),
        artist_name VARCHAR(200),
        date VARCHAR(50),
        top_track INT,
        CONSTRAINT primary_key_constraint PRIMARY KEY (id_album)
    )
    """
    # #SQL Query to Create Most Listened Artist
    # sql_query_2 = """
    # CREATE TABLE IF NOT EXISTS fav_artist(
    #     timestamp VARCHAR(200),
    #     ID VARCHAR(200),
    #     artist_name VARCHAR(200),
    #     count VARCHAR(200),
    #     CONSTRAINT primary_key_constraint PRIMARY KEY (ID)
    # )
    # """
    cursor.execute(sql_query_1)
    #cursor.execute(sql_query_2)
    print("Opened database successfully")

    #We need to only Append New Data to avoid duplicates
    try:
        load_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")
    try:
        Transformed_df.to_sql("fav_artist", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database2")

    #cursor.execute('DROP TABLE my_played_tracks')
    #cursor.execute('DROP TABLE fav_artist')

    conn.close()
    print("Close database successfully")
    
    