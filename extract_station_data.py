import urllib.request


def main():
        url = 'https://api.weather.gc.ca/collections/climate-stations/items?lang=en&limit=2000&PROV_STATE_TERR_CODE=BC&f=csv'

        file_Path = 'raw_bc_climate_stations_data/raw_bc_climate_stations_data.csv'

        urllib.request.urlretrieve(url, file_Path)
        print("Downloaded lines 0 to 2000")


if __name__ == "__main__":
    main()