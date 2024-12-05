import pandas as pd


# Aggregates data from CSV files into one dataframe
def aggregate_raw_data(filenames):
    aggregated_data = pd.DataFrame()

    for file in filenames:
        aggregated_data = pd.concat([aggregated_data, pd.read_csv(file, parse_dates=['LOCAL_DATE'])])

    return aggregated_data


# Fills in missing mean temperature values
def fill_in_missing_temperatures(data):
    if pd.isna(data['MEAN_TEMPERATURE']):
        data['MEAN_TEMPERATURE'] = (data['MIN_TEMPERATURE'] + data['MAX_TEMPERATURE']) / 2

    return data


# Prints out a short summary of the data
def summary(data):
    max_stations = data.groupby('STATION_NAME').agg({'LOCAL_DATE': 'max'})
    min_stations = data.groupby('STATION_NAME').agg({'LOCAL_DATE': 'min'})

    print("|=====SUMMARY====|")
    print("\nMax Date:")
    print(max_stations.min())
    print("\nMin Date:")
    print(min_stations.max())
    print("\nRow Counts:")
    print(data.count())

    return


def main():
    weather_filenames = ['raw_bc_daily_weather_data/bc_daily_weather_data_0.csv',
                         'raw_bc_daily_weather_data/bc_daily_weather_data_1.csv',
                         'raw_bc_daily_weather_data/bc_daily_weather_data_2.csv',
                         'raw_bc_daily_weather_data/bc_daily_weather_data_3.csv',
                         'raw_bc_daily_weather_data/bc_daily_weather_data_4.csv',
                         'raw_bc_daily_weather_data/bc_daily_weather_data_5.csv',
                         'raw_bc_daily_weather_data/bc_daily_weather_data_6.csv',
                         'raw_bc_daily_weather_data/bc_daily_weather_data_7.csv',
                         'raw_bc_daily_weather_data/bc_daily_weather_data_8.csv']

    indexes = ['STATION_NAME',
                    'y',
                    'x',
                    'LOCAL_DATE',
                    'MIN_TEMPERATURE',
                    'MAX_TEMPERATURE',
                    'MEAN_TEMPERATURE',
                    'TOTAL_PRECIPITATION',
                    'TOTAL_RAIN',
                    'TOTAL_SNOW',
                    'SNOW_ON_GROUND']

    aggregated_weather_data = aggregate_raw_data(weather_filenames)
    aggregated_weather_data = aggregated_weather_data[indexes]
    aggregated_weather_data = aggregated_weather_data.rename(columns={'y': 'Latitude', 'x': 'Longitude'})
    aggregated_weather_data = aggregated_weather_data.sort_values(['STATION_NAME', 'LOCAL_DATE'],
                                                                  ascending=[True, True])

    # Drops rows where more than one temperature value is missing (AKA we cannot calculate the missing temperature values)
    aggregated_weather_data = aggregated_weather_data.dropna(
        subset=['MIN_TEMPERATURE', 'MAX_TEMPERATURE', 'MEAN_TEMPERATURE'], how='all')
    aggregated_weather_data = aggregated_weather_data.dropna(subset=['MIN_TEMPERATURE', 'MAX_TEMPERATURE'], how='all')
    aggregated_weather_data = aggregated_weather_data.dropna(subset=['MIN_TEMPERATURE', 'MEAN_TEMPERATURE'], how='all')
    aggregated_weather_data = aggregated_weather_data.dropna(subset=['MAX_TEMPERATURE', 'MEAN_TEMPERATURE'], how='all')

    # Fills in missing mean temperatures
    aggregated_weather_data = aggregated_weather_data.apply(fill_in_missing_temperatures, axis=1)

    # Iterates over the possible stations and drop stations with too many consecutive null values
    valid_stations = []
    stations = aggregated_weather_data["STATION_NAME"].unique()
    for station in stations:
        station_df = aggregated_weather_data[aggregated_weather_data["STATION_NAME"] == station]
        # Adapted from user EdChum's answer on stackoverflow
        # Reference: https://stackoverflow.com/questions/29007830/identifying-consecutive-nans-with-pandas
        consecutive_count_1 = station_df["TOTAL_PRECIPITATION"].isnull().astype(int).groupby(station_df["TOTAL_PRECIPITATION"].notnull().astype(int).cumsum()).sum()
        consecutive_count_2 = station_df["TOTAL_RAIN"].isnull().astype(int).groupby(station_df["TOTAL_RAIN"].notnull().astype(int).cumsum()).sum()
        consecutive_count_3 = station_df["TOTAL_SNOW"].isnull().astype(int).groupby(station_df["TOTAL_SNOW"].notnull().astype(int).cumsum()).sum()
        consecutive_count_4 = station_df["SNOW_ON_GROUND"].isnull().astype(int).groupby(station_df["SNOW_ON_GROUND"].notnull().astype(int).cumsum()).sum()
        # If we're missing more than 7 days in a row, filter out that station
        if (consecutive_count_1.max() >= 7) and ((consecutive_count_2.max() >= 7) or (consecutive_count_3.max() >= 7)):
            continue
        elif (consecutive_count_4.max() >= 14):
            continue
        else:
            valid_stations.append(station)

    # Filter outs the datapoints only from valid stations
    aggregated_weather_data = aggregated_weather_data[aggregated_weather_data['STATION_NAME'].isin(valid_stations)]

    # Iterates over the possible stations and drop stations with more than 30% missing data
    filtered_valid_stations = []
    for station in valid_stations:
        station_df = aggregated_weather_data[aggregated_weather_data["STATION_NAME"] == station]

        precipitation_null_row_count = station_df["TOTAL_PRECIPITATION"].isnull().sum(axis = 0)
        rain_null_row_count = station_df["TOTAL_RAIN"].isnull().sum(axis = 0)
        snow_null_row_count = station_df["TOTAL_SNOW"].isnull().sum(axis = 0)
        snow_on_ground_null_row_count = station_df["SNOW_ON_GROUND"].isnull().sum(axis = 0)

        if (precipitation_null_row_count / len(station_df) > 0.3) or (rain_null_row_count / len(station_df) > 0.3) or (snow_null_row_count / len(station_df) > 0.3) or (snow_on_ground_null_row_count / len(station_df) > 0.3):
            continue
        else:
            filtered_valid_stations.append(station)

    # Filters out the datapoints only from valid stations
    aggregated_weather_data = aggregated_weather_data[aggregated_weather_data['STATION_NAME'].isin(filtered_valid_stations)]

    date_range = pd.date_range(start='1/1/2013', end='12/31/2023', freq='D')
    filled_in_aggregated_weather_data = pd.DataFrame()
    for station in filtered_valid_stations:
        station_df = aggregated_weather_data[aggregated_weather_data["STATION_NAME"] == station]

        station_df.set_index('LOCAL_DATE', inplace=True)
        station_df.index = pd.DatetimeIndex(station_df.index)
        station_df = station_df.reindex(date_range).reset_index().rename(columns={"index": "LOCAL_DATE"})

        # Fills in missing data using the last valid data point
        station_df = station_df.ffill()

        filled_in_aggregated_weather_data = pd.concat([filled_in_aggregated_weather_data, station_df])

    # Prints out information about the dataframes
    # summary(aggregated_weather_data)

    # Exports dataframes into CSV files
    filled_in_aggregated_weather_data.to_csv('clean_bc_daily_weather_data/clean_bc_daily_weather_data.csv', index=False)


if __name__ == '__main__':
    main()
