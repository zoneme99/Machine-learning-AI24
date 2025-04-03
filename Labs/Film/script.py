from functools import cache
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

movies_path = 'Labs/Film/ml-latest/movies.csv'
tags_path = 'Labs/Film/ml-latest/tags.csv'
links = pd.read_csv('Labs/Film/ml-latest/links.csv', index_col='movieId')

@cache
def create_matrix(m_path, t_path):
    movies = pd.read_csv(m_path, index_col='movieId')
    tags = pd.read_csv(t_path)
    #Städar taggarna
    tags = tags.drop(columns=['userId', 'timestamp'])
    tags = tags.dropna()
    tags = tags.drop_duplicates('tag')
    tags['tag'] = tags['tag'].apply(lambda x: str(x))
    grouped_tags = tags.groupby('movieId')['tag'].agg(' '.join)
    #Städar movies genres
    movies = movies[movies.index.isin(grouped_tags.index)]
    movies['genres'] = movies['genres'].apply(lambda x: x.replace('|', " "))
    #Konkatinera genres och taggar
    all_tags = movies['genres'] + ' ' + grouped_tags
    #Skapar och output blir en TFIDF-Vektor
    vector = TfidfVectorizer()
    tag_vector = vector.fit_transform(all_tags)
    return tag_vector, all_tags.index, movies

def translate(index, id, links, get_link=False):
    if get_link:
        urlnum = str(links['imdbId'][index[id]])
        if len(urlnum) != 7:
            diff = 7 - len(urlnum)
            urlnum = diff*'0' + urlnum
        print(f'https://www.imdb.com/title/tt{urlnum}')
    else:
        return index.get_loc(id)

def recommend_movies(tag_vector, index, movie_id, links):
    print(index.index(movie_id))
    exit()
    matrix = np.asarray(tag_vector.todense())
    serie = pd.Series(cosine_similarity(matrix, matrix[index.loc[movie_id]]).reshape(-1))
    serie = serie.sort_values(ascending=False)

    recommended_movies = serie.iloc[1:6]
    for id in recommended_movies.index:
        urlnum = str(*links['imdbId'].loc[index.loc[id]].values)
        if len(urlnum) != 7:
            diff = 7 - len(urlnum)
            urlnum = diff*'0' + urlnum
        print(f'https://www.imdb.com/title/tt{urlnum}')
    #257 new hope, 1166 empire strikes back

tag_vector, index, movies = create_matrix(movies_path,tags_path)
movie_id = 260 #New Hope
#recommend_movies(tag_vector, index, movie_id, links)
id_index = translate(index, movie_id, links)
translate(index, id_index, links, get_link=True)
#förväntat 0076759




