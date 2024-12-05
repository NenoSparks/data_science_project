# python plot_stations.py valid_data/weather.csv valid_data/hydrometric.csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys

def main():
    # weather_df = pd.read_csv("clean_bc_daily_weather_data/clean_bc_daily_weather_data.csv")
    # hydrometric_df = pd.read_csv("combined_data.csv")
    # wstations_df = weather_df.groupby("STATION_NAME").agg({"Latitude":"mean", "Longitude":"mean"})
    # hstations_df = hydrometric_df.groupby("Station Name").agg({"Latitude":"mean", "Longitude":"mean"})

    # TODO read new files with just the stations we're interested in
    weather_df = pd.read_csv(sys.argv[1])
    hydrometric_df = pd.read_csv(sys.argv[2])
    # get just the station and lat/lon
    wstations_df = weather_df.groupby("STATION_NAME").agg({"Latitude":"mean", "Longitude":"mean"})
    hstations_df = hydrometric_df.groupby("Station Name").agg({"Latitude":"mean", "Longitude":"mean"})

    lat1 = wstations_df['Latitude']
    lon1 = wstations_df['Longitude']
    names1 = list(weather_df["STATION_NAME"])

    lat2 = hstations_df['Latitude']
    lon2 = hstations_df['Longitude']
    names2 = list(hstations_df.index)
    
    # plot weather stations
    trace1 = go.Scattermap(
            lat=lat1,
            lon=lon1,
            mode='markers',
            marker=go.scattermap.Marker(
                size=9,
                color="red"
            ),
            text=names1,
        )
    
    # plot hydrometric stations
    trace2 = go.Scattermap(
            lat=lat2,
            lon=lon2,
            mode='markers',
            marker=go.scattermap.Marker(
                size=9,
                color="blue"
            ),
            text=names2,
        )

    fig = make_subplots()
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    
    fig.update_layout(
        autosize=True,
        hovermode='closest',
        map=dict(
            bearing=0,
            center=dict(
                lat=53.72,
                lon=-122.65
            ),
            pitch=0,
            zoom=4.5
        ),
    )

    fig.show()
    
    

if __name__ == "__main__":
    main()