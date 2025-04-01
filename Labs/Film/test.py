import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

class_index = pd.read_csv('Labs/Film/class_index.csv', index_col=0)
links = pd.read_csv('Labs/Film/ml-latest/links.csv', index_col='movieId')
matrix = sp.sparse.load_npz('Labs/Film/matrix.npz')
# Exempel-DataFrame
def retrieve_recommendations(class_index, links, matrix):


    serie = pd.Series(cosine_similarity(matrix, matrix.getrow(248)).reshape(-1))
    serie = serie.sort_values(ascending=False)
    recommended_movies = serie.iloc[1:6]

    for id in recommended_movies.index:
        urlnum = str(*links['imdbId'].loc[class_index.loc[id]].values)
        if len(urlnum) != 7:
            diff = 7 - len(urlnum)
            urlnum = diff*'0' + urlnum
        print(f'https://www.imdb.com/title/tt{urlnum}')

#retrieve_recommendations()

print(matrix.getrow(0))