from SPARQLWrapper import SPARQLWrapper, CSV
import numpy as np
import concurrent.futures
import pandas as pd
from tqdm import tqdm

def nationality_import(x): 
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    nationality = ["Other", "American"]  # 2 possibilities
    try:
        sparql.setQuery(f"""
        SELECT (IF(CONTAINS(?abstract, "American"), TRUE, FALSE) AS ?containsAmerican) WHERE {{ 
        <http://dbpedia.org/resource/{str(x).replace(' ', '_')}> <http://dbpedia.org/ontology/abstract> ?abstract .
        FILTER (lang(?abstract) = "en")
        }}
        """)
        sparql.setReturnFormat(CSV)
        result = sparql.query().convert().decode("utf-8")[-2]
        actor_nat = nationality[int(result)]
    except Exception as e:
        # In case of any error, return NaN
        actor_nat = np.nan
    return actor_nat

def parallelize_nationality_import(df, column_name):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Apply the nationality_import function to each row in the specified column
        results = list(tqdm(executor.map(nationality_import, df[column_name]), total=len(df), desc="Processing Nationality"))
    # Create a new column in the dataframe with the results
    df['nationality'] = results
    return df


  