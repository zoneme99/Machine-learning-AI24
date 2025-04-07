"""
A sample of 8 of the 26 Bootstrap themed Plotly figure templates available
in the dash-bootstrap-template library

"""
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
from movie_class import movie_recommendation
import pandas as pd

df = px.data.gapminder()

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
                            html.Div(id='pics')])


@callback(
    Output('pics', 'children'),
    Input('mov1', 'value'),
    Input('mov2', 'value'))

def update_graph(movie1, movie2):
    

    return f'first movie {movie1} and second movie {movie2}'


if __name__ == "__main__":
    app.run(debug=True)
    #print(movie_obj.get_movies([260, 1196]))
    
