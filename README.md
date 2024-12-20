# America first ? The influence of America in the global cinema

# Website url : https://cbouchiat.github.io/ADACTYLOUS/

# Abstract:
The end of the 19th century witnessed the start of narrative film production, driven by European pioneers like LePrince, the Lumière brothers & Mélies. However, the US American film industry soon took over the lead and the 20th century (1920s-60s) marks the golden age of Hollywood cinema (Radulovich, 2015). By 2009, the United States continued to dominate the worldwide film industry, with the top 20 highest-grossing films worldwide being either American productions or American co-productions (Crane, 2014). This enduring hegemony, that we aim to explore in greater depth, has significantly been influencing filmmaking trends including cast composition. Thus, we would also like to investigate what makes American movies so different and so successful compared to the rest of the world. Beyond production, audiences around the world often prefer American films over locally produced movies, for example in Sydney (Sedgwick et al., 2014). This tendency introduces new cultural paradigms, with an Americanization of local cultures and a diffusion of US soft power, for instance in China (Yan et al., 2024). This raises further questions about the cultural interlinks drawn by movies, between the United States and other nations, which we aim to explore in the present project.


# Research Questions:
In this project, we aim to examine America's influence on global cinema by addressing the following research questions:
1) Are American movies more successful than movies from other production countries ?
2) Does being American favor a successful acting career ?
3) How are geographic locations in the US perceived in movies and to what extent are typical American cultural aspects reflected? 
The corresponding embedded questions are described in the next section 'Methods'.

# Proposed additional datasets
To conduct this project, we are enriching the CMU dataset using additional datasets and queries :
- “IMDB” Dataset : that contains the IMDB ratings, number of votes, simplified movie's genres and attributes that are already present in the movies’ metadata dataset (release year, title and runtime). This dataset is merged with the dataset containing movies' metadata on runtime, release year and movie title attributes. [Link](https://developer.imdb.com/non-commercial-datasets/)

- ”DBpedia scraping” : By iterating over each actor name in the CMU dataset, we performed a SPARQL query to form a new column, “nationality”. The query uses the actor name to access the actor’s DBpedia page and checks whether the abstract contains the word “American”. If ”American” is found, the actor's nationality is set to “American”; otherwise, it is set to “Other”. If an error occurs, generally because the DBpedia page is incomplete, the nationality is set to NaN. With this query, we have a nationality value for all 450 000 actors of the CMU dataset - with 31% NaN. However, this method cannot account for dual nationalities. 
    - Initial input from: [Link](https://tinysubversions.com/notes/how-to-query-wikipedia/)
    - Typical DBpedia actor page: [Link](https://dbpedia.org/page/Frankie_Jonas)

- The datasets used so far do not contain any information about the success of the actors directly. The box office revenue of the movies the actors played in, might not properly represent their individual success. Therefore, another proxy for the success of actors is used, in order to compare American actors and non-Amarican actors to each other. For this purpose, a dataset on Golden Globe Awards for acting achievements is used to approximate the success of actors. The Golden Globe Award was chosen over the Oscar awards since the Oscars are awards originating from the US and might therefore be biased on American actors, which would bias as well the present study. In contrast, the Golden Globes are adjudicated by an international jury, allowing for the assumption that American actors are not given advantage in this award. The dataset contains all nominations for acting achievements ever announced from 1944 to 2020 which are 1743 unique nominees. From the dataset we can derive how often an actor was nominated and if the nomination led to a win or not. Creating from this information a Golden Globes index allows to assess which actors are more successful than others. [Link](https://www.kaggle.com/datasets/unanimad/golden-globe-awards).



# Methods
General :
Movies are categorized as strictly American movies, partially American movies (where the countries of production include the USA but are not limited to it) and movies from all other countries. Indeed, we believed it was interesting to distinguish those three cases (and results have shown that it is), especially in recent years where lots of movies are co-produced. 


Tools : Significance tests will extensively be used to determine the relevance of the observed patterns. Other than that, regression analysis and k-means clustering support the success analysis of actors whereas NLP is used to analyse the plot summaries.

**For research question 1** : 
This research question is answered by using three pillars:
- Exploring the translations of strictly and partially American movies into other languages, and the translations of non-American movies into English in order to assess the importance of the English language. 
- Exploring the box office revenue, the runtime and IMDB ratings : are they significantly higher for American movies than for movies with other countries of production ?
- Creating a Movies Success Index (MSI) from a linear regression fit on IMDb ratings, including parameters like translations, box office and actors to assess, if the success of a movie depends on its country of production

**For research question 2** : 
To answer this research question, the following three components are used: 
- Creating an Actor’s Career Success Index (ACSI), including parameters like the duration of the career, revenue from movies in which she/he acted, and the number of movies acted in. This way, we can evaluate the parameters of a successful actor career and link those with American origin or/and American films
- Examine the age of American and non-American actors at the time of their first movie. Herewith, we explore the following question: Does being American help launch the actor's career
- Investigating the box office revenue of the movies in which each actor acted, and explore whether the first movie in a series of high box-office revenue films is strictly or partially American. This way, we can answer : Does acting in a strictly or partially American movie help launch the actor's career? 

**For research question 3** : This section focuses on the plot summaries of the movies. For each topic, a set of key-words is  created and used to explore their frequencies in the plot summaries.
- The first topic focuses on the inclusion of geographic locations within the US in movie plot summaries. For this purpose, the plot summaries are scanned with a NLP algorithm which detects the words referring to locations in the US. The frequency of these terms compared to the total number of terms appearing in the plot summaries allow for comparison between different movie origins. The results show which movie plots mostly take place in real American places.
- The second topic uses a list of words of typical American terms which accurately represent American culture. The list of words is created by asking ChatGPT for typical American terms. Using this set of words, the plot summaries are scanned and the frequency of the terms appearing is calculated as it was done for the geographic locations above. The results allow us to understand if there is a link between the movies’ origin and the use of American cultural terms in the plot summaries. 


The steps developed above provide the information to assess, how America influences the global cinema and if this influence is visible in movies which are produced in other countries than the US. 


# Contributions of the group members :
- Chloé: Initial data analysis, dataset enrichment with actors nationalities, creation of the website, interpretation of results.
- Claire: Data analysis for movie translations and genres, creation of the movie success index (MSI), plot creation (including interactive plots), interpretation of results.
- Germana: Data analysis of the actors dataset, clustering of the actors, creation of the actor success index, interpretation of results.
- Luca: Data analysis for initial basic statistics and for movie metadata, plot summary analysis with NLP, creation of American lexicon, plot creation, interpretation of results.
- Marlen: Preparation of the Golden Globes dataset and creation of the Golden Globes index. Interpretation of results. Structure, story flow and textual description of the datastory.


# Bibliography
- Crane, D. (2014): European Audiovisual Observatory, 2010. Focus 2009: world film market trends. Cannes: Marché du Film. International Journal of Cultural Policy, 20(4), 365–382, DOI: 10.1080/10286632.2013.832233.
- Radulovich, S. (2015): Classical Hollywood Cinema and Post-Classical Hollywood Cinema; Case Study of Modern and Postmodern Film. Undergraduate thesis, University of Rijeka, Faculty of Humanities and Social Sciences, accessed 15 November 2024, https://urn.nsk.hr/urn:nbn:hr:186:725674
- Sedgwick, J., Pokorny, M. and Miskell, P. (2014): Hollywood in the world market – evidence from Australia in the mid-1930s. Business History, 56(5),  689–723. DOI: 10.1080/00076791.2013.837891.
- Yan, J., Li, N. and Yu, F. (2024): “An empirical study of trade effect on culture” Journal of Applied Economics, 27(1). DOI: 10.1080/15140326.2024.2334551.

# ada-2024-project-adactylous
ada-2024-project-adactylous created by GitHub Classroom
