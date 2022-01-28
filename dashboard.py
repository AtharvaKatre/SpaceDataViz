from dash import Dash, dcc, html, Output, Input, State
import dash_bootstrap_components as dbc

# import dash_table
# import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import math
import os
import base64

# ----------------------------------------------Read Data---------------------------------------------------------------
cwd = os.getcwd() + "/SpaceDataViz"
df = pd.read_csv(cwd + "/assets/dataset.csv")
df["Perigee"] = df["Perigee"].apply(lambda x: int(x.replace(",", "")))
df["Apogee"] = df["Apogee"].apply(lambda x: int(x.replace(",", "")))
df["Semi-Major Axis"] = df["Semi-Major Axis"].apply(lambda x: int(x.replace(",", "")))

logo_raw = os.path.join(cwd, "assets/space.png")
logo = base64.b64encode(open(logo_raw, "rb").read())

# plot functions
def lin_plot(df, x_data):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df[x_data],
            y=df["Apogee"],
            mode="markers",
            name="Apogee",
            marker_color="#c92a52",
            marker_symbol="triangle-down",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df[x_data],
            y=df["Semi-Major Axis"],
            mode="markers",
            name="Semi-Major Axis",
            marker_color="black",
            marker_symbol="x-thin",
            marker_line_width=2,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df[x_data],
            y=df["Perigee"],
            mode="markers",
            name="Perigee",
            marker_color="#4d70c9",
            marker_symbol="triangle-up",
        )
    )

    if x_data == "Period":
        title = "Orbital Period"
        x_title = title + " (minutes)"
    if x_data == "Inclination":
        title = x_data
        x_title = "Inclination (degrees)"
        fig.update_xaxes(
            range=[-20, 180],
            dtick=20,
            tickvals=[None, 0, 20, 40, 60, 80, 100, 120, 140, 160, 180],
            ticktext=[None, 0, 20, 40, 60, 80, 100, 120, 140, 160, 180],
            tickmode="array",
        )

    fig.update_layout(
        title="Space Objects by {}<br>".format(title),
        title_x=0,
        yaxis_title="Altitude (km)",
        xaxis_title=x_title,
        hovermode="closest",
        legend=dict(font=dict(size=12), bordercolor="Black", borderwidth=1),
        margin=dict(t=70, r=0),
        font=dict(family="Arial"),
        height=600,
        template="presentation",
    )
    return fig


def log_plot(df, x_data):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df[x_data],
            y=df["Apogee"],
            mode="markers",
            name="Apogee",
            marker_color="#c92a52",
            marker_symbol="triangle-down",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df[x_data],
            y=df["Semi-Major Axis"],
            mode="markers",
            name="Semi-Major Axis",
            marker_color="black",
            marker_symbol="x-thin",
            marker_line_width=1.3,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df[x_data],
            y=df["Perigee"],
            mode="markers",
            name="Perigee",
            marker_color="#4d70c9",
            marker_symbol="triangle-up",
        )
    )

    fig.add_hrect(
        y0=0,
        y1=2000,
        fillcolor="#EEEEEE",
        opacity=0.5,
        layer="below",
        line_width=0,
    )

    fig.add_hrect(
        y0=2000,
        y1=35786,
        fillcolor="#CCCCCC",
        opacity=0.5,
        layer="below",
        line_width=0,
    )

    fig.add_hline(
        y=35786,
        line_width=2,
        line_dash="dash",
        annotation_text="GEO",
    )

    fig.add_hrect(
        y0=35786,
        y1=999999,
        fillcolor="#999999",
        opacity=0.5,
        layer="below",
        line_width=0,
    )

    if x_data == "Inclination":
        fig.add_annotation(
            x=math.log(0.001),
            y=math.log(15),
            text="LEO",
            font=dict(size=13),
            showarrow=False,
            # xshift=5,
        )

        fig.add_annotation(
            x=math.log(0.001),
            y=math.log(55),
            text="MEO",
            font=dict(size=13),
            showarrow=False,
            # xshift=5,
        )

        fig.add_annotation(
            x=math.log(0.001),
            y=math.log(175),
            text="HEO",
            font=dict(size=13),
            showarrow=False,
            # xshift=5,
        )

        fig.add_annotation(
            x=math.log(0.001),
            y=math.log(85),
            text="<b>GEO",
            font=dict(size=13),
            showarrow=False,
            xshift=475,
        )

        title = x_data
        x_title = "Inclination (degrees)"
        fig.update_xaxes(
            range=[-20, 180],
            dtick=20,
            tickvals=[None, 0, 20, 40, 60, 80, 100, 120, 140, 160, 180],
            ticktext=[None, 0, 20, 40, 60, 80, 100, 120, 140, 160, 180],
            tickmode="array",
        )

    if x_data == "Period":
        fig.add_annotation(
            x=math.log(0.0001),
            y=math.log(15),
            text="LEO",
            font=dict(size=13),
            showarrow=False,
            xshift=0,
        )

        fig.add_annotation(
            x=math.log(0.0001),
            y=math.log(55),
            text="MEO",
            font=dict(size=13),
            showarrow=False,
            xshift=0,
        )

        fig.add_annotation(
            x=math.log(0.0001),
            y=math.log(175),
            text="HEO",
            font=dict(size=13),
            showarrow=False,
            xshift=0,
        )

        fig.add_annotation(
            x=math.log(0.001),
            y=math.log(85),
            text="<b>GEO",
            font=dict(size=13),
            showarrow=False,
            xshift=475,
        )

        title = "Orbital Period"
        x_title = title + " (minutes)"
        fig.update_xaxes(
            range=[-1000, 12000],
            dtick=2000,
            tickvals=[None, 0, 2000, 4000, 6000, 8000, 10000, 12000],
            ticktext=[None, 0, 2000, 4000, 6000, 8000, 1000, 12000],
            tickmode="array",
        )

    fig.update_layout(
        title="Space Objects by {}<br>".format(title),
        title_x=0,
        yaxis_title="Altitude (km) (log)",
        xaxis_title=x_title,
        margin=dict(t=70, r=0, l=120),
        legend=dict(font=dict(size=12), bordercolor="Black", borderwidth=1),
        hovermode="closest",
        font=dict(family="Arial"),
        height=600,
        template="presentation",
    )

    fig.update_yaxes(
        type="log",
        range=[2, 5.8],
        tickvals=[0, 200, 500, 1000, 2000, 10000, 35786, 100000, 300000, 999999],
    )
    return fig


def dummy_plot():
    high = [50000, 30000, 80000]
    mid = [35000, 20000, 55000]
    low = [20000, 10000, 30000]

    x = ["03 JAN 22", "10 JAN 22", "17 JAN 22"]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=high,
            mode="markers",
            name="Apogee",
            marker_color="#c92a52",
            marker_symbol="triangle-down",
            marker_size=8,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=mid,
            mode="markers",
            name="Semi-Major Axis",
            marker_color="black",
            marker_symbol="x-thin",
            marker_line_width=1,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=low,
            mode="markers",
            name="Perigee",
            marker_color="#4d70c9",
            marker_symbol="triangle-up",
            marker_size=8,
        )
    )

    fig.update_layout(
        title="Starlink 1337",
        title_x=0,
        template="presentation",
        xaxis=dict(title="Time", titlefont=dict(size=14), tickfont=dict(size=10)),
        yaxis=dict(
            title="Altitude (km)", titlefont=dict(size=14), tickfont=dict(size=10)
        ),
        height=280,
        margin=dict(t=30, b=50, l=50, r=30),
        font=dict(size=15, family="Arial"),
        showlegend=False,
    )
    return fig


# -----------------------------------------APP Definition---------------------------------------------------------------
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "SpaceData Dashboard"

# -----------------------------------------APP Components-------------------------------------------------------------------
banner = dbc.Row(
    [
        dbc.Col(
            html.H1(
                [
                    html.Span("Space Situational Awareness Dashboard "),
                    html.Span(
                        html.Img(
                            src="data:image/png;base64,{}".format(logo.decode()),
                            height="60",
                        )
                    ),
                ]
            )
        )
    ]
)

side_card_style = {"height": "300px"}
graph_card_style = {"height": "625px"}

# card1 = dbc.Card([], style=side_card_style)

settings_card = dbc.Card(
    [
        html.Div(
            [
                dbc.Row([dbc.Col(html.H4("SETTINGS"))]),
                html.Div(
                    [
                        dbc.Label(html.B("X-Axis")),
                        dbc.RadioItems(
                            options=[
                                {"label": "Inclination", "value": "Inclination"},
                                {"label": "Orbital Period", "value": "Period"},
                            ],
                            value="Inclination",
                            id="xaxis-input",
                        ),
                    ],
                    style={"margin": 10},
                ),
                html.Div(
                    [
                        dbc.Label(html.B("Y-Axis Scale")),
                        dbc.RadioItems(
                            options=[
                                {"label": "Linear", "value": "lin"},
                                {"label": "Log", "value": "log"},
                            ],
                            value="log",
                            inline=True,
                            id="yaxis-input",
                        ),
                    ],
                    style={"margin": 10},
                ),
                html.Div(
                    [
                        dbc.Label(html.B("Search Satellites")),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Input(
                                        id="sat-input",
                                        placeholder="Eg. Starlink",
                                        debounce=True,
                                        style={"width": "100%"},
                                    ),
                                    width=9,
                                ),
                                # dbc.Col(dbc.Button('Search', id='search-button', size='sm')),
                            ]
                        ),
                    ],
                    style={"margin": 10},
                ),
            ],
            style={"margin": 10},
        )
    ],
    style=side_card_style,
)
datasource_card = dbc.Card(
    [
        html.Div(
            [
                dbc.Row([dbc.Col(html.H4("DATASOURCES"))]),
                html.Div(
                    [
                        # dbc.Label("X-Axis"),
                        dbc.RadioItems(
                            options=[
                                {"label": "Datasource A", "value": "1"},
                                {"label": "Datasource B", "value": "2"},
                                {"label": "Datasource C", "value": "3"},
                                {"label": "Own Datasource", "value": "4"},
                            ],
                            value="1",
                            id="datasource-input",
                        ),
                    ],
                    style={"margin": 10},
                ),
            ],
            style={"margin": 10},
        )
    ],
    style=side_card_style,
)

dummygraph_card = dbc.Card(
    [
        html.Div(
            dcc.Loading(
                dcc.Graph(
                    figure=dummy_plot(),
                    config={
                        "displaylogo": False,
                        "modeBarButtonsToAdd": ["v1hovermode", "toggleSpikeLines"],
                    },
                )
            ),
            style={"margin": 10},
        )
    ],
    style=side_card_style,
)

details_card = dbc.Card(
    [
        html.Div(
            [
                dbc.Row([dbc.Col(html.H4("DETAILS"))]),
                html.Div(
                    [
                        dbc.Row(dbc.Col(html.P("Information 1"))),
                        dbc.Row(dbc.Col(html.P("Information 2"))),
                        dbc.Row(dbc.Col(html.P("Information 3"))),
                        dbc.Row(dbc.Col(html.P("Information 4"))),
                        dbc.Row(dbc.Col(html.P("Information 5"))),
                        dbc.Row(dbc.Col(html.P("Information 6"))),
                    ],
                    style={"margin": 10},
                ),
            ],
            style={"margin": 10},
        )
    ],
    style=side_card_style,
)

graph_card1 = dbc.Card(
    [
        html.Div(
            dcc.Loading(
                dcc.Graph(
                    id="graph1",
                    config={
                        "displaylogo": False,
                        "modeBarButtonsToAdd": ["v1hovermode", "toggleSpikeLines"],
                    },
                )
            ),
            style={"margin": 10},
        )
    ],
    style=graph_card_style,
)

row1 = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Row([dbc.Col(settings_card)]),
                html.Br(),
                dbc.Row([dbc.Col(datasource_card)]),
            ]
        ),
        dbc.Col(graph_card1, width=7),
        dbc.Col(
            [
                dbc.Row([dbc.Col(dummygraph_card)]),
                html.Br(),
                dbc.Row([dbc.Col(details_card)]),
            ]
        ),
    ]
)

# -----------------------------------------APP Layout-------------------------------------------------------------------
app.layout = dbc.Container(
    [
        html.Br(),
        banner,
        html.Br(),
        row1,
    ],
    fluid=True,
    style={"font-family": "Arial", "width": "95%"},
)

# -----------------------------------------App Callback-----------------------------------------------------------------

# plot xaxis callback
@app.callback(
    Output("graph1", "figure"),
    Input("xaxis-input", "value"),
    Input("yaxis-input", "value"),
    Input("sat-input", "value"),
    # Input("search-button", "n_clicks")
)
def update_graph(xaxis_data, y_type, sat_name):
    if sat_name is not None:
        dff = df[df["Satellite Name"].str.lower().str.contains(sat_name.lower())]
        if y_type == "log":
            return log_plot(dff, xaxis_data)
        if y_type == "lin":
            return lin_plot(dff, xaxis_data)
    else:
        if y_type == "log":
            return log_plot(df, xaxis_data)
        if y_type == "lin":
            return lin_plot(df, xaxis_data)


# -----------------------------------------Run Server-------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
