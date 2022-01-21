from dash import Dash, dcc, html, Output, Input, State
import dash_bootstrap_components as dbc

# import dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ----------------------------------------------Read Data---------------------------------------------------------------
df = pd.read_csv("assets/dataset.csv")
df["Perigee"] = df["Perigee"].apply(lambda x: int(x.replace(",", "")))
df["Apogee"] = df["Apogee"].apply(lambda x: int(x.replace(",", "")))
df["Semi-Major Axis"] = df["Semi-Major Axis"].apply(lambda x: int(x.replace(",", "")))


def plot(x_data):
    if x_data == "Period":
        title = "Orbital Period"
        x_title = title
    if x_data == "Inclination":
        title = x_data
        x_title = "Inclination (degrees)"

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

    fig.update_layout(
        title="Space Objects by {}<br>".format(title),
        # title_font=dict(size=20),
        # title_y=0.95,
        title_x=0,
        yaxis_title="Altitude (km)",
        xaxis_title=x_title,
        hovermode="closest",
        legend=dict(
            font=dict(size=12),
            # orientation="h",
            # yanchor="bottom",
            # y=1, xanchor="right", x=1.1,
            bordercolor="Black",
            borderwidth=1
            ),
        margin=dict(t=70,r=0),
        font=dict(family='Arial'),
        height=600,
        template="presentation",
    )
    return fig

def dummy_plot():
    high = [50000, 30000, 80000]
    mid = [35000, 20000, 55000]
    low = [20000, 10000, 30000]

    x = ["03 JAN 22", "10 JAN 22", "17 JAN 22"]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=x, y=high, mode='markers', name='Apogee', marker_color='#c92a52', marker_symbol='triangle-down',
                   marker_size=8))
    fig.add_trace(
        go.Scatter(x=x, y=mid, mode='markers', name='Semi-Major Axis', marker_color='black', marker_symbol='x-thin',
                   marker_line_width=1))
    fig.add_trace(
        go.Scatter(x=x, y=low, mode='markers', name='Perigee', marker_color='#4d70c9', marker_symbol='triangle-up',
                   marker_size=8))

    fig.update_layout(title='Starlink 1337', title_x=0, template='presentation', xaxis=dict(title='Time', titlefont=dict(size=14), tickfont=dict(size=10)), yaxis=dict(title='Altitude (km)', titlefont=dict(size=14), tickfont=dict(size=10)),
                      height=280, margin=dict(t=30,b=50,l=50,r=30), font=dict(size=15, family='Arial'), showlegend=False)
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
app.title = "Dashboard"

# -----------------------------------------APP Components-------------------------------------------------------------------
banner = dbc.Row([
    dbc.Col(html.H1([html.Span('Space Data '), html.Span(className='fas fa-satellite', style={'color':'navy'})]))
])

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
                        dbc.Label(html.B("Select Satellites")),
                        dcc.Dropdown(
                            options=[{"label": "Starlink", "value": "Starlink"}],
                            value='Starlink',
                            multi=True
                        )
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
                        dbc.Row(dbc.Col(html.P('Information 1'))),
                        dbc.Row(dbc.Col(html.P('Information 2'))),
                        dbc.Row(dbc.Col(html.P('Information 3'))),
                        dbc.Row(dbc.Col(html.P('Information 4'))),
                        dbc.Row(dbc.Col(html.P('Information 5'))),
                        dbc.Row(dbc.Col(html.P('Information 6'))),
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
                    id='graph1',
                    figure=plot("Inclination"),
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

#plot xaxis callback
@app.callback(
    Output("graph1", "figure"),
    Input("xaxis-input", "value")
)
def update_graph(xaxis_variable):
    return plot(xaxis_variable)

# -----------------------------------------Run Server-------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
