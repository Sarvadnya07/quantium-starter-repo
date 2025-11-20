# app.py
import pandas as pd
from datetime import datetime
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
DF_PATH = "data/final_output.csv"
df = pd.read_csv(DF_PATH)

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Aggregate daily sales
daily = df.groupby("date", as_index=False)["sales"].sum()

# Default chart (initial)
price_increase_date = datetime(2021, 1, 15)

initial_fig = px.line(
    daily,
    x="date",
    y="sales",
    title="Daily Sales of Pink Morsel",
    labels={"date": "Transaction Date", "sales": "Total Sales (USD)"}
)

# Add default vertical line + annotation
initial_fig.add_vline(
    x=price_increase_date,
    line_width=2,
    line_dash="dash",
    line_color="red"
)
initial_fig.add_annotation(
    x=price_increase_date,
    y=max(daily["sales"]),
    text="Price Increase (15 Jan 2021)",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    bgcolor="rgba(255, 200, 200, 0.7)"
)

# Dash app
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualiser"),

    html.Div(className="radio-group", children=[
        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": "All", "value": "all"},
                {"label": "North", "value": "north"},
                {"label": "East", "value": "east"},
                {"label": "South", "value": "south"},
                {"label": "West", "value": "west"},
            ],
            value="all",
            inline=True,
            style={"margin": "20px", "font-size": "18px"}
        )
    ]),

    dcc.Graph(id="sales-graph", figure=initial_fig)
])

# Callback for filtering by region
@app.callback(
    Output("sales-graph", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        title="Pink Morsel Sales Over Time",
        labels={"date": "Date", "sales": "Sales ($)"}
    )

    # Price increase marker
    fig.add_vline(x=price_increase_date, line_dash="dash", line_color="red")

    fig.add_annotation(
        x=price_increase_date,
        y=max(filtered_df["sales"]),
        text="Price Increase (15 Jan 2021)",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
        bgcolor="rgba(255,200,200,0.7)"
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
