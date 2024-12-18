# import the libraries needed to clean
import os
import ast # needed to clean the dataset
import gzip # since IMDB datasets are compressed in the .gz format
import shutil # needed to write the .tsv file in a new file of IMDB dataset after extracting ir
import tarfile # sinve CMU datasets are compressed in the .tar.gz format
import numpy as np
import pandas as pd
from unidecode import unidecode # for handling non ACSII character for the purpose of writing csv files
from nationality_importer import parallelize_nationality_import # to import the nationality_importer.py (cf scripts folder)
from create_award_index import create_award_index # importing the function to create the award index from create_award_index.py (cf scripts folder)

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
OSCAR_SUBFOLDER = "OSCAR/"
GLOBES_SUBFOLDER = "GOLDENGLOBES/"


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

## OSCARS
print("Dataframes creation for OSCARS dataset starting.")
df_oscars = pd.read_csv(DATA_FOLDER + OSCAR_SUBFOLDER + 'database.csv')
print("Dataframes creation for OSCARS datasets done.")

## GOLDEN GLOBES
print("Dataframes creation for GLOBES dataset starting.")
df_globes = pd.read_csv(DATA_FOLDER + GLOBES_SUBFOLDER + 'golden_globe_awards.csv')
print("Dataframes creation for GLOBES datasets done.")

################################################## Cleaning CMU dataset ##########################################################
df_movie_metadata_CMU.columns = ['wiki_movie_ID', 'freebase_movie_ID', 'title', 'release_date', 'box_office', 'runtime', 'languages', 'countries', 'genres']
df_character_metadata_CMU.columns = ['wiki_movie_ID', 'freebase_movie_ID', 'release_date', 'character_name', 'birth_date', 'gender', 'height', 'ethnicity', 'actor_name', 'age_at_release','freebase_map_ID', 'freebase_char_ID', 'freebase_actor_ID']
df_tvtropes_clusters_CMU.columns = ['persona','dictionary']

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

# Correcting manually some wrong movie time using Wikipedia to have a more meaningful distribution
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
# Correcting the age outliers in character dataset : age at release is a float
clean_df_character_metadata_CMU['age_at_release'] = clean_df_character_metadata_CMU['age_at_release'].apply(lambda x: abs(x) if abs(x) < 100 else np.nan)
# Keeping only years as actor date of birth in character dataset - output years are strings (use pd.numeric if operations needed) : input is object 
# Replacing the 'nan' by np.nan 
clean_df_character_metadata_CMU['birth_date'] = pd.to_numeric(clean_df_character_metadata_CMU['birth_date'].astype(str).str[:4], errors='coerce')
#CLEANER CA 
clean_df_character_metadata_CMU['birth_year'] = clean_df_character_metadata_CMU['birth_date'].astype('Int64').apply(lambda x: x if 1800 <= x<= 2016 else np.nan)
# Modifying manually one "weird" release date (cf. above same modification for the movie.metadata)
clean_df_character_metadata_CMU['release_date'] = clean_df_character_metadata_CMU['release_date'].replace('1010-12-02', '2012-10-19')

# Similarly keeping only years as movie release date - input is object 
clean_df_character_metadata_CMU['release_year'] = clean_df_character_metadata_CMU['release_date'].astype(str).str[:4].replace('nan', np.nan, inplace=True)
# Convert release year to numeric, nan str have been converted to nan int 
clean_df_character_metadata_CMU['release_year'] = clean_df_character_metadata_CMU['release_year'].astype('Int64')

# Clean height outliers (only the larger values) - the small values (0.6m) correspond to children
clean_df_character_metadata_CMU['height'] = clean_df_character_metadata_CMU['height'].apply(lambda x : x if x<2.5 else np.nan)
# Change actors ethnicity by their nationality (American or other)
clean_df_character_metadata_CMU.drop(columns='ethnicity')
# Nationality
# Here we iterqte over the dataset and perform the SPARQL query
clean_df_character_metadata_CMU['nationality'] = parallelize_nationality_import(clean_df_character_metadata_CMU, 'actor_name')
# Once we have peformed the query and written nationalities as a csv, we can re-run cleaning processes without redoing the query every time, using the lines below 
#nationality = pd.read_csv('data/nationality.csv',header=None, names=['nationality'], skiprows=1) #temporary
#clean_df_character_metadata_CMU['nationality'] = nationality['nationality'] #temporary

## PERSONAS 
# Already cleaned since comes from the reference paper (Bramman et al., 2015) coming along with the CMU dataset

## OSCARS
# Filter for awards provided only for acting achievements 
df_oscars_actors = df_oscars['Award'].str.contains('Actor|Actress') # The concerned awards contain the words 'Actor' or 'Actress'
index_actors = [i for i,x  in enumerate(list(df_oscars_actors)) if x == True] # Creates an index for the rows with the wanted awards 
df_oscars_actors = df_oscars.iloc[index_actors]

# Clean the column 'Year': keep only the first four letters:
df_oscars_actors['Year'] = df_oscars_actors['Year'].apply(lambda x: x[:4])

# Create a column with the right count of the winners to keep track of the winners
winners = df_oscars_actors.groupby('Name').agg({'Winner': 'sum'})
# Create a column with the number nominations for an oscar for each actor:
nominations = df_oscars_actors.groupby('Name', as_index=False)['Name'].value_counts()
df_oscars_actors['Winner'] = df_oscars_actors['Winner'].apply(lambda x: True if x == 1 else False) # Creates a more reasonable value for if the actor won or not 

# Preparing the dataframe for csv writing
# Group by "actors" to have unique values "Name" for the actors:
df_oscars_clean = df_oscars_actors.groupby('Name', as_index=False).first() # first() only keeps the first row of a grouped dataframe

# Add the columns to the dataset with unique values by merging
df_oscars_clean = pd.merge(df_oscars_clean, winners, left_on='Name', right_index=True)
df_oscars_clean = pd.merge(df_oscars_clean, nominations, left_on='Name', right_on='Name') # Add number of nominations to the dataset
# Drop supplement columns, rename columns
df_oscars_clean = df_oscars_clean.drop(['Winner_x', 'Year', 'Ceremony', 'Film', 'Award'], axis = 1)
df_oscars_clean = df_oscars_clean.rename(columns = {'Winner_y' : 'nr_wins', 'count' : 'nr_nominations', 'Name' : 'nominee'})

# Renameing also the df_oscars_actors columns for conistency
df_oscars_actors = df_oscars_actors.rename(columns={'Year' : 'year', 'Ceremony': 'ceremony', 'Award': 'award', 'Winner': 'winner', 'Name': 'nominee', 'Film' : 'film'})

# Creating an award index for oscars using the create_award_index function (cf create_award_index.py):
df_oscars_clean['oscar_index'] = create_award_index(df_oscars_clean['nr_nominations'], df_oscars_clean['nr_wins'])


## GOLDEN GLOBES
# Renaming columns for consitency with OSCARS dataset
df_globes.rename(columns= {'year_award': 'year', 'category': 'award', 'win' : 'winner'}, inplace=True)
# Filter for awards provided only for acting achievements 
actor_awards = df_globes['award'].str.contains('Actor|Actress')
index_actors = [i for i,x  in enumerate(list(actor_awards)) if x == True]
df_globes_actors = df_globes.iloc[index_actors]

# Count times of nominations of each actor
nominations = df_globes_actors.groupby('nominee', as_index=False)['nominee'].value_counts()
# Count times wins of each actor:
winners = df_globes_actors.groupby('nominee', as_index=False).agg({'winner': 'sum'})

# Merge the data:
df_globes_clean = df_globes_actors.groupby('nominee', as_index=False).first() # first() only keeps the first row of a grouped dataframe
df_globes_clean = pd.merge(df_globes_clean, nominations, left_on='nominee', right_on='nominee')
df_globes_clean = pd.merge(winners, df_globes_clean, left_on='nominee', right_on='nominee')
df_globes_clean.drop(['year_film', 'year', 'ceremony', 'award', 'film', 'winner_y'], axis = 1, inplace=True)
df_globes_clean = df_globes_clean.rename(columns= {'winner_x' : 'nr_wins', 'count' : 'nr_nominations'})

# Creating an award index for golden globe awards using the create_award_index function (cf create_award_index.py):
df_globes_clean['globes_index'] = create_award_index(df_globes_clean['nr_nominations'], df_globes_clean['nr_wins'])

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

# to ensure that 'release_year' stays an int when writing it to the csv file
df_movies_full_left['release_year'] = df_movies_full_left['release_year'].astype('Int64')

# 1b) Merging the clean CMU movie dataset with the actor dataset -- USEFUL, LEAVE IT !! :)
clean_df_character_metadata_CMU.drop(columns=['release_date','release_year'], inplace=True)
df_character_final = pd.merge(clean_df_character_metadata_CMU, clean_df_movie_metadata_CMU, on=['wiki_movie_ID', 'freebase_movie_ID'], how='inner')
df_character_final.drop(columns=[ 'runtime', 'languages','genres'], inplace=True)

# Commented for now but maybe useful for later
# 1c) Merging the clean character dataset with the personas dataset
# df_character_personas = pd.merge(clean_df_character_metadata_CMU, df_tvtropes_clusters_CMU, on=['character_name', 'actor_name', 'freebase_map_ID'], how='left')
# df_character_personas.drop(columns=['release_date','birth_date', 'dictionary', 'ethnicity', 'freebase_map_ID','freebase_char_ID','freebase_actor_ID'], inplace= True)
#df_character_personas.to_csv("data/character_personas_CMU.csv", sep=',', encoding='utf-8', index=False, header=True)

################################################## Writing CSV files ############################################################
df_movie_metada_full_left.to_csv("data/movie_metadata_CMU_IMDB.csv", sep=',', encoding='utf-8', index=False, header=True)
df_character_final.to_csv("data/actor_metadata_CMU.csv", sep=',', encoding='utf-8', errors='ignore',index=False, header=True)
df_tvtropes_clusters_CMU.to_csv("data/personas_metadata_CMU.csv",sep=',', encoding='utf-8', index=False, header=True)
df_plot_summaries_CMU.to_csv("data/plot_summaries_CMU.csv", sep=',', encoding='utf-8', index=False, header=True)

df_oscars_clean.to_csv("./ada-2024-project-adactylous/data/oscars_award_index.csv", sep=',', encoding='utf-8', index=False, header=True) # Write csv for oscar award index
df_globes_clean.to_csv("./ada-2024-project-adactylous/data/globes_award_index.csv", sep=',', encoding='utf-8', index=False, header=True) # Write csv for oscar award index