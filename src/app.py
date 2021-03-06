from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import locale
import altair as alt
import datetime
import pandas as pd
from utility import get_data, filter_data
import plotly.graph_objects as go
import plotly_express as px
from datetime import datetime

### App setup codes

alt.data_transformers.disable_max_rows()

df = get_data()
daterange = [x for x in range(len(df["date"].unique()))]
month_index = pd.date_range(
    start=df["date"].dt.date.unique()[0], end=df["date"].dt.date.unique()[-1], freq="2M"
)
month_index = month_index - pd.offsets.MonthBegin()

marks = {
    numd: date.strftime("%Y-%m-%d")
    for numd, date in zip(daterange, df["date"].dt.date.unique())
}

marks_display = {}
marks_display.update(
    {
        0: {
            "label": datetime.strptime(marks.get(0), "%Y-%m-%d").strftime("%y/%m"),
            "style": {
                "color": "#77b0b1",
            },
        }
    }
)

last_index = len(marks) - 1

for key, item in marks.items():
    if key != 0 and item in month_index and last_index - key > 30 and key - 0 > 10:
        marks_display.update(
            {
                key: {
                    "label": datetime.strptime(item, "%Y-%m-%d").strftime("%y/%m"),
                    "style": {
                        "color": "#77b0b1",
                    },
                }
            }
        )


marks_display.update(
    {
        last_index: {
            "label": datetime.strptime(marks.get(last_index), "%Y-%m-%d").strftime(
                "%y/%m"
            ),
            "style": {
                "color": "#77b0b1",
            },
        }
    }
)

### App setup codes end

### Selection modules

feature_dropdown = dcc.Dropdown(
    id="feature_dropdown",
    value="new_cases_per_million",
    options=[
        {"label": "Total confirmed cases", "value": "total_cases"},
        {
            "label": "Total confirmed cases per million people",
            "value": "total_cases_per_million",
        },
        {"label": "Daily confirmed cases", "value": "new_cases"},
        {
            "label": "Daily confirmed cases per million people",
            "value": "new_cases_per_million",
        },
        {"label": "Total deaths", "value": "total_deaths"},
        {
            "label": "Total deaths per million people",
            "value": "total_deaths_per_million",
        },
        {"label": "Daily deaths", "value": "new_deaths"},
        {"label": "Daily deaths per million people", "value": "new_deaths_per_million"},
    ],
    style={
        "height": "40px",
    },
)


feature_dropdown2 = dcc.Dropdown(
    id="feature_dropdown2",
    value="new_cases_per_million",
    options=[
        {"label": "Total confirmed cases", "value": "total_cases"},
        {
            "label": "Total confirmed cases per million people",
            "value": "total_cases_per_million",
        },
        {"label": "Daily confirmed cases", "value": "new_cases"},
        {
            "label": "Daily confirmed cases per million people",
            "value": "new_cases_per_million",
        },
        {"label": "Total deaths", "value": "total_deaths"},
        {
            "label": "Total deaths per million people",
            "value": "total_deaths_per_million",
        },
        {"label": "Daily deaths", "value": "new_deaths"},
        {"label": "Daily deaths per million people", "value": "new_deaths_per_million"},
    ],
    style={
        "height": "40px",
    },
)

# Date slider
date_slider = dcc.RangeSlider(
    id="date_slider",
    min=daterange[0],
    max=daterange[-1],
    value=[daterange[0], daterange[-1]],
    marks=marks_display,
)

# Data scale radio button for line chart in map tab
scale_map_line_radio = dbc.RadioItems(
    options=[
        {"label": "Linear", "value": "linear"},
        {"label": "Log", "value": "symlog"},
    ],
    value="linear",
    id="scale-map-line-radio",
    inline=True,
)

points_option = dbc.RadioItems(
    options=[
        {"label": "No", "value": False},
        {"label": "Yes", "value": True},
    ],
    value=False,
    id="points_option",
    inline=True,
)


# Data scale radio button for line charts in Charts tab
scale_charts_radio = dbc.RadioItems(
    options=[
        {"label": "Linear", "value": "linear"},
        {"label": "Log", "value": "symlog"},
    ],
    value="linear",
    id="scale-charts-radio",
    inline=True,
)

# Country selector
country_selector = dcc.Dropdown(
    id="country-selector",
    multi=True,
    options=[{"label": x, "value": x} for x in df.location.sort_values().unique()],
    value=["Canada", "United States", "United Kingdom", "France", "Singapore"],
)

### Selection module ends

### Side bars and Tabs

# Sidebar
sidebar = dbc.Col(
    dbc.Row(
        [
            html.Br(),
            html.P(" "),
            html.P(" "),
            html.H3(
                "World COVID-19 Dashboard",
                style={
                    "font": "Helvetica",
                    "font-size": "28px",
                    "text-align": "center",
                },
            ),
            html.P(" "),
            html.Br(),
            html.P(
                "Explore the global situation of COVID-19 using this interactive dashboard. Compare selected countries and indicators across different date ranges to observe the effect of policy, and vaccination rate.",
                style={"text-align": "left"},
            ),
            html.Hr(),
            html.Br(),
            html.B(
                [
                    "Country Filter ",
                    html.Span(
                        "(?)",
                        id="tooltip-target-country",
                        style={
                            "textDecoration": "underline",
                            "cursor": "pointer",
                            "font-size": "10px",
                            "vertical-align": "top",
                        },
                    ),
                ]
            ),
            dbc.Tooltip(
                "Use this filter to add or remove a country from the analysis. If there are no countries selected, it returns data for all countries",
                target="tooltip-target-country",
            ),
            html.Br(),
            html.Br(),
            country_selector,
            html.Hr(),
            html.Br(),
            html.Hr(),
            html.B("Data Source"),
            html.P(" "),
            html.P(
                "The World COVID-19 Dashboard uses a colection of COVID-19 data maintained by Our World in Data",
                style={"text-align": "left", "font-size": "15px"},
            ),
            html.Div(
                [
                    dcc.Markdown(
                        """
                    Data source can be found [here](https://github.com/owid/covid-19-data/tree/master/public/data).
                    """
                    ),
                ],
                style={"text-align": "left", "font-size": "15px"},
            ),
            html.Div(
                [
                    dcc.Markdown(
                        """
                    Source code can be found [here](https://github.com/UBC-MDS/group10-worldcovid-dashpython).
                    """
                    ),
                ],
                style={"text-align": "left", "font-size": "15px"},
            ),
        ],
    ),
    width=2,
    style={
        "border-width": "0",
        "backgroundColor": "#d3e9ff",
        # "min-height": "100vh",
        # "min-width": "1300px",
    },
)

# Map Tab
map_tab = (
    dbc.Row(
        [
            html.P(" "),
            html.P(
                "Animated World Map",
                style={"font-size": "25px"},
            ),
            html.P(
                "The map below depicts the selected COVID-19 indicator for the selected countries. Use the play button to animate the timeline of this indicator over the date range selected by the slider above.",
            ),
            html.B(
                [
                    "Indicator ",
                    html.Span(
                        "(?)",
                        id="tooltip-target_3",
                        style={
                            "textDecoration": "underline",
                            "cursor": "pointer",
                            "font-size": "10px",
                            "vertical-align": "top",
                        },
                    ),
                ]
            ),
            dbc.Tooltip(
                "Select an indicator to explore on the map and line plot using the dropdown below.",
                target="tooltip-target_3",
            ),
            html.Br(),
            html.Br(),
            feature_dropdown,
        ]
    ),
    dbc.Row(
        [
            html.P(" "),
            dbc.Col(html.P(" "), width=1),
            dbc.Col(
                dbc.Toast(
                    dcc.Loading(
                        dcc.Graph(
                            id="map_plot",
                            style={"height": "60vh"},
                        ),
                    ),
                    style={"width": "95%"},
                ),
            ),
            html.P(" "),
            html.P(" "),
        ]
    ),
)


# Line Tab
line_tab = dbc.Row(
    [
        html.P(" "),
        html.P(
            "Line Plot",
            style={"font-size": "25px"},
        ),
        html.P(
            "The line plot below depicts the selected COVID-19 indicator for the selected countries over the date range selected by the slider above. Click the legend to highlight particular countries.",
        ),
        html.B(
            [
                "Indicator ",
                html.Span(
                    "(?)",
                    id="tooltip-target_4",
                    style={
                        "textDecoration": "underline",
                        "cursor": "pointer",
                        "font-size": "10px",
                        "vertical-align": "top",
                    },
                ),
            ]
        ),
        dbc.Tooltip(
            "Select an indicator to explore on the map and line plot using the dropdown below.",
            target="tooltip-target_4",
        ),
        feature_dropdown2,
        html.P(" "),
        dbc.Col(
            [
                html.P(
                    " ",
                ),
                html.B(
                    [
                        "Data Scale ",
                        html.Span(
                            "(?)",
                            id="tooltip-target",
                            style={
                                "textDecoration": "underline",
                                "cursor": "pointer",
                                "font-size": "10px",
                                "vertical-align": "top",
                            },
                        ),
                    ]
                ),
                dbc.Tooltip(
                    "Use these buttons to change the data scale. Linear: shows the absolute change in value over time. Log: shows the relative change in value over time.",
                    target="tooltip-target",
                ),
                scale_map_line_radio,
                html.P(
                    " ",
                ),
                html.B(
                    [
                        "Add Points ",
                        html.Span(
                            "(?)",
                            id="tooltip-target_2",
                            style={
                                "textDecoration": "underline",
                                "cursor": "pointer",
                                "font-size": "10px",
                                "vertical-align": "top",
                            },
                        ),
                    ]
                ),
                dbc.Tooltip(
                    "Use these buttons to add specific data points to the plot, in addition to the rolling mean",
                    target="tooltip-target_2",
                ),
                points_option,
            ],
            width=2,
        ),
        dbc.Col(
            dbc.Toast(
                dcc.Loading(
                    html.Iframe(
                        id="line_chart",
                        style={
                            "height": "70vh",
                            "width": "100%",
                            "textAlign": "center",
                        },
                    ),
                ),
                style={"height": "550px", "width": "950px"},
            ),
            style={"height": "600px"},
        ),
    ]
)


# Charts Tab
charts_tab = (
    dbc.Row(
        [
            html.P(" "),
            html.B(
                [
                    "Data Scale ",
                    html.Span(
                        "(?)",
                        id="tooltip-target-line",
                        style={
                            "textDecoration": "underline",
                            "cursor": "pointer",
                            "font-size": "10px",
                            "vertical-align": "top",
                        },
                    ),
                ]
            ),
            dbc.Tooltip(
                "Use these buttons to change the data scale. Linear: shows the absolute change in value over time. Log: shows the relative change in value over time.",
                target="tooltip-target-line",
            ),
            html.Br(),
            scale_charts_radio,
            html.P(" "),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.P(
                                "Total Vaccinations",
                                style={"font-size": "25px"},
                            ),
                            html.P(
                                "Shows the total number of people vaccinated for the selected countries, over the date range selected by the slider above.",
                            ),
                            dbc.Toast(
                                dcc.Loading(
                                    html.Iframe(
                                        id="chart_1",
                                        style={
                                            "display": "block",
                                            "overflow": " hidden",
                                            # "margin": "auto",
                                            "border-width": "0",
                                            "width": "550px",
                                            "height": "500px",
                                        },
                                    ),
                                ),
                                style={"width": "550px", "height": "480px"},
                            ),
                        ],
                        #    width=5,
                    ),
                    dbc.Col(
                        [
                            html.P(
                                "New Vaccinations",
                                style={"font-size": "25px"},
                            ),
                            html.P(
                                "Shows the number of people newly vaccinated for the selected countries, over the date range selected by the slider above.",
                            ),
                            dbc.Toast(
                                dcc.Loading(
                                    html.Iframe(
                                        id="chart_2",
                                        style={
                                            "display": "block",
                                            "overflow": " hidden",
                                            # "margin": "auto",
                                            "border-width": "0",
                                            "width": "550px",
                                            "height": "500px",
                                        },
                                    ),
                                ),
                                style={"width": "550px", "height": "480px"},
                            ),
                        ],
                        #    width=5,
                    ),
                ]
            ),
            dbc.Row([html.P(" "), html.P(" ")]),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.P(
                                "Daily ICU Hospitalizations",
                                style={"font-size": "25px"},
                            ),
                            html.P(
                                "Shows the daily number of people per million admitted to the ICU for the selected countries, over the date range selected by the slider above.",
                            ),
                            dbc.Toast(
                                dcc.Loading(
                                    html.Iframe(
                                        id="chart_3",
                                        style={
                                            "display": "block",
                                            "overflow": " hidden",
                                            # "margin": "auto",
                                            "border-width": "0",
                                            "width": "550px",
                                            "height": "500px",
                                        },
                                    ),
                                ),
                                style={"width": "550px", "height": "480px"},
                            ),
                        ],
                        #  width=4,
                    ),
                    dbc.Col(
                        [
                            html.P(
                                "Daily Hospitalizations",
                                style={"font-size": "25px"},
                            ),
                            html.P(
                                "Shows the daily number of people per million admitted to the hospital for the selected countries, over the date range selected by the slider above.",
                            ),
                            dbc.Toast(
                                dcc.Loading(
                                    html.Iframe(
                                        id="chart_4",
                                        style={
                                            "display": "block",
                                            "overflow": " hidden",
                                            # "margin": "auto",
                                            "border-width": "0",
                                            "width": "550px",
                                            "height": "500px",
                                        },
                                    ),
                                ),
                                style={"width": "550px", "height": "480px"},
                            ),
                        ],
                        # width=5,
                        style={"height": "700px"},
                    ),
                ]
            ),
        ]
    ),
)


# Setup app and layout/ frontend
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "World COVID-19 Dashboard"
server = app.server

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                sidebar,
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.P(
                                    " ",
                                ),
                                html.B(
                                    [
                                        "Date Slider ",
                                        html.Span(
                                            "(?)",
                                            id="tooltip-target2",
                                            style={
                                                "textDecoration": "underline",
                                                "cursor": "pointer",
                                                "font-size": "10px",
                                                "vertical-align": "top",
                                            },
                                        ),
                                    ]
                                ),
                                dbc.Tooltip(
                                    "Use this slider to adjust the date range of the visualizations. The dates displayed below, are the boundaries of the timeline.",
                                    target="tooltip-target2",
                                ),
                                html.P(
                                    id="date_display",
                                ),
                                html.Br(),
                                html.Br(),
                                html.P(" "),
                                date_slider,
                                html.Br(),
                                html.Br(),
                                html.P(" "),
                                dbc.Tabs(
                                    [
                                        dbc.Tab(
                                            map_tab,
                                            label="Global COVID-19 Map",
                                            tab_id="map-tab",
                                        ),
                                        dbc.Tab(
                                            line_tab,
                                            label="Global COVID-19 Plot",
                                            tab_id="line-tab",
                                        ),
                                        dbc.Tab(
                                            charts_tab,
                                            label="Vaccination and Hospitalization Indicators",
                                            tab_id="charts-tab",
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ],
                    # style={"width": "80%"},
                    width=10,
                ),
            ]
        ),
        dbc.Row(
            [
                dcc.Markdown(
                    "The World COVID-19 Dashboard was created and maintained by [Adam Morphy](https://github.com/adammorphy), [Kingslin Lv](https://github.com/Kingslin0810), [Kristin Bunyan](https://github.com/khbunyan), and [Thomas Siu](https://github.com/thomassiu)."
                )
            ],
            style={
                "height": "60px",
                "background-color": "#e5e5e5",
                "font-size": "14px",
                "padding-left": "20px",
                "padding-top": "20px",
            },
        ),
    ],
    fluid=True,
)

# Map plot sample
@app.callback(
    Output("map_plot", "figure"),
    [
        Input("feature_dropdown", "value"),
        Input("country-selector", "value"),
        Input("date_slider", "value"),
        # Input("scale_radio", "value"),
    ],
)
def plot_map(ycol, countries, daterange):

    if daterange is None:
        daterange.append(0)
        daterange.append(list(marks.keys())[-1])

    filter_df = filter_data(
        df,
        date_from=marks.get(daterange[0]),
        date_to=marks.get(daterange[1]),
        countries=countries,
    )

    filter_df["count"] = filter_df[ycol]
    filter_df["date_str"] = filter_df["date"].apply(lambda x: str(x))

    fig = px.choropleth(
        data_frame=filter_df,
        locations="iso_code",
        hover_name="location",
        color=ycol,
        animation_frame="date_str",
        animation_group=ycol,
        color_continuous_scale=px.colors.sequential.deep,
        labels={ycol: " "},
    )

    fig.update_layout(
        geo=dict(
            showframe=False, showcoastlines=False, projection_type="equirectangular"
        )
    )

    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 50
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 50

    return fig


# Map line chart
@app.callback(
    Output("line_chart", "srcDoc"),
    [
        Input("feature_dropdown2", "value"),
        Input("country-selector", "value"),
        Input("date_slider", "value"),
        Input("scale-map-line-radio", "value"),
        Input("points_option", "value"),
    ],
)
def plot_map_line_chart(ycol, countries, daterange, scale, points_option=False):

    if daterange is None:
        daterange.append(0)
        daterange.append(list(marks.keys())[-1])

    filter_df = filter_data(
        df,
        date_from=marks.get(daterange[0]),
        date_to=marks.get(daterange[1]),
        countries=countries,
    )

    filter_df["count"] = filter_df[ycol]

    click = alt.selection_multi(fields=["location"], bind="legend")

    line = (
        alt.Chart(filter_df)
        .mark_line()
        .transform_window(
            rolling_mean="mean(count)",
            frame=[-7, 0],
            groupby=["location"],
        )
        .encode(
            y=alt.Y(
                "rolling_mean:Q",
                scale=alt.Scale(domainMin=0, type=scale),
                title="",
            ),
            x="date",
            tooltip=["location", alt.Tooltip(ycol, title="count")],
            color=alt.Color(
                "location",
                legend=alt.Legend(
                    title="",
                    orient="none",
                    direction="horizontal",
                    legendX=0,
                    legendY=-50,
                    columns=4,
                ),
            ),
            opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)),
        )
    )

    chart = None

    points = (
        alt.Chart(filter_df)
        .mark_circle(size=5, opacity=0.4)
        .encode(
            y=alt.Y(
                "count:Q",
                scale=alt.Scale(domainMin=0, type=scale),
                title="",
            ),
            x="date",
            tooltip=["location", alt.Tooltip(ycol, title="count")],
            color=alt.Color("location"),
            opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)),
        )
    )

    if points_option == False:
        chart = (
            line.properties(width=800, height=400)
            .add_selection(click)
            .interactive()
            .configure_title(
                fontSize=15,
                anchor="start",
            )
            .configure_legend(title=None)
        )

    elif points_option == True:
        chart = (
            alt.layer(points, line)
            .properties(width=800, height=400)
            .add_selection(click)
            .interactive()
            .configure_title(
                fontSize=15,
                anchor="start",
            )
            .configure_legend(title=None)
        )

    return chart.to_html()


@app.callback(Output("date_display", "children"), Input("date_slider", "value"))
def update_output(value):
    template = " Date range: {} to {}"

    if value is None:
        value = []
        value.append(0)
        value.append(list(marks.keys())[-1])

    output_string = template.format(marks.get(value[0]), marks.get(value[1]))

    return output_string


# line chart 1
@app.callback(
    Output("chart_1", "srcDoc"),
    [
        Input("country-selector", "value"),
        Input("date_slider", "value"),
        Input("scale-charts-radio", "value"),
    ],
)
def plot_chart_1(countries, daterange, scale):

    if daterange is None:
        daterange.append(0)
        daterange.append(list(marks.keys())[-1])

    filter_df = filter_data(
        df,
        date_from=marks.get(daterange[0]),
        date_to=marks.get(daterange[1]),
        countries=countries,
    )

    filter_df["count"] = filter_df["people_fully_vaccinated"] / 1000000

    click = alt.selection_multi(fields=["location"], bind="legend")

    chart = (
        alt.Chart(filter_df)
        .mark_line()
        .transform_window(
            rolling_mean="mean(count)",
            frame=[-7, 0],
            groupby=["location"],
        )
        .encode(
            y=alt.Y(
                "rolling_mean:Q",
                scale=alt.Scale(domainMin=0, type=scale),
                title="People fully vaccinated",
            ),
            x="date",
            tooltip=[
                "location",
                alt.Tooltip("people_fully_vaccinated", title="People fully vaccinated"),
            ],
            color=alt.Color(
                "location",
                legend=alt.Legend(
                    title="",
                    orient="none",
                    direction="horizontal",
                    legendX=0,
                    legendY=-50,
                    columns=4,
                ),
            ),
            opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)),
        )
        .properties(
            width=400,
            height=300,  # title=f"Country Data for people fully vaccinated"
        )
        .add_selection(click)
        .interactive()
        .configure_title(
            fontSize=15,
            anchor="start",
        )
    )

    return chart.to_html()


# line chart 2
@app.callback(
    Output("chart_2", "srcDoc"),
    [
        Input("country-selector", "value"),
        Input("date_slider", "value"),
        Input("scale-charts-radio", "value"),
    ],
)
def plot_chart_2(countries, daterange, scale):

    if daterange is None:
        daterange.append(0)
        daterange.append(list(marks.keys())[-1])

    filter_df = filter_data(
        df,
        date_from=marks.get(daterange[0]),
        date_to=marks.get(daterange[1]),
        countries=countries,
    )

    filter_df["count"] = filter_df["new_vaccinations"] / 1000000

    click = alt.selection_multi(fields=["location"], bind="legend")

    chart = (
        alt.Chart(filter_df)
        .mark_line()
        .transform_window(
            rolling_mean="mean(count)",
            frame=[-7, 0],
            groupby=["location"],
        )
        .encode(
            y=alt.Y(
                "rolling_mean:Q",
                scale=alt.Scale(domainMin=0, type=scale),
                title="People newly vaccinated",
            ),
            x="date",
            tooltip=[
                "location",
                alt.Tooltip("new_vaccinations", title="People newly vaccinated"),
            ],
            color=alt.Color(
                "location",
                legend=alt.Legend(
                    title="",
                    orient="none",
                    direction="horizontal",
                    legendX=0,
                    legendY=-50,
                    columns=4,
                ),
            ),
            opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)),
        )
        .properties(
            width=400,
            height=300,  # title=f"Country Data for people newly vaccinated"
        )
        .add_selection(click)
        .interactive()
        .configure_title(
            fontSize=15,
            anchor="start",
        )
    )

    return chart.to_html()


# Chart 3
@app.callback(
    Output("chart_3", "srcDoc"),
    [
        Input("country-selector", "value"),
        Input("date_slider", "value"),
        Input("scale-charts-radio", "value"),
    ],
)
def plot_chart_3(countries, daterange, scale):

    ycol = "icu_patients_per_million"

    if daterange is None:
        daterange.append(0)
        daterange.append(list(marks.keys())[-1])

    filter_df = filter_data(
        df,
        date_from=marks.get(daterange[0]),
        date_to=marks.get(daterange[1]),
        countries=countries,
    )

    filter_df["count"] = filter_df["icu_patients_per_million"]

    click = alt.selection_multi(fields=["location"], bind="legend")

    chart = (
        alt.Chart(filter_df)
        .mark_line()
        .transform_window(
            rolling_mean="mean(count)",
            frame=[-7, 0],
            groupby=["location"],
        )
        .encode(
            y=alt.Y(
                "rolling_mean:Q",
                scale=alt.Scale(domainMin=0, type=scale),
                title="ICU patients per million",
            ),
            x="date",
            tooltip=[
                "location",
                alt.Tooltip("icu_patients_per_million", title="count"),
            ],
            color=alt.Color(
                "location",
                legend=alt.Legend(
                    title="",
                    orient="none",
                    direction="horizontal",
                    legendX=0,
                    legendY=-50,
                    columns=4,
                ),
            ),
            opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)),
        )
        .properties(
            width=400,
            height=300,
            # title=f"Country Data for ICU patients per million people",
        )
        .add_selection(click)
        .interactive()
        .configure_title(
            fontSize=15,
            anchor="start",
        )
    )

    return chart.to_html()


# Chart 4
@app.callback(
    Output("chart_4", "srcDoc"),
    [
        Input("country-selector", "value"),
        Input("date_slider", "value"),
        Input("scale-charts-radio", "value"),
    ],
)
def plot_chart_4(countries, daterange, scale):

    if daterange is None:
        daterange.append(0)
        daterange.append(list(marks.keys())[-1])

    filter_df = filter_data(
        df,
        date_from=marks.get(daterange[0]),
        date_to=marks.get(daterange[1]),
        countries=countries,
    )

    filter_df["count"] = filter_df["hosp_patients_per_million"]

    click = alt.selection_multi(fields=["location"], bind="legend")

    chart = (
        alt.Chart(filter_df)
        .mark_line()
        .transform_window(
            rolling_mean="mean(count)",
            frame=[-7, 0],
            groupby=["location"],
        )
        .encode(
            y=alt.Y(
                "rolling_mean:Q",
                scale=alt.Scale(domainMin=0, type=scale),
                title="Hospitalized patients per million",
            ),
            x="date",
            tooltip=[
                "location",
                alt.Tooltip("hosp_patients_per_million", title="count"),
            ],
            color=alt.Color(
                "location",
                legend=alt.Legend(
                    title="",
                    orient="none",
                    direction="horizontal",
                    legendX=0,
                    legendY=-50,
                    columns=4,
                ),
            ),
            opacity=alt.condition(click, alt.value(0.9), alt.value(0.2)),
        )
        .properties(
            width=400,
            height=300,
            # title=f"Country Data for hospitalized patients per million people",
        )
        .add_selection(click)
        .interactive()
        .configure_title(
            fontSize=15,
            anchor="start",
        )
    )

    return chart.to_html()


if __name__ == "__main__":
    app.run_server()
