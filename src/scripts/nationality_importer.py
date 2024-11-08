from SPARQLWrapper import SPARQLWrapper, CSV #from stack overflow
import re
import numpy as np

def nationality_import(x): 
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    nationality = ["Other", "American"] #2 possibilities
    count = 0
    try : 
        count+=1
        print(count)
        sparql.setQuery(f"""
        SELECT (IF(CONTAINS(?abstract, "American"), TRUE, FALSE) AS ?containsAmerican) WHERE {{ 
        <http://dbpedia.org/resource/{str(x).replace(' ', '_')}> <http://dbpedia.org/ontology/abstract> ?abstract .
        FILTER (lang(?abstract) = "en")
        }}
        """)
        sparql.setReturnFormat(CSV)
        # -2 : one-before last character (last one is a space)
        # query.convert.decode outputs : "containsAmerican"1 or "containsAmerican"0 
        result = sparql.query().convert().decode("utf-8")[-2]
        print(result)
        actor_nat = nationality[int(result)]
    except Exception as e :
        pblm = x
        actor_nat = np.nan
    return actor_nat

  