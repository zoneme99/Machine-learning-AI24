"""
A sample of 8 of the 26 Bootstrap themed Plotly figure templates available
in the dash-bootstrap-template library

"""
from dash import Dash, html, dcc, Input, Output, State, callback
from dash.exceptions import PreventUpdate
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
app.layout = dbc.Container([html.H2(children='Submit your favourite movies from 1 to 5 movies!\n AI will recommend movies based of those movies!(Write in dropdown menu to get available movies)',
                            style={'width': '100%'}),
                            dcc.Dropdown(id='mov1'),
                            dcc.Dropdown(id='mov2'),
                            dcc.Dropdown(id='mov3'),
                            dcc.Dropdown(id='mov4'),
                            dcc.Dropdown(id='mov5'),
                            html.Button('Submit', id='submit-val', n_clicks=0),
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
    Output("mov1", "options"),
    Input('mov1', 'search_value')
)
def update_options1(search_value):
    if not search_value:
        raise PreventUpdate
    return movie_obj.movies[movie_obj.movies['title'].str.contains(search_value, case=False, na=False)]['title']
@callback(
    Output("mov2", "options"),
    Input('mov2', 'search_value')
)
def update_options2(search_value):
    if not search_value:
        raise PreventUpdate
    return movie_obj.movies[movie_obj.movies['title'].str.contains(search_value, case=False, na=False)]['title']
@callback(
    Output("mov3", "options"),
    Input('mov3', 'search_value')
)
def update_options3(search_value):
    if not search_value:
        raise PreventUpdate
    return movie_obj.movies[movie_obj.movies['title'].str.contains(search_value, case=False, na=False)]['title']
@callback(
    Output("mov4", "options"),
    Input('mov4', 'search_value')
)
def update_options4(search_value):
    if not search_value:
        raise PreventUpdate
    return movie_obj.movies[movie_obj.movies['title'].str.contains(search_value, case=False, na=False)]['title']
@callback(
    Output("mov5", "options"),
    Input('mov5', 'search_value')
)
def update_options5(search_value):
    if not search_value:
        raise PreventUpdate
    return movie_obj.movies[movie_obj.movies['title'].str.contains(search_value, case=False, na=False)]['title']

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
    Input('submit-val', 'n_clicks'),
    State('mov1', 'value'),
    State('mov2', 'value'),
    State('mov3', 'value'),
    State('mov4', 'value'),
    State('mov5', 'value'))

def print_movies(placeholder, movie1, movie2, movie3, movie4, movie5):
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
    
