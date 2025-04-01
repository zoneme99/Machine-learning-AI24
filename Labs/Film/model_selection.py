from sklearn.model_selection import GridSearchCV
import scipy as sp
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
matrix = sp.sparse.load_npz('Labs/Film/matrix.npz')

def model_selection(matrix):
    y = [movieId for movieId in range(matrix.shape[0])] #indexet är filmen och klassen
    # Jag gör ingen train_test_split, overfittar datan istället eftersom jag jobbar med samma data och vill endast hitta största likhet
    def grid_search(X, y):
        pipe = Pipeline([('Regressor', KNeighborsClassifier())])

        params = [
    {
        'Regressor' : [KNeighborsClassifier()],
        'Regressor__metric': ['minkowski', 'cosine'],
        'Regressor__n_neighbors': [3,5,25]
    },
    {
        'Regressor' : [LogisticRegression()],
        'Regressor__C' : [0.1,1,1.5]
    },
    {
        'Regressor' : [RandomForestClassifier()],
        'Regressor__criterion' : ['gini', 'entropy']
    }
        ]

        grid_search = GridSearchCV(pipe, params, scoring = 'accuracy', cv=1, verbose = 2, n_jobs= -1) # Eftersom jag har många klasser med få observationer så stänger jag av crossvalidation (cv=1) men testar bästa parametrar
        grid_search.fit(matrix, y)
        return grid_search.cv_results_

    score = grid_search(matrix, y)
    result = pd.DataFrame(score)
    result.to_csv('Labs/Film/estimators.csv')
    
model_selection(matrix)
