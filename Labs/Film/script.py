from functools import cache
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
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
    if len(movie_id) > 1:
        matrix_index = translate(index, movie_id[0], links)
        serie = pd.Series(euclidean_distances(tag_vector, tag_vector.getrow(matrix_index)).reshape(-1))
        for id in movie_id[1:]:
            matrix_index = translate(index, id, links)
            tmp = pd.Series(euclidean_distances(tag_vector, tag_vector.getrow(matrix_index)).reshape(-1))
            serie = serie + tmp
        matrix_index = list()
        for id in movie_id:
            matrix_index.append(translate(index, id, links))
        serie.drop(index=matrix_index, inplace=True)
        serie = serie.sort_values(ascending=True)
        recommended_movies = serie.iloc[:6]
        
    else:
        matrix_index = translate(index, movie_id, links)
        serie = pd.Series(euclidean_distances(tag_vector, tag_vector.getrow(matrix_index)).reshape(-1))
        serie = serie.sort_values(ascending=True)
        recommended_movies = serie.iloc[1:7]
    
    for id in recommended_movies.index:
        translate(index, id, links, get_link=True)


tag_vector, index, movies = create_matrix(movies_path,tags_path)
movie_id = [260,1196,122886] #New Hope, empire, force awakens
recommend_movies(tag_vector, index, movie_id, links)
#förväntat 0076759




