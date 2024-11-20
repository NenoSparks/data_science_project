import urllib.request


def main():
    for i in range(9):
        url = ('https://api.weather.gc.ca/collections/climate-daily/items?lang=en&datetime=2013-01-01%2F2023-12-31&PROVINCE_CODE=BC&f=csv&limit=100000'
           + "&offset=" + str(100000 * i))

        file_Path = 'raw_bc_daily_weather_data/bc_daily_weather_data_' + str(i) + ".csv"

        urllib.request.urlretrieve(url, file_Path)
        print("Downloaded lines " + str(100000 * i) + " to " + str(100000 + (100000 * i)))


if __name__ == "__main__":
    main()