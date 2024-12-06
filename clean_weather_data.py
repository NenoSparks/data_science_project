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
    aggregated_weather_data = aggregated_weather_data.rename(columns={'y': 'LATITUDE', 'x': 'LONGITUDE'})
    aggregated_weather_data = aggregated_weather_data.sort_values(['STATION_NAME', 'LOCAL_DATE'],
                                                                  ascending=[True, True])

    # Drops duplicated rows for observations from the same station with the same date
    aggregated_weather_data = aggregated_weather_data.drop_duplicates(
        subset=['LOCAL_DATE', 'STATION_NAME', 'LATITUDE', 'LONGITUDE'], keep='last')

    # Gets all unique stations
    all_stations = aggregated_weather_data[['STATION_NAME', 'LATITUDE', 'LONGITUDE']].drop_duplicates(
        subset=['STATION_NAME', 'LATITUDE', 'LONGITUDE'], keep='last').values.tolist()

    # Filters out stations that don't span the date range from 01/01/2013 to 12/31/2023
    valid_stations1 = []
    valid_station_names = []
    valid_latitudes = []
    valid_longitudes = []
    for station in all_stations:
        station_df = aggregated_weather_data[(aggregated_weather_data["STATION_NAME"] == station[0]) & (
                    aggregated_weather_data["LATITUDE"] == station[1]) & (
                                                         aggregated_weather_data["LONGITUDE"] == station[2])]

        if (station_df['LOCAL_DATE'].min() == pd.Timestamp('2013-01-01')) and (
                station_df['LOCAL_DATE'].max() == pd.Timestamp('2023-12-31')):
            valid_stations1.append(station)
            valid_station_names.append(station[0])
            valid_latitudes.append(station[1])
            valid_longitudes.append(station[2])

    # Filter outs the datapoints only from valid stations
    aggregated_weather_data = aggregated_weather_data[
        (aggregated_weather_data["STATION_NAME"].isin(valid_station_names)) & (
            aggregated_weather_data["LATITUDE"].isin(valid_latitudes)) & (
            aggregated_weather_data["LONGITUDE"].isin(valid_longitudes))]

    # Iterates over the possible stations and drop stations with too many consecutive null values
    valid_stations2 = []
    valid_station_names = []
    valid_latitudes = []
    valid_longitudes = []
    for station in valid_stations1:
        station_df = aggregated_weather_data[(aggregated_weather_data["STATION_NAME"] == station[0]) & (
                    aggregated_weather_data["LATITUDE"] == station[1]) & (
                                                         aggregated_weather_data["LONGITUDE"] == station[2])]
        # Adapted from user EdChum's answer on stackoverflow
        # Reference: https://stackoverflow.com/questions/29007830/identifying-consecutive-nans-with-pandas
        consecutive_count_1 = station_df["TOTAL_PRECIPITATION"].isnull().astype(int).groupby(
            station_df["TOTAL_PRECIPITATION"].notnull().astype(int).cumsum()).sum()
        consecutive_count_2 = station_df["TOTAL_RAIN"].isnull().astype(int).groupby(
            station_df["TOTAL_RAIN"].notnull().astype(int).cumsum()).sum()
        consecutive_count_3 = station_df["TOTAL_SNOW"].isnull().astype(int).groupby(
            station_df["TOTAL_SNOW"].notnull().astype(int).cumsum()).sum()
        consecutive_count_4 = station_df["SNOW_ON_GROUND"].isnull().astype(int).groupby(
            station_df["SNOW_ON_GROUND"].notnull().astype(int).cumsum()).sum()
        # If we're missing more than 7 days in a row, filter out that station
        if (consecutive_count_1.max() >= 7) and ((consecutive_count_2.max() >= 7) or (consecutive_count_3.max() >= 7)):
            continue
        elif (consecutive_count_4.max() >= 14):
            continue
        else:
            valid_stations2.append(station)
            valid_station_names.append(station[0])
            valid_latitudes.append(station[1])
            valid_longitudes.append(station[2])

    # Filter outs the datapoints only from valid stations
    aggregated_weather_data = aggregated_weather_data[
        (aggregated_weather_data["STATION_NAME"].isin(valid_station_names)) & (
            aggregated_weather_data["LATITUDE"].isin(valid_latitudes)) & (
            aggregated_weather_data["LONGITUDE"].isin(valid_longitudes))]

    # Iterates over the possible stations and drop stations with more than 30% missing data
    valid_stations3 = []
    valid_station_names = []
    valid_latitudes = []
    valid_longitudes = []
    for station in valid_stations2:
        station_df = aggregated_weather_data[
            (aggregated_weather_data["STATION_NAME"] == station[0]) & (
                        aggregated_weather_data["LATITUDE"] == station[1]) & (
                        aggregated_weather_data["LONGITUDE"] == station[2])]

        precipitation_null_row_count = station_df["TOTAL_PRECIPITATION"].isnull().sum(axis=0)
        rain_null_row_count = station_df["TOTAL_RAIN"].isnull().sum(axis=0)
        snow_null_row_count = station_df["TOTAL_SNOW"].isnull().sum(axis=0)
        snow_on_ground_null_row_count = station_df["SNOW_ON_GROUND"].isnull().sum(axis=0)

        if (precipitation_null_row_count / len(station_df) > 0.3) or (rain_null_row_count / len(station_df) > 0.3) or (
                snow_null_row_count / len(station_df) > 0.3) or (snow_on_ground_null_row_count / len(station_df) > 0.3):
            continue
        else:
            valid_stations3.append(station)
            valid_station_names.append(station[0])
            valid_latitudes.append(station[1])
            valid_longitudes.append(station[2])

    # Filter outs the datapoints only from valid stations
    aggregated_weather_data = aggregated_weather_data[
        (aggregated_weather_data["STATION_NAME"].isin(valid_station_names)) & (
            aggregated_weather_data["LATITUDE"].isin(valid_latitudes)) & (
            aggregated_weather_data["LONGITUDE"].isin(valid_longitudes))]

    # Drops rows where more than one temperature value is missing (AKA we cannot calculate the missing temperature values)
    aggregated_weather_data = aggregated_weather_data.dropna(
        subset=['MIN_TEMPERATURE', 'MAX_TEMPERATURE', 'MEAN_TEMPERATURE'], how='all')
    aggregated_weather_data = aggregated_weather_data.dropna(
        subset=['MIN_TEMPERATURE', 'MAX_TEMPERATURE'], how='all')
    aggregated_weather_data = aggregated_weather_data.dropna(
        subset=['MIN_TEMPERATURE', 'MEAN_TEMPERATURE'], how='all')
    aggregated_weather_data = aggregated_weather_data.dropna(
        subset=['MAX_TEMPERATURE', 'MEAN_TEMPERATURE'], how='all')

    # Fills in missing mean temperatures
    filled_in_aggregated_weather_data = aggregated_weather_data.apply(fill_in_missing_temperatures, axis=1)

    # Fills in missing dates ranging between 1/1/2013 and 12/31/2023 for each station
    final_aggregated_weather_data = pd.DataFrame()

    date_range = pd.date_range(start='1/1/2013', end='12/31/2023', freq='D')
    for station in valid_stations3:
        station_df = filled_in_aggregated_weather_data[
            (filled_in_aggregated_weather_data["STATION_NAME"] == station[0]) & (
                    filled_in_aggregated_weather_data["LATITUDE"] == station[1]) & (
                    filled_in_aggregated_weather_data["LONGITUDE"] == station[2])]

        station_df.set_index('LOCAL_DATE', inplace=True)
        station_df.index = pd.DatetimeIndex(station_df.index)
        station_df = station_df.reindex(date_range).reset_index().rename(columns={"index": "LOCAL_DATE"})

        final_aggregated_weather_data = pd.concat([final_aggregated_weather_data, station_df])

    # Fills in missing data using the last valid data point
    final_aggregated_weather_data = final_aggregated_weather_data.ffill()

    # Prints out information about the dataframes
    # summary(final_aggregated_weather_data)

    # Exports dataframes into CSV files
    final_aggregated_weather_data.to_csv('clean_bc_daily_weather_data/clean_bc_daily_weather_data.csv', index=False)


if __name__ == '__main__':
    main()
