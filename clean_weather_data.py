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

    indexes_ver1 = ['STATION_NAME',
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

    indexes_ver2 = ['STATION_NAME',
                    'Latitude',
                    'Longitude',
                    'LOCAL_DATE',
                    'MIN_TEMPERATURE',
                    'MAX_TEMPERATURE',
                    'MEAN_TEMPERATURE',
                    'TOTAL_PRECIPITATION']

    aggregated_weather_data = aggregate_raw_data(weather_filenames)
    aggregated_weather_data = aggregated_weather_data[indexes_ver1]
    aggregated_weather_data = aggregated_weather_data.rename(columns={'y': 'Latitude', 'x': 'Longitude'})
    aggregated_weather_data = aggregated_weather_data.sort_values(['STATION_NAME', 'LOCAL_DATE'],
                                                                  ascending=[True, True])

    # Drops rows were more than one temperature value is missing (AKA we cannot calculate the missing temperature values)
    aggregated_weather_data = aggregated_weather_data.dropna(
        subset=['MIN_TEMPERATURE', 'MAX_TEMPERATURE', 'MEAN_TEMPERATURE'], how='all')
    aggregated_weather_data = aggregated_weather_data.dropna(subset=['MIN_TEMPERATURE', 'MAX_TEMPERATURE'], how='all')
    aggregated_weather_data = aggregated_weather_data.dropna(subset=['MIN_TEMPERATURE', 'MEAN_TEMPERATURE'], how='all')
    aggregated_weather_data = aggregated_weather_data.dropna(subset=['MAX_TEMPERATURE', 'MEAN_TEMPERATURE'], how='all')

    # Fills in missing mean temperatures
    aggregated_weather_data = aggregated_weather_data.apply(fill_in_missing_temperatures, axis=1)

    # Drops rows with any null value(s)
    aggregated_weather_data_ver1 = aggregated_weather_data.dropna()
    aggregated_weather_data_ver2 = aggregated_weather_data[indexes_ver2].dropna()

    # Prints out information about the dataframes
    # summary(aggregated_weather_data)
    # summary(aggregated_weather_data_ver1)
    # summary(aggregated_weather_data_ver2)

    # Exports dataframes into CSV files
    aggregated_weather_data.to_csv('clean_bc_daily_weather_data/clean_bc_daily_weather_data.csv', index=False)
    aggregated_weather_data_ver1.to_csv('clean_bc_daily_weather_data/clean_bc_daily_weather_data_ver1.csv', index=False)
    aggregated_weather_data_ver2.to_csv('clean_bc_daily_weather_data/clean_bc_daily_weather_data_ver2.csv', index=False)


if __name__ == '__main__':
    main()
