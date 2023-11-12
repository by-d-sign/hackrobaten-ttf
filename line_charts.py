import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.express.colors import sample_colorscale
from plot_map import plot_map

Load_Data = True

if not Load_Data:
    # load data from mastercard
    path_master = r"C:\Users\lisa2\Desktop\Tilo\Hackathon\MastercardData\GeoInsights_Synthetic_Output.csv"
    df = pd.read_csv(path_master)

    l = df.describe()

    # filter raw data

    # event war am 8.2.-12.2.
    date_start = "2023-01-24"
    date_end = "2023-02-27"
    # date_start = "2023-01-25"
    # date_end = "2023-02-20"
    df = df[(df["txn_date"]>date_start)&(df["txn_date"]<date_end)]

    #df = df[(df["txn_date"] == "2022-02-10")]
    # only get Total Retail
    #df = df[df["industry"] == "Total Retail"]

    # load id --> translation
    path_mid = r"C:\Users\lisa2\Desktop\Tilo\Hackathon\MastercardData\GeoInsights_Hackathon_Quads_GeoInfo.csv"
    df_id = pd.read_csv(path_mid, sep="|")


    # add lat, long
    def get_coord(r):
        id = r["quad_id"]
        row = df_id[df_id["quad_id"] == id].iloc[0]
        return row["central_latitude"], row["central_longitude"], row["bounding_box"]


    df[["lat", "lon", "poly"]] = df.apply(get_coord, axis=1, result_type="expand")

    # filter everything around point

    # Bad Gasstein
    POI_lat = 47.11126
    POI_lon = 13.13416
    # Wien
    # POI_lat = 48.2100321
    # POI_lon = 16.3696289

    SCALE = 0.00744
    RADIUS = 10 * SCALE  # [km] --> rad


    def calc_dist(row):
        return (row["lat"] - POI_lat) ** 2 + (row["lon"] - POI_lon) ** 2  # -->rad to km


    df["distance"] = df.apply(calc_dist, axis=1)

    df = df[df["distance"] < RADIUS ** 2]

    # add weekday to the data
    # df["weekday"] = pd.to_datetime(df["txn_date"], format='%Y-%m-%d').dt.day_name()

    # save data
    df.to_csv("savepoint.csv")
else:
    df = pd.read_csv("savepoint.csv")

# group by date
rename_dict = {"txn_date":"date", "txn_amt":"sales", "acct_cnt":"unique cards numbers"}
dfg = df.filter(list(rename_dict.keys()))
dfg = dfg.rename(columns=rename_dict)
dfg = dfg.groupby(by=["date"]).mean().reset_index()
#dfg = dfg.groupby(by=["date", "industry"]).sum().reset_index()
dfg["weekday"] = pd.to_datetime(dfg["date"], format='%Y-%m-%d').dt.day_name()

# Event vs 2 Wochen vorher
df_pre = dfg[(dfg["date"]>"2023-01-25")&(dfg["date"]<"2023-01-30")].reset_index(drop=True)
#df_pre["time"] = "2 weeks ago"


df_now = dfg[(dfg["date"]>"2023-02-08")&(dfg["date"]<"2023-02-13")].reset_index(drop=True)

df_past = dfg[(dfg["date"]>"2023-02-22")&(dfg["date"]<"2023-02-27")].reset_index(drop=True)
#df_past["time"] = "2 weeks ahead"

df_pre["sales"] = df_now["sales"] - df_pre["sales"]
df_pre["unique cards numbers"] = df_now["unique cards numbers"] - df_pre["unique cards numbers"]

df_past["sales"] = df_now["sales"] - df_past["sales"]
df_past["unique cards numbers"] = df_now["unique cards numbers"] - df_past["unique cards numbers"]

#df = pd.concat([df_pre, df_past], ignore_index=True)


fig = make_subplots(rows=1, cols=2, shared_yaxes=True,
                    subplot_titles=('average sales in comparision to two weeks ago and ahead',  'unique cards numbers in comparision to two weeks ago and ahead'))

fig.append_trace(go.Scatter(
    x=df_pre["weekday"],
    y=df_pre["sales"],
    name="2 weeks ago"),
    row=1, col=1)

fig.append_trace(go.Scatter(
    x=df_past["weekday"],
    y=df_past["sales"],
    name="2 weeks ahead"),
    row=1, col=1)

fig.append_trace(go.Scatter(
    x=df_pre["weekday"],
    y=df_pre["unique cards numbers"],
    name="2 weeks ago"),
    row=1, col=2)

fig.append_trace(go.Scatter(
    x=df_past["weekday"],
    y=df_past["unique cards numbers"],
    name="2 weeks ahead"),
    row=1, col=2)

# edit axis labels
fig['layout']['xaxis']['title']='weekday'
fig['layout']['xaxis2']['title']='weekday'
fig['layout']['yaxis']['title']='index'
# fig['layout']['yaxis']['title']='average sales (index)'
# fig['layout']['yaxis2']['title']='unique cards numbers (index)'

fig.update_layout(
    title=dict(text="Event weekend in comparison to normal weekend", font=dict(size=50), x=0.5),
)

#fig = px.line(df, x="weekday", y="sales", title='sales compared to 2 weeks ago and ahead', color="time")
fig.show()

# fig = px.line(dfg, x="date", y="unique cards", title='uniquecards over time', color="industry")
# fig.show()