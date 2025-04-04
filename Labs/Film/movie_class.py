import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances


class movie_recommendation:
    def __init__(self, movie_path, tags_path, links_df):
        self.tag_vector, self.index, self.movies = self.create_matrix(movie_path, tags_path)
        self.links = links_df

    def get_movies(self, movie_list):
        if type(movie_list) == list:
            return self.recommend_movies(self.tag_vector, self.index, movie_list, self.links)
        else:
            raise ValueError('movie_list must be a list')

    def create_matrix(self, m_path, t_path):
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


    def translate(self, index, id, links, get_link=False):
        if get_link:
            urlnum = str(links['imdbId'][index[id]])
            if len(urlnum) != 7:
                diff = 7 - len(urlnum)
                urlnum = diff*'0' + urlnum
            return f'https://www.imdb.com/title/tt{urlnum}'
        else:
            return index.get_loc(id)

    def recommend_movies(self, tag_vector, index, movie_id, links):
        if len(movie_id) > 1:
            matrix_index = self.translate(index, movie_id[0], links)
            serie = pd.Series(euclidean_distances(tag_vector, tag_vector.getrow(matrix_index)).reshape(-1))
            for id in movie_id[1:]:
                matrix_index = self.translate(index, id, links)
                tmp = pd.Series(euclidean_distances(tag_vector, tag_vector.getrow(matrix_index)).reshape(-1))
                serie = serie + tmp
            matrix_index = list()
            for id in movie_id:
                matrix_index.append(self.translate(index, id, links))
            serie.drop(index=matrix_index, inplace=True)
            serie = serie.sort_values(ascending=True)
            recommended_movies = serie.iloc[:6]
            
        else:
            matrix_index = self.translate(index, movie_id, links)
            serie = pd.Series(euclidean_distances(tag_vector, tag_vector.getrow(matrix_index)).reshape(-1))
            serie = serie.sort_values(ascending=True)
            recommended_movies = serie.iloc[1:7]
        urls = list()
        for id in recommended_movies.index:
            urls.append(self.translate(index, id, links, get_link=True))
        return urls
    
    def create_ratings(path, movie_index):
        ratings = pd.read_csv(path)
        ratings = ratings.groupby('movieId')['rating'].agg(['count', 'mean'])
        ratings = ratings[ratings['count'] < 25] #Ta bort avvikelser, tex. 1 review som ger 5.0 rating
        ratings = ratings[ratings.index.isin(movie_index)]
        ratings['mean'].to_csv('Labs/Film/ratings.py')





