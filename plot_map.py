import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.express.colors import sample_colorscale


def transl_poly(s):
    s = s.replace("POLYGON ((", "").replace("))", "")

    lat, lon = [], []
    points = s.split(", ")
    for p in points:
        parts = p.split(" ")
        lon.append(float(parts[0]))
        lat.append(float(parts[1]))

        # lon.append(float(parts[0]) + SCALE/2)
        # lat.append(float(parts[1]) - SCALE/2)

    return lat, lon


def plot_map(df, POI_lon, POI_lat):
    # plotting of map data

    fig = go.Figure()

    max_txn_amt = df["txn_amt"].max()

    df["color"] = sample_colorscale('OrRd', list(df["txn_amt"] / df["txn_amt"].max()))

    for idx, row in df.iterrows():
        lat, lon = transl_poly(row["poly"])
        fig.add_trace(go.Scattermapbox(
            fill="toself",
            lon=lon, lat=lat,
            marker={'size': 0, 'color': row["color"]}
        )
        )

    fig.update_layout(
        mapbox={'style': "carto-positron", 'center': {'lon': POI_lon, 'lat': POI_lat}, 'zoom': 13},
        showlegend=False,
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0})

    fig.show()

    df["size_txn_amt"] = df["txn_amt"] / df["txn_amt"].max()
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="industry",
                            size="size_txn_amt",
                            color="size_txn_amt",
                            hover_data=["txn_amt", "txn_cnt", "quad_id"],
                            color_discrete_sequence=["fuchsia"],
                            animation_frame="txn_date")  # , zoom=8

    # fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(mapbox={'style': "carto-positron", 'center': {'lon': POI_lon, 'lat': POI_lat}, 'zoom': 13})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()
