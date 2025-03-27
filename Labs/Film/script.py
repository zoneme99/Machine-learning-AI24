import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from functools import cache

@cache
def create_df():
    movies = pd.read_csv('Labs/Film/ml-latest/movies.csv')
    df_one_hot = movies['genres'].str.get_dummies(sep='|')
    movies = movies.drop(columns='genres')
    df = pd.concat([movies,df_one_hot], axis=1)
    
    tags = pd.read_csv('Labs/Film/ml-latest/tags.csv')
    print(tags['tag'].shape)
    tags = tags.dropna()
    vector = TfidfVectorizer()
    tag_vectorized = vector.fit_transform(tags['tag'])

    #tfidf_df = pd.DataFrame(tag_vectorized.toarray(), columns=vector.get_feature_names_out())
    #print(tfidf_df)
    return tag_vectorized
#def model_selection(df):


df = create_df()
print(df.data)