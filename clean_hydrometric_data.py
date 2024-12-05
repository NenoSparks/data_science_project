# python clean_hydrometric_data.py raw_hydrometric_data clean_hydrometric_data
import os
import sys
import csv
import pandas as pd

# Date last modified:
# Description:
# Input:
# Output:
# Time Complexity:
def aggregateData(raw_data_path, clean_data_path):
    # if the output directory does not exist, create one
    if not os.path.isdir(clean_data_path):
        os.makedirs(clean_data_path)

    firstFile = True
    count = 0
    with open(f'{clean_data_path}\\rawAggregateData.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        for filename in os.listdir(raw_data_path):
            with open(f'{raw_data_path}\\{filename}', newline='') as infile:
                if (firstFile):
                    reader = list(csv.reader(infile))
                    firstFile = False
                else:
                    reader = list(csv.reader(infile))[2:]

                print(f'Input file {filename} has {len(reader)} rows.')
                count += len(reader)
                for row in reader:
                    writer.writerow(row)

    print(f'Total lines of input data: {count}')


def main():
    raw_data_path = sys.argv[1]
    clean_data_path = sys.argv[2]

    
    aggregateData(raw_data_path, clean_data_path)

    # read our data into a dataframe
    data_df = pd.read_csv("clean_hydrometric_data/rawAggregateData.csv", skiprows=1, dtype={' ID':'str'})
    # get rid of the annoying ' ID' column header
    data_df.rename(columns={" ID":"Station ID"}, inplace=True)

    # Split into two dataframes, PARAM=1 and PARAM=2. Then join the two dataframes
    # rename into 1: Daily Discharge (m3/s) and 2: Daily Water Level (m)
    data_df1 = data_df[data_df['PARAM'] == 1]
    data_df1 = data_df1[['Station ID','Date','Value','SYM']]
    data_df1.rename(columns={"Value":"Daily Discharge", "SYM":"SYM1"}, inplace=True)
    data_df2 = data_df[data_df['PARAM'] == 2]
    data_df2 = data_df2[['Station ID','Date','Value','SYM']]
    data_df2.rename(columns={"Value":"Daily Water Level","SYM":"SYM2"}, inplace=True)

    data_df = pd.merge(data_df1, data_df2, on=["Station ID", "Date"])

    valid_stations = []
    # iterate over the possible stations
    stations = data_df["Station ID"].unique()
    for station in stations:
        station_df = data_df[data_df["Station ID"] == station]
        # Adapted from user EdChum's answer on stackoverflow
        # Reference: https://stackoverflow.com/questions/29007830/identifying-consecutive-nans-with-pandas
        consecutive_count_1 = station_df["Daily Discharge"].isnull().astype(int).groupby(station_df["Daily Discharge"].notnull().astype(int).cumsum()).sum()
        consecutive_count_2 = station_df["Daily Water Level"].isnull().astype(int).groupby(station_df["Daily Water Level"].notnull().astype(int).cumsum()).sum()

        # if we're missing more than 7 days in a row, filter out that station
        if (consecutive_count_1.max() >= 7) or (consecutive_count_2.max() >= 7):
            continue
        else:
            valid_stations.append(station)

    # filter out the datapoints only form valid stations
    data_df = data_df[data_df['Station ID'].isin(valid_stations)]

    # Our data at this point has to form |Station ID|PARAM|Date|Value|SYM|
    # However, 'stationID' is an internal numbering with no meaning. Our weather data is going to
    # be based on a 'Climate ID' so ideally we can combine the stationID with additional metadata
    # so that we can then correctly match the stations between 'stationID' and 'Climate ID'
    # Station ID's have the form ##AA### while the official Climate ID's are a 7 digit number assigned
    # by the Meteorological Service of Canada to a site where official weather observations are taken,
    # and serves as a permanent, unqiue identifier.
    # Our Station ID metadata includes latitude and longitude, so if we are unable to find a perfect match
    # between BC hydrometric and MSC sites we can find one that is closest.

    # read our metadata file
    meta_df = pd.read_csv("bc_station_metadata/metadata_20241115T0843.csv")
    # change header "Station Number" -> "Station ID"
    meta_df.rename(columns={"Station Number":"Station ID"}, inplace=True)

    # Combine data_df with meta_df so each station has lat/long as well as additional values
    combined_data = data_df.merge(meta_df, on="Station ID", sort=True)

    # Before save, get rid of some more useless columns
    columns = ['Date','Station ID','Station Name','Province','Latitude','Longitude','Daily Discharge',
            'SYM1','Daily Water Level','SYM2']
    combined_data = combined_data[columns]

    # Before pivot, get rid of some more useless columns
    columns = ['Date','Station ID','Station Name','Province','Latitude','Longitude','Daily Discharge',
            'SYM1','Daily Water Level','SYM2']
    combined_data = combined_data[columns]

    # remove dates outside of 2013/01/01 - 2023/12/31
    minDate = pd.Timestamp('2013-01-01')
    maxDate = pd.Timestamp('2023-12-31')
    combined_data["Date"] = pd.to_datetime(combined_data["Date"])
    station_df = combined_data.groupby("Station ID").agg({"Date":["min","max"]})
    station_df = station_df[station_df["Date"]["min"] <= minDate]
    station_df = station_df[station_df["Date"]["max"] >= maxDate]
    
    # get only the data from stations with enough data to cover our date range
    combined_data = combined_data[combined_data["Station ID"].isin(list(station_df.index))]

    # use a boolean mask to get just the rows within our date range
    # credit: unutbu on stackoverflow https://stackoverflow.com/questions/29370057/select-dataframe-rows-between-two-dates
    mask = (combined_data['Date'] >= minDate) & (combined_data['Date'] <= maxDate)
    combined_data = combined_data.loc[mask]

    # fill in missing NaN values 
    # Note: we decided it would be okay to fill in missing values by propogating the last
    # valid observation to the next valid since we limited our data to have at most 7
    # consecutive days of missing values.
    # combined_data = combined_data.ffill(axis=1)


    combined_data.to_csv("clean_hydrometric_data/clean_hydrometric_data.csv", index=False)


    # # TODO should likely be a separte script to combine data together and get it into a format for ML
    # # Pivot to get Date as index and columns organized by station id for each feature
    # pivot_df = combined_data.pivot(columns="Station ID", index="Date")


    # # Check for continuity within our dates, decide how to fill in missing values
    # date_range = pd.date_range(start="1/1/2013", end="12/31/2023")
    # # make the index the complete date range we are interested in
    # pivot_df = pivot_df.reindex(date_range)
    

    # # # TODO join data with climate data



    # pivot_df = pivot_df.reset_index(names="Date")
    # pivot_df.to_csv("pivot_data.csv", index=False)

if __name__=='__main__':
    main()

