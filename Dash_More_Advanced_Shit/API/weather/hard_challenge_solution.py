# Solution to change your app to show yesterday’s forecast of "mintemp" & “avgtemp” in New York
# Changes made to lines 15,19,37

from datetime import date, timedelta

import pandas as pd  # (version 1.0.0)

import dash  # (version 1.9.1) pip install dash==1.9.1
from dash import dcc, html
from dash.dependencies import Input, Output
import requests

# import sys
# sys.path.append(["/Users/onesixx/my/git/Dash-by-Plotly-1/common"])
# import dconsts
# from common.dconsts import ACCESS_KEY, TODAY, YESTERDAY
ACCESS_KEY = '88ffb416536794b25ea52f6e9a6c6c28'
YESTERDAY = (date.today()-timedelta(1)).isoformat()

app = dash.Dash(__name__)

# -------------------------------------------------------------------------------
categories = ["mintemp", "avgtemp"]
def update_weather():
    url = "http://api.weatherstack.com/forecast?access_key=" + \
        ACCESS_KEY+"&query="+"New%20York"
    df = pd.DataFrame(requests.get(url).json())
    return([
        html.Table([
            html.Tr([
                html.Td([name+": "+str(data)])
            ])
            # make sure to change date
            for name, data in zip(categories, map(df['forecast'][YESTERDAY].get, categories))
        ], className='table-weather')
    ])

    # weather_requests = requests.get(
    #     "http://api.weatherstack.com/forecast?access_key=88ffb416536794b25ea52f6e9a6c6c28&query=New%20York"
    # )
    # weather_requests = requests.get(url)
    # json_data = weather_requests.json()
    # df = pd.DataFrame(json_data)

    # return([
    #     html.Table(
    #         className='table-weather',
    #         children=[
    #             html.Tr(
    #                 children=[
    #                     html.Td(
    #                         children=[
    #                             name+": "+str(data)
    #                         ]
    #                     )
    #                 ]
    #             )
    #             # make sure to change date
    #             for name, data in zip(categories, map(df['forecast'][YESTERDAY].get, categories))
    #         ]
    #     )
    # ])


# -------------------------------------------------------------------------------
app.layout = html.Div([
    dcc.Interval(
        id='my_interval',
        disabled=False,  # if True the counter will no longer update
        n_intervals=0,  # number of times the interval has passed
        interval=300*1000,  # increment the counter n_intervals every 5 minutes
        max_intervals=100,  # number of times the interval will be fired.
        # if -1, then the interval has no limit (the default)
        # and if 0 then the interval stops running.
    ),

    html.Div([
        html.Div(
            id="weather",
            children=update_weather()
        )
    ]),

])

# -------------------------------------------------------------------------------
# Callback to update news


@app.callback(Output("weather", "children"), [Input("my_interval", "n_intervals")])
def update_weather_div(n):
    return update_weather()


# -------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
