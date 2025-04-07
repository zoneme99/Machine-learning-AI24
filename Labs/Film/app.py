"""
A sample of 8 of the 26 Bootstrap themed Plotly figure templates available
in the dash-bootstrap-template library

"""
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
from movie_class import movie_recommendation, get_imdb_image
import pandas as pd


movies_path = 'Labs/Film/ml-latest/movies.csv'
tags_path = 'Labs/Film/ml-latest/tags.csv'
ratings_path = 'Labs/Film/ml-latest/ratings.csv'
links = pd.read_csv('Labs/Film/ml-latest/links.csv', index_col='movieId')

movie_obj = movie_recommendation(movies_path, tags_path, links)

templates = [
    "bootstrap",
    "minty",
    "pulse",
    "flatly",
    "quartz",
    "cyborg",
    "darkly",
    "vapor",
]
template = 'pulse'

load_figure_template(template)



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([dcc.Dropdown(movie_obj.movies['title'], id='mov1'),
                            dcc.Dropdown(movie_obj.movies['title'], id='mov2'),
                            dcc.Dropdown(movie_obj.movies['title'], id='mov3'),
                            dcc.Dropdown(movie_obj.movies['title'], id='mov4'),
                            dcc.Dropdown(movie_obj.movies['title'], id='mov5'),
                            html.Div([
                                html.Div([
                                    html.Img(id='pic1', style={'height': '300px'}),
                                    html.A("Rang1_länk", id='link1', href="#", target="_blank")
                                ], style={'display': 'inline-block', 'margin': '10px', 'textAlign': 'center'}),
                                html.Div([
                                    html.Img(id='pic2', style={'height': '300px'}),
                                    html.A("Rang2_länk", id='link2', href="#", target="_blank")
                                ], style={'display': 'inline-block', 'margin': '10px', 'textAlign': 'center'}),
                                html.Div([
                                    html.Img(id='pic3', style={'height': '300px'}),
                                    html.A("Rang3_länk", id='link3', href="#", target="_blank")
                                ], style={'display': 'inline-block', 'margin': '10px', 'textAlign': 'center'}),
                                html.Div([
                                    html.Img(id='pic4', style={'height': '300px'}),
                                    html.A("Rang4_länk", id='link4', href="#", target="_blank")
                                ], style={'display': 'inline-block', 'margin': '10px', 'textAlign': 'center'}),
                                html.Div([
                                    html.Img(id='pic5', style={'height': '300px'}),
                                    html.A("Rang5_länk", id='link5', href="#", target="_blank")
                                ], style={'display': 'inline-block', 'margin': '10px', 'textAlign': 'center'}),
                            ])
                        ])


@callback(
    Output('pic1', 'src'),
    Output('pic2', 'src'),
    Output('pic3', 'src'),
    Output('pic4', 'src'),
    Output('pic5', 'src'),
    Output('link1', 'href'),
    Output('link2', 'href'),
    Output('link3', 'href'),
    Output('link4', 'href'),
    Output('link5', 'href'),
    Input('mov1', 'value'),
    Input('mov2', 'value'),
    Input('mov3', 'value'),
    Input('mov4', 'value'),
    Input('mov5', 'value'))

def update_graph(movie1, movie2, movie3, movie4, movie5):
    titles = [movie1, movie2, movie3, movie4, movie5]
    ids = list()
    for title in titles:
        if title != None:
            ids.append(movie_obj.movies[movie_obj.movies['title'] == title].index[0])
        else:
            continue
    
    if len(ids) > 0:
        urls = movie_obj.get_movies(ids)
    else:
        urls = [None, None, None, None, None]

        

    return get_imdb_image(urls[0]), get_imdb_image(urls[1]), get_imdb_image(urls[2]), get_imdb_image(urls[3]), get_imdb_image(urls[4]), urls[0], urls[1], urls[2], urls[3], urls[4]


if __name__ == "__main__":
    app.run(debug=True)
    #print(movie_obj.get_movies([260, 1196]))
    
