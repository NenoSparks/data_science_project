# python combine_data.py valid_data/weather.csv valid_data/hydrometric.csv

import pandas as pd
import sys

def main():
    weather_filename = sys.argv[1]
    hydro_filename = sys.argv[2]

    valid_weather = pd.read_csv(weather_filename)
    valid_hydro = pd.read_csv(hydro_filename)
    
    

if __name__ == "__main__":
    main()
