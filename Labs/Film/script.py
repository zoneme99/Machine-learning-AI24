import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from functools import cache
import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.preprocessing import MinMaxScaler, StandardScaler

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
        sparse = hstack([movies, scaled_rating])
        return sparse, refined_ratings.index

    
    def refine_tags(notags):
        tags = pd.read_csv('Labs/Film/ml-latest/tags.csv')
        tags = tags.drop(columns=['userId', 'timestamp'])
        tags = tags.dropna()
        tags['tag'] = tags['tag'].apply(lambda x: str(x))
        grouped_tags = tags.groupby('movieId')['tag'].agg(' '.join)
        print(len(notags.difference(grouped_tags.index)))
        exit()
        vector = TfidfVectorizer()
        tag_vectorized = vector.fit_transform(grouped_tags)
        return tag_vectorized
    
    part1, notags = refine_movies_ratings()
    part2 = refine_tags(notags)
    print(part1.shape, part2.shape)
    exit()
    return hstack([part1, part2])
    
#def model_selection(df):


matrix = create_matrix()
print(matrix)