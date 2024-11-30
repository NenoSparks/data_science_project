# python match_stations.py clean_bc_daily_weather_data/clean_bc_daily_weather_data.csv clean_hydrometric_data/clean_hydrometric_data.csv
# take the weather station data and hydrometric station data as arguments
import numpy as np
import pandas as pd
import sys
import os

# adapted from Exercise 3
def distance(point1, point2):
    # radius of earth given in kilometers
    radius = 6371

    # formula was derived from user 'Salvador Dali' on stackoverflow
    # https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
    distance = 0.5 - np.cos(np.radians((point2[0]-point1[0]))) / 2 + np.cos(np.radians(point1[0])) * np.cos(np.radians(point2[0])) * (1 - np.cos(np.radians((point2[1] - point1[1])))) / 2
    distance = 2 * radius * np.arcsin(np.sqrt(distance))

    return distance

def main():
    weather_data = sys.argv[1]
    hydrom_data = sys.argv[2]

    # weather and hydrometric data
    weather_df = pd.read_csv(weather_data)
    hydrom_df = pd.read_csv(hydrom_data)

    # weather and hydrometric station location data
    wstations_df = weather_df.groupby("STATION_NAME").agg({"Latitude":"mean", "Longitude":"mean"})
    hstations_df = hydrom_df.groupby("Station Name").agg({"Latitude":"mean", "Longitude":"mean"})

    # names of valid weather stations
    valid_w_stations = []
    # names of valid hydrometric stations
    valid_h_stations = []

    # figure out which stations from each dataset correspond to one another
    # iterate over our hydrometric stations since there are fewer compared to weather stations
    for h_station in hstations_df.index:
        h = tuple(hstations_df.loc[h_station, ['Latitude','Longitude']].values)
        for w_station in wstations_df.index:
            w = tuple(wstations_df.loc[w_station, ['Latitude','Longitude']].values)
            if distance(h, w) < 10:
                valid_h_stations.append(h_station)
                valid_w_stations.append(w_station)
                # once we find a single match per hydrometric station move onto the next one
                break
    
    
    assert len(valid_h_stations) == len(valid_w_stations)
    # TODO create dictionary to convert weather station names to hydrometric station names
    # then change all of the names in the clean weather station data and filter for any rows that
    # aren't from the desired station
    
    weather_to_hydro_dict = dict(zip(valid_w_stations, valid_h_stations))
    hydro_to_weather_dict = dict(zip(valid_h_stations, valid_w_stations))

    # get the rest of the data associated with valid stations
    valid_weather_df = weather_df[weather_df["STATION_NAME"].isin(valid_w_stations)]
    valid_station_df = hydrom_df[hydrom_df["Station Name"].isin(valid_h_stations)]

    # if directory /valid_data does not already exist, create it
    if not os.path.isdir("valid_data"):
        os.makedirs("valid_data")

    # save as csv files
    valid_weather_df.to_csv("valid_data/weather.csv", index=False)
    valid_station_df.to_csv("valid_data/hydrometric.csv", index=False)


if __name__ == "__main__":
    main()