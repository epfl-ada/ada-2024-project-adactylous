from SPARQLWrapper import SPARQLWrapper, CSV #from stack overflow
import re
import numpy as np


def nationality_import(df, col_name): 
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    nationality = ["Other", "American"] #2 possibilities
    pblm = []
    actor_nat = []
    for i in df[col_name].head(500):  
        try : 
            print()
            sparql.setQuery(f"""
            SELECT (IF(CONTAINS(?abstract, "American"), TRUE, FALSE) AS ?containsAmerican) WHERE {{ 
            <http://dbpedia.org/resource/{str(i).replace(' ', '_')}> <http://dbpedia.org/ontology/abstract> ?abstract .
            FILTER (lang(?abstract) = "en")
            }}
            """)
            sparql.setReturnFormat(CSV)
        # -2 : one-before last character (last one is a space)
        # query.convert.decode outputs : "containsAmerican"1 or "containsAmerican"0 
            result = sparql.query().convert().decode("utf-8")[-2]
            print(result)
            actor_nat.append(nationality[int(result)])
        except Exception as e :
            pblm.append(i)
            actor_nat.append(np.nan)
    print(pblm)
    return actor_nat

  