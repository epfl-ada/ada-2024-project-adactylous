# import the libraries needed to clean
import os
import ast # needed to clean the dataset
import gzip # since IMDB datasets are compressed in the .gz format
import shutil # needed to write the .tsv file in a new file of IMDB dataset after extracting ir
import tarfile # sinve CMU datasets are compressed in the .tar.gz format
import numpy as np
import pandas as pd
from unidecode import unidecode

# Define a helper function to extract the names by importing **ast** to safely parse the strings into dictionaries
def clean_column(dict_string):
    # Use ast.literal_eval to safely parse the string into a dictionary as in
    # https://stackoverflow.com/questions/39169718/convert-string-to-dict-then-access-keyvalues-how-to-access-data-in-a-class 
    try:
        parsed_dict = ast.literal_eval(dict_string)
        return ', '.join(parsed_dict.values())  # Join all names into a single string based on the comma between them
    except (ValueError, SyntaxError):
        return dict_string  # Return the string as it is if parsing fails


DATA_FOLDER = "data/raw/"
CMU_SUBFOLDER = "CMU/"
IMDB_SUBFOLDER = "IMDB/"


################################################## Extraction ##################################################################
compressed_folders_list_CMU = ["data/raw_zip/MovieSummaries.tar.gz", "data/raw_zip/corenlp_plot_summaries.tar"] # 2 CMU datasets
compressed_files_list_IMDB = ["data/raw_zip/title.ratings.tsv.gz", "data/raw_zip/title.basics.tsv.gz"] # 2 IMDB datasets

##### CMU
# Extract contents of the .tar file into the folder
print("Extraction starting...")
for compressed_folder in compressed_folders_list_CMU:
    with tarfile.open(compressed_folder, 'r') as tar_ref:
        tar_ref.extractall(path=DATA_FOLDER + CMU_SUBFOLDER)
        print(f"Extraction completed of folder {compressed_folder}.")       
# après y'a encore bcp de fichiers xml.gz à extraire dans le corenplot datasets --> pour plus tard

###### IMDB
# The procedure is different here since the IMDB files are compressed in the gz format and are single files, not folders
for compressed_file in compressed_files_list_IMDB:
    tsv_file_path = os.path.join(DATA_FOLDER, IMDB_SUBFOLDER, os.path.basename(compressed_file)[:-3]) # remove the 3 last characters corresponding to '.gz' so that a clean tsv file is created
    with gzip.open(compressed_file, 'rb') as file_in: #gzip
        with open(tsv_file_path, 'wb') as file_out:
            shutil.copyfileobj(file_in, file_out)
            print(f"TSV file {tsv_file_path} created")

print(f"All tsv files have been created and saved in the {IMDB_SUBFOLDER} subfolder.")

################################################## Reading ###################################################################
file_path = DATA_FOLDER + CMU_SUBFOLDER + "/MovieSummaries"

print("Dataframes creation starting for CMU datasets...")

df_plot_summaries_CMU = pd.read_csv(file_path + "/plot_summaries.txt", delimiter="\t", header=None, names=["ID", "Summary"]) # renaming the columns for better understanding
df_movie_metadata_CMU = pd.read_csv(file_path + "/movie.metadata.tsv", delimiter="\t", header=None) 
df_character_metadata_CMU = pd.read_csv(file_path + "/character.metadata.tsv", delimiter="\t", header=None) 
df_tvtropes_clusters_CMU = pd.read_csv(file_path + "/tvtropes.clusters.txt", delimiter="\t", header=None) 
df_name_clusters_CMU = pd.read_csv(file_path + "/name.clusters.txt", delimiter="\t", header=None) 

print("Dataframes creation for CMU datasets done.")

## IMDB
print("Dataframes creation for IMDB datasets starting. This takes around 3 minutes.")
df_basics_IMDB = pd.read_csv(DATA_FOLDER + IMDB_SUBFOLDER + "/title.basics.tsv", delimiter = '\t', low_memory= False)  # low_memeory = False to ensure no mixed types according to documentation
df_ratings_IMDB = pd.read_csv(DATA_FOLDER + IMDB_SUBFOLDER + "/title.ratings.tsv", delimiter = '\t')

print("Dataframes creation for IMDB datasets done.")

################################################## Cleaning CMU dataset ##########################################################
df_movie_metadata_CMU.columns = ['wiki_movie_ID', 'freebase_movie_ID', 'title', 'release_date', 'box_office', 'runtime', 'languages', 'countries', 'genres']
df_character_metadata_CMU.columns = ['wiki_movie_ID', 'freebase_movie_ID', 'release_date', 'character_name', 'birth_date', 'gender', 'height', 'ethnicity', 'actor_name', 'age_at_release','freebase_map_ID', 'freebase_char_ID', 'freebase_actor_ID']
df_tvtropes_clusters_CMU.columns = ['cluster','dictionary']

clean_df_movie_metadata_CMU = df_movie_metadata_CMU.copy() # copy of original data frame to avoid messing it up
clean_df_character_metadata_CMU = df_character_metadata_CMU.copy()

# MOVIE METADATA
# Cleaning the dataset columns
clean_df_movie_metadata_CMU['languages'] = clean_df_movie_metadata_CMU['languages'].apply(clean_column)
clean_df_movie_metadata_CMU['countries'] = clean_df_movie_metadata_CMU['countries'].apply(clean_column)
clean_df_movie_metadata_CMU['genres'] = clean_df_movie_metadata_CMU['genres'].apply(clean_column)

# Creating a new columns for the 'realease_date' of the movie
# Parameter 'coerce' to convert the relase year to float64 while keeping NaN values according to the documentation
clean_df_movie_metadata_CMU['release_year'] = pd.to_numeric(clean_df_movie_metadata_CMU['release_date'].astype(str).str[:4], downcast="integer", errors = 'coerce')
clean_df_movie_metadata_CMU['release_year'] = clean_df_movie_metadata_CMU['release_year'].astype('Int64')

# Correcting the date 1010 that correspondonds to 2010 accroding to the following link
# https://en.wikipedia.org/wiki/Hunting_Season_(2010_film) 
# use of the loc syntax to really modify the dataframe and not its view
clean_df_movie_metadata_CMU.loc[clean_df_movie_metadata_CMU['release_year'] == 1010, 'release_year'] = 2010
clean_df_movie_metadata_CMU.loc[clean_df_movie_metadata_CMU['release_date'] == '1010-12-02', 'release_date'] = '2010-12-02'

# https://en.wikipedia.org/wiki/Thiruthani_(film)
clean_df_movie_metadata_CMU.loc[clean_df_movie_metadata_CMU['title'] == 'Thiruthani', 'release_year'] = 2012
clean_df_movie_metadata_CMU.loc[clean_df_movie_metadata_CMU['title'] == 'Thiruthani', 'release_date'] = '2012-10-19'

# https://en.wikipedia.org/wiki/Paradise_in_Harlem 
clean_df_movie_metadata_CMU.loc[clean_df_movie_metadata_CMU['title'] == 'Paradise in Harlem', 'release_year'] = 1939

# Correcting the runtime outlier of the the film Zero Tolerance that has a tremendous runtime value to the duration written in wikipedia
# https://en.wikipedia.org/wiki/Zero_Tolerance_(1994_film)
clean_df_movie_metadata_CMU.loc[clean_df_movie_metadata_CMU['title'] == 'Zero Tolerance', 'runtime'] = 94.0
# https://en.wikipedia.org/wiki/Paradise_in_Harlem
clean_df_movie_metadata_CMU.loc[clean_df_movie_metadata_CMU['title'] == 'Paradise in Harlem', 'runtime'] = 85.0
# https://en.wikipedia.org/wiki/Kai_Kodutha_Deivam 
clean_df_movie_metadata_CMU.loc[clean_df_movie_metadata_CMU['title'] == 'Kai Koduttha Dheivam', 'runtime'] = 164.0
# https://www.imdb.com/title/tt0371636/ 
clean_df_movie_metadata_CMU.loc[clean_df_movie_metadata_CMU['title'] == 'Dil Ne Phir Yaad Kiya', 'runtime'] = 147.0
# https://en.wikipedia.org/wiki/Dhool_Ka_Phool
clean_df_movie_metadata_CMU.loc[clean_df_movie_metadata_CMU['title'] == 'Dhool Ka Phool', 'runtime'] = 153.0
# https://en.wikipedia.org/wiki/Thiruthani_(film)
clean_df_movie_metadata_CMU.loc[clean_df_movie_metadata_CMU['title'] == 'Thiruthani', 'runtime'] = 145.0
# https://en.wikipedia.org/wiki/Rebound_(2005_film)  
clean_df_movie_metadata_CMU.loc[clean_df_movie_metadata_CMU['title'] == 'Rebound', 'runtime'] = 103.0
# https://en.wikipedia.org/wiki/Backfire_(1950_film) 
clean_df_movie_metadata_CMU.loc[clean_df_movie_metadata_CMU['title'] == 'Backfire', 'runtime'] = 91.0
# https://en.wikipedia.org/wiki/First_Yank_into_Tokyo 
clean_df_movie_metadata_CMU.loc[clean_df_movie_metadata_CMU['title'] == 'First Yank into Tokyo', 'runtime'] = 82.0

# TVTROPES
# Creating new columns for each key of the dictionary to separate its values
# https://www.geeksforgeeks.org/python-convert-string-dictionary-to-dictionary/
df_tvtropes_clusters_CMU['dictionary'] = df_tvtropes_clusters_CMU['dictionary'].apply(ast.literal_eval)
df_tvtropes_clusters_CMU[['character_name','title','freebase_map_ID','actor_name']] = pd.json_normalize(df_tvtropes_clusters_CMU['dictionary'])

# CHARACTERS METADATA
# Correcting the age outliers in character dataset : HOW
clean_df_character_metadata_CMU['age_at_release'] = pd.to_numeric(clean_df_character_metadata_CMU['age_at_release'].apply(lambda x: abs(x) if x < 0 else (x if x < 100 else np.nan)), errors='coerce')
# Keeping only years as actor date of birth in character dataset - output years are strings (use pd.numeric if operations needed)
# Replacing the 'nan' by np.nan 
clean_df_character_metadata_CMU['birth_date'] = clean_df_character_metadata_CMU['birth_date'].apply(lambda x:str(x)[:4]).replace('nan', np.nan)
# Modifying manually one "weird" release date
clean_df_character_metadata_CMU['release_date'] = clean_df_character_metadata_CMU['release_date'].replace('1010-12-02', '1900-01-01')
# Similarly keeping only years as movie release date 
clean_df_character_metadata_CMU['release_date'] = clean_df_character_metadata_CMU['release_date'].apply(lambda x:str(x)[:4]).replace('nan', np.nan)
# Clean height outliers (only the larger values) - the small values (0.6m) correspond to children
clean_df_character_metadata_CMU['height'] = clean_df_character_metadata_CMU['height'].apply(lambda x : x if x<2.5 else np.nan)
# Change actors ethnicity by their nationality (American or other)
clean_df_character_metadata_CMU.drop(columns='ethnicity')
# Nationality
from nationality_importer import nationality_import
#clean_df_character_metadata_CMU['nationality'] = nationality_import(clean_df_character_metadata_CMU, 'actor_name')
clean_df_character_metadata_CMU['nationality'] = clean_df_character_metadata_CMU['actor_name'].apply(lambda x: nationality_import(x))

################################################## Merging #############################################################

# 1a) Merging both IMDB datasets: title
# Inner join because want to keep only movies that have been rated by the public
df_basics_ratings_merged_IMDB = pd.merge(df_basics_IMDB, df_ratings_IMDB, on = 'tconst', how = 'inner') 

# Cleaning the rest and dropping useless columns for our analysis
# si met inplace = True ça agit direct sur le df, ie sans avoir besoin de créer une nouvelle variable
df_basics_ratings_merged_IMDB_cleaned = df_basics_ratings_merged_IMDB[(df_basics_ratings_merged_IMDB['titleType'] == 'short') | (df_basics_ratings_merged_IMDB['titleType'] == 'movie')]
df_IMDB_final = df_basics_ratings_merged_IMDB_cleaned.drop(columns = ['tconst', 'titleType', 'primaryTitle', 'isAdult', 'endYear'])
# Changing the datatypes for later merge with CMU dataset
# If ‘coerce’, then invalid parsing will be set as NaN, according to the documentation
df_IMDB_final['startYear'] = pd.to_numeric(df_IMDB_final['startYear'].replace("\\N", np.nan), errors = 'coerce').astype("Int64") 
df_IMDB_final['runtimeMinutes'] = pd.to_numeric(df_IMDB_final['runtimeMinutes'].replace("\\N", np.nan), errors = 'coerce').astype('float64')

# 2a) Merging the final IMDB with the clean CMU movie.metatdat
df_movie_metada_full_left = pd.merge(clean_df_movie_metadata_CMU, df_IMDB_final, left_on= ['title', 'runtime', 'release_year'], right_on= ['originalTitle', 'runtimeMinutes','startYear'], how = 'left', suffixes=('_CMU', '_IMDB'))

df_movie_metada_full_left.drop(columns=['runtimeMinutes', 'startYear', 'originalTitle'], inplace= True)


# Check for rows with non-UTF-8 characters and replace them
for col in df_movie_metada_full_left.columns:
    df_movie_metada_full_left[col] = df_movie_metada_full_left[col].apply(
        lambda x: unidecode(x) if isinstance(x, str) else x
    )

# Reorder the columns in a more convenient way
cols = ['wiki_movie_ID', 'freebase_movie_ID', 'title', 'release_date', 'release_year', 'runtime', 'languages', 'countries', 'box_office', 'averageRating', 'numVotes', 'genres_CMU', 'genres_IMDB']
df_movies_full_left = df_movie_metada_full_left[cols]

# to ensure that 'release_year' stays an int whne writing it to the csv file
df_movies_full_left['release_year'] = df_movies_full_left['release_year'].astype('Int64')


# 1b) Merging the clean CMU movie dataset witht the character dataset
df_movie_character_merged = pd.merge(clean_df_character_metadata_CMU, clean_df_movie_metadata_CMU, on=['wiki_movie_ID','freebase_movie_ID','release_date'], how='outer')
df_movie_character_final = pd.merge(df_movie_character_merged, df_tvtropes_clusters_CMU, on = ['freebase_map_ID', 'title', 'character_name','actor_name'], how='left')
df_movie_character_final.drop(columns=['release_date','ethnicity', 'freebase_map_ID','freebase_char_ID','freebase_actor_ID', 'languages', 'genres', 'dictionary'], inplace= True)


    

################################################## Writing CSV files ############################################################
df_movie_metada_full_left.to_csv("data/movie_metadata_CMU_IMDB.csv", sep=',', encoding='utf-8', index=False, header=True)
df_movie_character_final.to_csv("data/character_actor_metadata_CMU.csv",sep=',', encoding='utf-8', index=False, header=True)
df_plot_summaries_CMU.to_csv("data/plot_summaries_CMU.csv", sep=',', encoding='utf-8', index=False, header=True)