import Extract
import pandas as pd 

# Set of Data Quality Checks Needed to Perform Before Loading
def Data_Quality(load_df):
    #Checking Whether the DataFrame is empty
    if load_df.empty:
        print('No Songs Extracted')
        return False
    
    #Enforcing Primary keys since we don't need duplicates
    if pd.Series(load_df['id_album']).is_unique:
       pass
    else:
        #The Reason for using exception is to immediately terminate the program and avoid further processing
        raise Exception("Primary Key Exception,Data Might Contain duplicates")
    
    #Checking for Nulls in our data frame 
    if load_df.isnull().values.any():
        raise Exception("Null values found")
    
def extract_uri_id(uri):
    return uri.split(":")[-1]

# Writing some Transformation Queries to get the count of artist
def Transform_df(load_df):
    # Convert 'release_date' to datetime format

    # Applying transformation logic
    load_df['date'] = load_df['release_date'] + ' : ' + load_df['release_date_precision']
    load_df.rename(columns={'popularity_track': 'top_track'}, inplace=True)
    load_df['uri'] = load_df['uri'].apply(extract_uri_id)

    # Selecting specific columns
    transformed_df = load_df[['id_album', 'name_track', 'uri', 'artist_name', 'date', 'top_track']]
    return transformed_df
if __name__ == "__main__":
    # Importing the songs_df from the Extract.py
    load_df = Extract.search_for_track()
    #print(load_df)
    Data_Quality(load_df)

    # Calling the transformation
    transformed_df = Transform_df(load_df)
    print(transformed_df)








    
    