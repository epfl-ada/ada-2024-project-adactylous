# import the libraries needed to clean
import os
import ast # needed to clean the dataset
import gzip # since IMDB datasets are compressed in the .gz format
import shutil # needed to write the .tsv file in a new file of IMDB dataset after extracting ir
import tarfile # sinve CMU datasets are compressed in the .tar.gz format
import numpy as np
import pandas as pd
from unidecode import unidecode

DATA_FOLDER = "data/raw/"
CMU_SUBFOLDER = "CMU/"
IMDB_SUBFOLDER = "IMDB/"
file_path = DATA_FOLDER + CMU_SUBFOLDER + "/MovieSummaries"


df_character_metadata_CMU = pd.read_csv(file_path + "/character.metadata.tsv", delimiter="\t", header=None)
df_character_metadata_CMU.columns = ['wiki_movie_ID', 'freebase_movie_ID', 'release_date', 'character_name', 'birth_date', 'gender', 'height', 'ethnicity', 'actor_name', 'age_at_release','freebase_map_ID', 'freebase_char_ID', 'freebase_actor_ID']
df_character_metadata_CMU = df_character_metadata_CMU.head(10) #a enlever
clean_df_character_metadata_CMU = df_character_metadata_CMU.copy()

clean_df_character_metadata_CMU['age_at_release'] = clean_df_character_metadata_CMU['age_at_release'].apply(lambda x: abs(x) if x < 0 else (x if x < 100 else np.nan))
clean_df_character_metadata_CMU['birth_date'] = pd.to_numeric(clean_df_character_metadata_CMU['birth_date'].astype(str).str[:4],  errors='coerce')

print(clean_df_character_metadata_CMU['height'].dtype)