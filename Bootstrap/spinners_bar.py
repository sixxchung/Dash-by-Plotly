import dash  # pip install dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
# pip install dash-bootstrap-components
import dash_bootstrap_components as dbc
import pandas as pd  # pip install pandas

# https://drive.google.com/file/d/1Srm_mhf6oRb6R5kFijFzaZk6tye9Ugb0/view
df = pd.read_csv("green_tripdata_2019-01.csv")
df = df[df["total_amount"] > 0]
df = df[:150000]

# https://bootswatch.com/default/ for more themes
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

app.layout = html.Div(
    children=[
        dbc.Row(dbc.Col(
            dbc.Spinner(children=[dcc.Graph(id="loading-output")],
                        size="lg", color="primary", type="border", fullscreen=True,),
            # spinner_style={"width": "10rem", "height": "10rem"}),
            # spinnerClassName="spinner"),
            # dcc.Loading(children=[dcc.Graph(id="loading-output")], color="#119DFF", type="dot", fullscreen=True,),

            width={'size': 12, 'offset': 0}),
        ),

        dbc.Row([
            dbc.Col(dbc.Input(id="passenger_count", type="number", min=1, max=6, step=1, value=1),
                    width={'size': 2, 'offset': 1}),
            dbc.Col(dbc.Button(id="loading-button", n_clicks=0, children=["Passengers"]),
                    width={'size': 1, 'offset': 0})
        ]),  # no_gutters is no longer possible with the new Dash Bootstrap components version upgrade

        html.Br(),
        dbc.Row(dbc.Col(dbc.Progress(children=["25%"], value=25, max=100, striped=True, color="success", style={"height": "20px"}),
                        width={'size': 5, 'offset': 1}),
                ),
    ]
)


@app.callback(
    Output("loading-output", "figure"),
    [Input("loading-button", "n_clicks")], [State("passenger_count", "value")]
)
def load_output(n_clicks, psg_num):
    if n_clicks:
        dff = df[df["passenger_count"] == psg_num]
        fig = px.histogram(
            dff, x="total_amount", title="NYC Green Taxi Rides").update_layout(title_x=0.5)
        return fig
    return px.histogram(df.query(f"passenger_count=={psg_num}"), x="total_amount",
                        title="NYC Green Taxi Rides").update_layout(title_x=0.5)


if __name__ == "__main__":
    app.run_server(debug=True)


# https://youtu.be/t1bKNj021do
