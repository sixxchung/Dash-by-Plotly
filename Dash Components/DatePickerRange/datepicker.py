from datetime import datetime as dt
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd

# Data from NYC Open Data portal
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Dash%20Components/DatePickerRange/Sidewalk_Caf__Licenses_and_Applications.csv")
df['SUBMIT_DATE'] = pd.to_datetime(df['SUBMIT_DATE'])
df.set_index('SUBMIT_DATE', inplace=True)
print(df[:5][['BUSINESS_NAME', 'LATITUDE', 'LONGITUDE', 'APP_SQ_FT']])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.DatePickerRange(
        id='my-date-picker-range',  # ID to be used for callback
        calendar_orientation='horizontal',  # vertical or horizontal
        day_size=39,  # size of calendar image. Default is 39
        end_date_placeholder_text="Return",  # text that appears when no end date chosen
        with_portal=False,  # if True calendar will open in a full screen overlay portal
        first_day_of_week=0,  # Display of calendar when open (0 = Sunday)
        reopen_calendar_on_clear=True,
        is_RTL=False,  # True or False for direction of calendar
        clearable=True,  # whether or not the user can clear the dropdown
        number_of_months_shown=1,  # number of months shown when calendar is open
        # minimum date allowed on the DatePickerRange component
        min_date_allowed=dt(2018, 1, 1),
        # maximum date allowed on the DatePickerRange component
        max_date_allowed=dt(2020, 6, 20),
        # the month initially presented when the user opens the calendar
        initial_visible_month=dt(2020, 5, 1),
        start_date=dt(2018, 8, 7).date(),
        end_date=dt(2020, 5, 15).date(),
        # how selected dates are displayed in the DatePickerRange component.
        display_format='MMM Do, YY',
        # how calendar headers are displayed when the calendar is opened.
        month_format='MMMM, YYYY',
        minimum_nights=2,  # minimum number of days between start and end date

        persistence=True,
        persisted_props=['start_date'],
        persistence_type='session',  # session, local, or memory. Default is 'local'

        updatemode='singledate'  # singledate or bothdates. Determines when callback is triggered
    ),

    html.H3("Sidewalk Café Licenses and Applications",
            style={'textAlign': 'center'}),
    dcc.Graph(id='mymap')
])


@app.callback(
    Output('mymap', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)
def update_output(start_date, end_date):
    # print("Start date: " + start_date)
    # print("End date: " + end_date)
    dff = df.loc[start_date:end_date]
    # print(dff[:5])

    fig = px.density_mapbox(dff, lat='LATITUDE', lon='LONGITUDE', z='APP_SQ_FT', radius=13, zoom=10, height=650,
                            center=dict(lat=40.751418, lon=-73.963878), mapbox_style="carto-positron",
                            hover_data={'BUSINESS_NAME': True, 'LATITUDE': False, 'LONGITUDE': False,
                                        'APP_SQ_FT': True})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False)


# https://youtu.be/5uwxoxaPD8M
