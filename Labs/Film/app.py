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
app.layout = dbc.Container([dcc.Dropdown(df.columns, 'gdpPercap', id='xaxis-column'),
                            dcc.Dropdown(df.columns, 'lifeExp', id='yaxis-column'),
                            dcc.Graph(id='graph')])


@callback(
    Output('graph', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'))

def update_graph(xaxis_column_name, yaxis_column_name):
    

    figure = px.scatter(
        df.query("year==2007"),
        x=xaxis_column_name,
        y=yaxis_column_name,
        size="pop",
        color="continent",
        log_x=True,
        size_max=60,
        template=template,
        title="Gapminder 2007: '%s' theme" % template,
    )



    return figure


if __name__ == "__main__":
    #app.run(debug=True)
    movie_obj = movie_recommendation(movies_path, tags_path, links)
    print(movie_obj.get_movies([260, 1196]))
    
