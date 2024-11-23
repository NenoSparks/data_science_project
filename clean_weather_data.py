import pandas as pd


def aggregate_raw_data(filenames):
    aggregated_data = pd.DataFrame()

    for file in filenames:
        aggregated_data = pd.concat([aggregated_data, pd.read_csv(file, parse_dates=['LOCAL_DATE'])])

    return aggregated_data


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
               'MIN_REL_HUMIDITY',
               'MAX_REL_HUMIDITY',
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
    aggregated_weather_data = aggregated_weather_data.sort_values(['STATION_NAME', 'LOCAL_DATE'], ascending=[True, True])

    aggregated_weather_data = aggregated_weather_data.dropna(how='any')

    aggregated_weather_data.to_csv('clean_bc_daily_weather_data/clean_bc_daily_weather_data.csv', index=False)


if __name__ == '__main__':
    main()
