"""
A sample of 8 of the 26 Bootstrap themed Plotly figure templates available
in the dash-bootstrap-template library

"""
from dash import Dash, html, dcc, Input, Output, State, callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from movie_class import movie_recommendation, get_imdb_image
import pandas as pd


movies_path = 'Labs/Film/ml-latest/movies.csv'
tags_path = 'Labs/Film/ml-latest/tags.csv'
links = pd.read_csv('Labs/Film/ml-latest/links.csv', index_col='movieId')
movie_obj = movie_recommendation(movies_path, tags_path, links)
ratings = pd.read_csv('Labs/Film/ratings.csv', index_col='movieId')

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
app = Dash(__name__, external_stylesheets=[dbc.themes.PULSE])

#Layout för appen
app.layout = dbc.Container([dcc.Markdown(f'''
                                         # Submit your favourite movies from 1 to 5 movies!
                                         
                                        ## AI will recommend movies based of those movies!
                                         - Write in dropdown menu to get available movies
                                         - Filter movies by choosing comparison symbol and prefered rating from {ratings['mean'].min():.2f} to {ratings['mean'].max():.2f}
                                         - Symbols: ALL - all movies considered, < - less than rating number, > - greater than rating number
                                         - Rating number: Any decimal number between interval'''),
                            dcc.Dropdown(id='mov1'),
                            dcc.Dropdown(id='mov2'),
                            dcc.Dropdown(id='mov3'),
                            dcc.Dropdown(id='mov4'),
                            dcc.Dropdown(id='mov5'),
                            html.Div(
                            [dcc.Dropdown(
                                id='comparison-dropdown',
                                options=[
                                    {'label': '<', 'value': '<'},
                                    {'label': '>', 'value': '>'},
                                    {'label': 'ALL', 'value': 'ALL'}
                                ],
                                value='ALL',
                                clearable=False,
                                style={'width': '80px'}
                            ),
                            dcc.Input(
                                id='number-input',
                                type='number',
                                min=ratings.min().iloc[0],
                                max=ratings.max().iloc[0],
                                value = 3,
                                style={'marginLeft': '10px', 'width': '60px'}
                            ),
                            html.Button('Submit', id='submit-val', n_clicks=0)], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px'}),
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

#Har callback-funktioner för varje searchbar. Anledningen är pga optimering. Att ladda in alla alternativ i alla searchbars var beräkningstungt.
#Därför uppdateras valen utefter vad du skriver in vilket minskar antalet alternativ drastiskt.
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

#En input button med State-data från filmtitlar och rating-värden, output: bilder och länkar
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
    State('mov5', 'value'),
    State('comparison-dropdown', 'value'),
    State('number-input', 'value'))

def print_movies(placeholder, movie1, movie2, movie3, movie4, movie5, compare, rating):
    titles = [movie1, movie2, movie3, movie4, movie5]

    #Enkel switch som filtrerar ratings.index
    match compare:
        case 'ALL':
            rate_index = ratings.index
        case '<': #less than
            rate_index = ratings[ratings['mean'] < rating].index
        case '>': #more than
            rate_index = ratings[ratings['mean'] > rating].index

    ids = list()
    #Omvandlar titlar till movieId, hoppar över om det är ett None värde
    for title in titles:
        if title != None:
            ids.append(movie_obj.movies[movie_obj.movies['title'] == title].index[0])
        else:
            continue
    
    #Kollar att ids är inte är tom, annars spottar den ut en tom lista
    if len(ids) > 0:
        urls = movie_obj.get_movies(ids, rate_index)
    else:
        urls = [None, None, None, None, None]

        
    #Returnerar alla bilder och länkar
    return get_imdb_image(urls[0]), get_imdb_image(urls[1]), get_imdb_image(urls[2]), get_imdb_image(urls[3]), get_imdb_image(urls[4]), urls[0], urls[1], urls[2], urls[3], urls[4]


if __name__ == "__main__":
    app.run()
