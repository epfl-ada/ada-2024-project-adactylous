# America first ? The influence of America in the global cinema


# Abstract:
The end of the 19th century witnessed the start of narrative film production, driven by European pioneers like LePrince, the Lumière brothers & Mélies. However, the US American film industry soon took over the lead and the 20th century (1920s-60s) marks the golden age of Hollywood cinema (Radulovich, 2015). In 2009, the United States still seem to dominate the worldwide film industry with the top 20 highest-grossing films worldwide being American or American co-productions (Crane, 2014). This hegemony, that we aim at characterizing more precisely, should also significantly influence filmmaking trends including cast composition. Thus, we would also like to investigate what makes American movies so different and so successful compared to the rest of the world. Besides from movie production, audiences usually prefer American films over locally produced movies, e.g. in Sydney (Sedgwick et al., 2014). This tendency introduces new cultural paradigms, with an Americanization of local cultures and a diffusion of USA soft power, for instance in China (Yan et al., 2024). This raises additional questions on the cultural interlinks drawn by movies, between the United States and other nations. 


# Research Questions:
During this project, we will address the following research questions :
1) Are American movies more successful than movies from other production countries ?
2) Does being American favor a successful acting career ?
3) How is USA soft power visible in American movies and does it influence non-American movies?
The corresponding embedded questions are described in the next section 'Methods'.

# Proposed additional datasets
To conduct this project, we are enriching the CMU dataset using additional datasets and queries :
- “IMDB” Dataset : that contains ratings, number of votes, simplified movie's genres and attributes that are already present in the movies’ metadata dataset (release year, title and runtime). This dataset is merged with the dataset containing movies' metadata on runtime, release year and movie title attributes. [Link](https://developer.imdb.com/non-commercial-datasets/)

- ”DBpedia scraping” : Iterating over each actor name in the CMU dataset, we performed a SPARQL query to form a new column, “nationality”. The query uses the actor name to access the actor’s DBpedia page and checks whether the abstract contains the word “American”. If ”American” is found, the actor's nationality is set to “American”; otherwise, it is set to “Other”. If an error occurs, generally because the DBpedia page is incomplete, the nationality is set to NaN. With this query, we have a nationality value for all 450 000 actors of the CMU dataset - with 31% NaN - However, this method cannot account for dual nationalities. 
    - Initial input from: [Link](https://tinysubversions.com/notes/how-to-query-wikipedia/)
    - Typical DBpedia actor page: [Link](https://dbpedia.org/page/Frankie_Jonas)

Later on in the project, we will also include the “The Academy Awards 1927-2015” Dataset. This dataset contains all actors and movies nominated for or winning an Oscar each year. It includes 5747 unique values for nominees, of whom 244 are actors and actresses. Since the list of Oscar-nominees is complete, we are certain that no other actor or actress has ever been nominated and, therefore, we can use this dataset to enrich the Actors’ Career Success Index (ACSI) (see below) we plan to create ([Link](https://www.kaggle.com/datasets/theacademy/academy-awards/data)) 


# Methods
General :
Movies are categorized as strictly American movies, partially American movies (where the countries of production include the USA but are not limited to it), and movies from all other countries. Indeed, we believed it was interesting to distinguish those three cases (and results have shown it is), especially in recent years where lots of movies are co-produced. 
During the cleaning, we decided not to merge the tvtropes dataset - containing only 501 lines - with the actors dataset, to avoid filling lots of rows with NaN values.

Tools : Significance tests will extensively be used to determine the relevance of the observed patterns.

**For research question 1** : 
Explore the translations of strictly and partially American movies into other languages, and the translations of non-American movies into English. 
Explore the box office revenue, the runtime and IMDB ratings : are they significantly higher for American movies than for movies with other countries of production ?
Create a Movies Success Index (MSI), including parameters like number of translations, box office, and IMDB ratings. Weights will be deduced from a regression with the best strictly and partially Americain movies.

**For research question 2** : 
Create an Actor’s Career Success Index (ACSI), including parameters like the duration of the career, revenue from movies in which she/he acted, and the number of movies acted in. This way, we can evaluate the parameters of a successful actor career and link those with American origin or/and American films
 Examine the age of American and non-American actors at the time of their first movie. This way, we could answer : Does being American help launch the actor's career
 Investigate the box office revenue of the movies in which each actor acted, and explore whether the first movie in a series of high box-office revenue films is strictly or partially American. This way, we can answer : Does acting in a strictly or partially American movie help launch the actor's career? 

**For research question 3** : This section focuses on the plot summaries of the movies. For each topic, a set of key-words will be created and used to explore the summaries. 
First, we will determine whether historical events related to the USA (e.g. Cold War, 9/11 or Wall Street) influence worldwide cinema. 
Then, we explore how American culture is visible in partially-Americain and non-American movies, like McDonalds, Thanksgiving or Baseball. 
We will also look for the main stereotypes carried by Americain movies and whether they appear similarly in partially-American and non-American movies. For this last step, we’ll use the tvtropes datatset, created from the reference article (Bamman et al. 2013)  

# Proposed timeline
Week 10 : 
- RQ 1: Finish  exploration of the actor dataset
- RQ 2: Continue exploration of the actor dataset
- RQ 3: Look for datasets of words and major events (Thanksgiving, 09/11…), characteristic of America and American life.

Week 11 : 
- RQ 1: Define a Movies Success Index (MSI) formula
- RQ 2: Define an Actor’s Career Success Index (ACSI)  formula. Investigate the personas and associated stereotypes 
- RQ 3: Perform the search of USA presence in movie plot summaries 

Week 12 :
- RQ 1: Finish MSI, clean and select plots to keep for the website
- RQ 2: Analyze possible relationships between ACSI, personas and associated stereotypes 
- RQ 3: Plot creation and analysis of the results

Week 13 :
- Integration of the results into the website
- Qualitative description and cross interpretation of all the results
- Historical context and analysis for result interpretation, conclusion drawing

Week 14 :
- Last improvements and adjustments of the final product/website
- Proofreading, visual completion

# Organization within the team :
- For RQ 1 : Luca, Claire
- For RQ 2 : Germana
- For RQ 3 : Chloé, Marlen


# Bibliography
- Crane, D. (2014): European Audiovisual Observatory, 2010. Focus 2009: world film market trends. Cannes: Marché du Film. International Journal of Cultural Policy, 20(4), 365–382, DOI: 10.1080/10286632.2013.832233.
- Radulovich, S. (2015): Classical Hollywood Cinema and Post-Classical Hollywood Cinema; Case Study of Modern and Postmodern Film. Undergraduate thesis, University of Rijeka, Faculty of Humanities and Social Sciences, accessed 15 November 2024, https://urn.nsk.hr/urn:nbn:hr:186:725674
- Sedgwick, J., Pokorny, M. and Miskell, P. (2014): Hollywood in the world market – evidence from Australia in the mid-1930s. Business History, 56(5),  689–723. DOI: 10.1080/00076791.2013.837891.
- Yan, J., Li, N. and Yu, F. (2024): “An empirical study of trade effect on culture” Journal of Applied Economics, 27(1). DOI: 10.1080/15140326.2024.2334551.

# ada-2024-project-adactylous
ada-2024-project-adactylous created by GitHub Classroom
