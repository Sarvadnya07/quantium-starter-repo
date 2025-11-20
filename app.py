# app.py
import pandas as pd
from datetime import datetime
from dash import Dash, dcc, html
import plotly.express as px

# Load data from data/final_output.csv
DF_PATH = "data/final_output.csv"
df = pd.read_csv(DF_PATH)

# Ensure date is datetime and sort
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Build line chart: aggregate sales per day (in case multiple rows per date)
daily = df.groupby("date", as_index=False)["sales"].sum()

fig = px.line(
    daily,
    x="date",
    y="sales",
    title="Daily Sales of Pink Morsel",
    labels={"date": "Transaction Date", "sales": "Total Sales (USD)"}
)

# Mark the price increase date
price_increase_date = datetime(2021, 1, 15)
# Draw the vertical line for Jan 15, 2021
fig.add_vline(
    x=price_increase_date,
    line_width=2,
    line_dash="dash",
    line_color="red"
)

# Add the annotation separately (Plotly-safe)
fig.add_annotation(
    x=price_increase_date,
    y=max(df["sales"]),   # puts the text at the top
    text="Price Increase (15 Jan 2021)",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    bgcolor="rgba(255, 200, 200, 0.7)"
)


app = Dash(__name__)
server = app.server  # expose the server for gunicorn

app.layout = html.Div(
    [
        html.H1("Soul Foods — Pink Morsel Sales Visualiser", style={"textAlign": "center"}),
        dcc.Graph(id="sales-line", figure=fig),
        html.P("Vertical dashed line = price increase on 15 Jan 2021.", style={"textAlign": "center"}),
    ],
    style={"maxWidth": "900px", "margin": "0 auto", "padding": "20px"}
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
