import os
from load_data import StockDataAPI, StockDataLocal
import dash
from dash import html, dcc
from dash.dependencies import Output, Input
import plotly_express as px
from dateutil.relativedelta import relativedelta

path = os.path.join(os.path.dirname(__file__), "../../Data/Stocksdata")

# api_key = os.getenv("ALPHA_API_KEY")
# stock_data = StockDataAPI(api_key)
stock_data = StockDataLocal(path)
stock_dict = {"AAPL": "Apple", "NVDA": "Nvidia", "TSLA": "Tesla", "IBM": "IBM"}

df_dict = {symbol: stock_data.get_dataframe(symbol) for symbol in stock_dict}

stock_options = [{"label": name, "value": symbol}
                 for symbol, name in stock_dict.items()]
app = dash.Dash(__name__)

ohlc_options = [{"label": option.capitalize(), "value": option}
                for option in ["open", "high", "low", "close"]]

slider_marks = {i: mark for i, mark in enumerate(
    ["1 day", "1 week", "3 months", "1 year", "5 years", "MAX"])}

app.layout = html.Div([
    html.H1("Stocks viewer"),
    html.P("Choose a stock"),
    dcc.Dropdown(id='stock-picker-dropdown', className='', options=stock_options,
                 value='AAPL', placeholder="Apple"),
    dcc.RadioItems(id="ohlc-radio", className='',
                   options=ohlc_options,
                   value='close'),
    dcc.Graph(id="stock-graph"),
    dcc.Slider(id='time-slider',
               min=0,
               max=5,
               step=None,
               value=2,
               marks=slider_marks)
])


@app.callback(
    Output("stock-graph", "figure"),
    Input("stock-picker-dropdown", "value"),
    Input("ohlc-radio", "value"),
    Input("time-slider", "value")
)
def update_graph(stock, ohlc, time_index):
    df_daily, df_intraday = df_dict[stock]
    
    df = df_intraday if time_index < 2 else df_daily
    
    days = {i: day for i, day in enumerate([1,7,90,365,365*5])}

    df = df if time_index == 5 else filter_time(df, days=days[time_index])

    fig = px.line(df, x=df.index, y=ohlc, title=stock_dict[stock])
    return fig

def filter_time(df, days=0):
    last_day = df.index[0].date()
    start_day = last_day-relativedelta(days=days)
    df = df.sort_index().loc[start_day:last_day]
    return df

if __name__ == '__main__':
    app.run_server(debug=True)
