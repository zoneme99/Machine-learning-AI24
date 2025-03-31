import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
# Exempel-DataFrame

# Direkt modifiering av underliggande NumPy-array (snabbare än loc)


#movies = pd.read_csv('Labs/Film/ml-latest/movies.csv', index_col='movieId')
#ratings = pd.read_csv('Labs/Film/ml-latest/ratings.csv', index_col='movieId')
tags = pd.read_csv('Labs/Film/ml-latest/tags.csv', index_col='movieId')
matrix = sp.sparse.load_npz('Labs/Film/matrix.npz',)
#row = matrix.indptr
#col = matrix.indices
#data = matrix.data
woody = tags.loc[1]
#woody.hist()
#plt.show()
print(woody.groupby('tag').size())

def test():
    row = matrix.toarray()[1]
    count = 0
    for num in row:
        if num != 0:
            count += 1
    print(count)