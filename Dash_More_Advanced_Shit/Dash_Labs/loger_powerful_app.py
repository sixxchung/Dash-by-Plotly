# pip istall dash THIS CODE WAS CREATED BY ANN W. AND SLIGHTLY ALTERED BY ME
import dash
import dash_labs as dl  # pip install -U dash-labs
from dash import dcc
import plotly.express as px
import dash_bootstrap_components as dbc
# pip install -U dash-bootstrap-components spectra colormath requests tinycss2

# Choose the app's layout template ***************************************
# Templates list: FlatDiv, HtmlCard, DbcCard, DbcRow, DbcSidebar, DbcSidebarTabs, https://github.com/plotly/dash-labs/blob/main/docs/04-PredefinedTemplates.md
tpl = dl.templates.DbcSidebar(
    # tab_roles=["line","histogram"], # only used for DbcSidebarTabs to define tabs
    title="Dash App Demo",
    sidebar_columns=3,
    # change theme: https://hellodash.pythonanywhere.com/dash_labs
    theme=dbc.themes.COSMO,
    figure_template=True,       # aligns plotly.py figure template with bootstrap theme
)

app = dash.Dash(__name__, plugins=[dl.plugins.FlexibleCallbacks()])

df = px.data.gapminder()
print(df.head())

# Create the app components **********************************************
dropdown = dcc.Dropdown(
    options=[{"label": str(i), "value": i}
             for i in ["gdpPercap", "lifeExp", "pop"]],
    value="gdpPercap",
    clearable=False,
)

checklist = dbc.Checklist(
    options=[{"label": i, "value": i} for i in df.continent.unique()],
    value=df.continent.unique()[1:],
    inline=True,
)

yrs = df.year.unique()
range_slider = dcc.RangeSlider(
    min=yrs[0],
    max=yrs[-1],
    step=5,
    marks={int(i): str(i) for i in [1952, 1962, 1972, 1982, 1992, 2007]},
    value=[1982, yrs[-1]],
)


# Create interaction between app components ******************************
@app.callback(
    inputs=dict(
        indicator=dl.Input(
            dropdown, label="Select indicator (y-axis)", component_property="value"),
        continents=dl.Input(
            checklist, label="Select continents", component_property="value"),
        years=dl.Input(range_slider, label="Select time period",
                       component_property="value"),
    ),
    output=dict(
        div_content=tpl.div_output(
            component_property="children", role="output"),
        # div_content2=tpl.div_output(component_property="children", role="histogram"),
    ),
    template=tpl,
)
def update_charts(years, indicator, continents):
    if continents == []:
        return {}

    dff = df[df.year.between(years[0], years[1])]
    dff = dff[dff.continent.isin(continents)]
    line_fig = px.line(
        dff,
        x="year",
        y=indicator,
        color="continent",
        line_group="country",
        title=indicator + " from %.0f to %.0f" % (years[0], years[1]),
    )

    dff = dff[dff.year == years[1]]

    hist_fig = px.histogram(
        dff, x="lifeExp", nbins=10, title=f"Life Expectancy {years[1]}")

    return dict(
        div_content=[
            dbc.Row([
                dbc.Col(dcc.Graph(figure=line_fig), width=6),
                dbc.Col(dcc.Graph(figure=hist_fig), width=6),
            ])
        ]
        # div_content=dcc.Graph(figure=line_fig),
        # div_content2=dcc.Graph(figure=hist_fig)
    )


app.layout = tpl.layout(app)


if __name__ == "__main__":
    app.run_server(debug=True)
