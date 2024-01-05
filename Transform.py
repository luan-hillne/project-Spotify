import Extract
import pandas as pd
import re
# re.sub function to replace any content within parentheses with an empty string
# Set of Data Quality Checks Needed to Perform Before Loading
def Data_Quality(check_song):
    # Checking Whether the DataFrame is empty
    if check_song.empty:
        print('No Songs Extracted')
        return False

    # Enforcing Primary keys since we don't need duplicates
    if pd.Series(check_song['album_id']).is_unique:
        pass
    else:
        # The Reason for using an exception is to immediately terminate the program and avoid further processing
        raise Exception("Primary Key Exception, Data Might Contain duplicates")

    # Checking for Nulls in our data frame
    if check_song.isnull().values.any():
        raise Exception("Null values found")

def remove_parentheses(text):
    return re.sub(r'\([^)]*\)', '', text).strip()

def Transform_df(album_df, artist_df, track_df):
    #remove all symbol, parentheses
    album_df['album_name'] = album_df['album_name'].apply(remove_parentheses)

    # dt.strftime convert to given date format
    album_df['album_release_date'] = pd.to_datetime(album_df['album_release_date'], format='%Y-%m-%d')
    album_df['album_release_date'] = album_df['album_release_date'].dt.strftime('%m-%d-%Y')


    # strip() used to remove leading and trailing characters
    track_df['track_name'] = track_df['track_name'].apply(remove_parentheses)
    track_df.sort_values(by='popularity_track', ascending=False, inplace=True)
    track_df.rename(columns={'popularity_track': 'track_top'}, inplace=True)
    
    # Selecting specific columns
    transformed_album = album_df[['album_id', 'album_name', 'album_release_date']]
    transformed_artist = artist_df[['artist_id', 'artist_name', 'artist_type']]
    transformed_track = track_df[['track_id', 'track_name', 'track_top']]

    return transformed_album, transformed_artist, transformed_track

def song_df(album_df, artist_df, track_df):
    song_df = pd.concat([album_df, artist_df, track_df], axis=1)
    song_df.reset_index(drop=True, inplace=True)  # Resetting index
    return song_df

if __name__ == "__main__":
    # Importing the songs_df from the Extract.py
    album_df, artist_df, track_df = Extract.search_for_track("Tom")
    check_song = song_df(album_df, artist_df, track_df)
    Data_Quality(check_song)
    transformed_album, transformed_artist, transformed_track = Transform_df(album_df, artist_df, track_df)
    print(transformed_artist)
