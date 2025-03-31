import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from functools import cache
import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import scipy as sp

@cache
def create_matrix():

    def refine_movies_ratings():
        #Movie refinement
        movies = pd.read_csv('Labs/Film/ml-latest/movies.csv', index_col='movieId')
        df_one_hot = movies['genres'].str.get_dummies(sep='|')
        movies = movies.drop(columns=['genres','title'])
        movies = pd.concat([movies,df_one_hot], axis=1)
        ratings = pd.read_csv('Labs/Film/ml-latest/ratings.csv')
        #Rating refinement
        mask = ratings.groupby('userId').size() > 25
        expert_ratings = ratings[ratings['userId'].isin(mask[mask].index)] # Sorterar bort ej "expert users"
        refined_ratings = expert_ratings.groupby('movieId')['rating'].mean() #Minskar datan genom att ta ett medel för varje film
        movies = movies[movies.index.isin(refined_ratings.index)] # Filtrerar bort alla filmer som inte finns med hos expert users
        S_scaler = StandardScaler()
        rate_array = refined_ratings.array.reshape((-1, 1))
        scaled_rating = S_scaler.fit_transform(rate_array)
        min_scaler = MinMaxScaler()
        scaled_rating = min_scaler.fit_transform(scaled_rating)
        #Konkatinera
        movies = csr_matrix(movies.values)
        return movies, scaled_rating, refined_ratings.index

    
    def refine_tags(ratings):
        tags = pd.read_csv('Labs/Film/ml-latest/tags.csv')
        tags = tags.drop(columns=['userId', 'timestamp'])
        tags = tags.dropna()
        tags['tag'] = tags['tag'].apply(lambda x: str(x))
        grouped_tags = tags.groupby('movieId')['tag'].agg(' '.join)
        tags_ratings = grouped_tags[grouped_tags.index.isin(ratings)] # Filmer med tags och ratings
        no_tag = ratings.difference(tags_ratings.index) # Filmer utan några taggar
        for index in no_tag:
            tags_ratings.loc[index] = '' #Fyller alla filmer med inga taggar till tomma strings, detta för att få lika stor mängd datapunkter i movies och tags (Dock lite beräkningstung, men ska bara köras en gång)
        vector = TfidfVectorizer()
        tag_vectorized = vector.fit_transform(tags_ratings)
        return tag_vectorized
    
    movies, ratings, rating_index = refine_movies_ratings()
    tags = refine_tags(rating_index)
    ratings = csr_matrix(ratings) # alla ska vara csr-matriser
    return hstack([movies, ratings, tags])
    

matrix = create_matrix()
print("Done")
sp.sparse.save_npz('Labs/Film/matrix.npz', matrix)