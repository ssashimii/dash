import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

df = pd.read_csv("covid_19_filtered.csv")
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
df.sort_values("Date", inplace=True)


app = dash.Dash(__name__)
server = app.server


app.title = "COVID-19 ANALYTICS"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Covid-19 analytics", className="header-title"
                ),
                html.P(
                    children="statistisc between 01.22.2020 and 07.27.2020",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Country/Region", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in np.sort(df.Region.unique())
                            ],
                            value="Afghanistan",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=df.Date.min().date(),
                            max_date_allowed=df.Date.max().date(),
                            start_date=df.Date.min().date(),
                            end_date=df.Date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="confirmed-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="deaths-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="recovered-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    [Output("confirmed-chart", "figure"), Output("deaths-chart", "figure"), Output("recovered-chart", "figure"),],
    [
        Input("region-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(region, start_date, end_date):
    mask = (
        (df.Region == region)
        & (df.Date >= start_date)
        & (df.Date <= end_date)
    )

    filtered_df = df.loc[mask, :]
    confirmed_chart_figure = {
        "data": [
            {
                "x": filtered_df["Date"],
                "y": filtered_df["Confirmed"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "COVID-19 Confirmed",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#000000"],
        },
    }

    deaths_chart_figure = {
        "data": [
            {
                "x": filtered_df["Date"],
                "y": filtered_df["Deaths"],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "COVID-19 Deaths",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }

    recovered_chart_figure = {
        "data": [
            {
                "x": filtered_df["Date"],
                "y": filtered_df["Recovered"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "COVID-19 Recovered", 
            "x": 0.05, 
            "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
    return confirmed_chart_figure, deaths_chart_figure, recovered_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)