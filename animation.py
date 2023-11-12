import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.express.colors import sample_colorscale
from plot_map import plot_map


# load data from mastercard
path_master = r"C:\Users\lisa2\Desktop\Tilo\Hackathon\MastercardData\GeoInsights_Synthetic_Output.csv"
df = pd.read_csv(path_master)

# filter raw data

# event war am 8.2.-12.2.
date_start = "2023-02-16"
date_end = "2023-02-20"
#df = df[(df["txn_date"]>date_start)&(df["txn_date"]<date_end)]

df = df[(df["txn_date"] == "2022-02-10")]
# only get Total Retail

df = df[df["industry"] == "Total Retail"]

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
# POI_lat = 47.11126
# POI_lon = 13.13416
# Wien
POI_lat = 48.2100321
POI_lon = 16.3696289

SCALE = 0.00744
RADIUS = 20 * SCALE  # [km] --> rad


def calc_dist(row):
    return (row["lat"] - POI_lat) ** 2 + (row["lon"] - POI_lon) ** 2  # -->rad to km


df["distance"] = df.apply(calc_dist, axis=1)

df = df[df["distance"] < RADIUS ** 2]

# def mean_(x):
#     try:
#         float(x[0])
#         return np.sum(x)
#     except Exception as e:
#         return x[0]
#
# df = df.groupby(by=["txn_date"]).agg(mean_).reset_index()

plot_map(df, POI_lon, POI_lat)

# # group by date
# rename_dict = {"txn_date":"date", "txn_amt":"sales", "acct_cnt":"unique cards"}
# dfg = df.filter(list(rename_dict.keys()))
# dfg = dfg.rename(columns=rename_dict)
# dfg = dfg.groupby(by="date").mean().reset_index()
#
# fig = px.line(dfg, x="date", y="sales", title='sales over time')
fig.show()

