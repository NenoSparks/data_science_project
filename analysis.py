# python analyis.py 0
import sys
import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.decomposition import PCA


def main():
    key = int(sys.argv[1])

    # lets see if theres any correllation between rainfall and water Level
    weather_df = pd.read_csv("valid_data/weather.csv")
    hydro_df = pd.read_csv("valid_data/hydrometric.csv")

    # get the subset we're interested in doing analysis on (in this case total rain and water level)
    rain_data = weather_df[["Date","Station Name","TOTAL_RAIN","TOTAL_PRECIPITATION","MEAN_TEMPERATURE",
            "TOTAL_SNOW","MIN_TEMPERATURE","MAX_TEMPERATURE","SNOW_ON_GROUND","match key"]]
    level_data = hydro_df[["Date","Station Name","Daily Discharge","Daily Water Level","match key"]]

    # get the data for a single matched station
    rain_data_0 = rain_data[rain_data["match key"] == key]
    level_data_0 = level_data[level_data["match key"] == key]

    combine0 = rain_data_0.merge(level_data_0, on="Date")

    ml_data = combine0[["TOTAL_RAIN","TOTAL_PRECIPITATION","MEAN_TEMPERATURE",
            "TOTAL_SNOW","MIN_TEMPERATURE","MAX_TEMPERATURE","SNOW_ON_GROUND","Daily Discharge","Daily Water Level"]]
    
    # get our labels
    ml_data["y"] = ml_data["Daily Water Level"].shift(-1)

    # remove row with null in "y"
    ml_data = ml_data.iloc[:-1]

    

    # dont use random train test split, order matters, time series data
    # X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.3, shuffle=False)
    # TODO ideally, we can organize data by season, so we can predict based on station and season, but that would require
    # a 40 year span to get the same amount of data points as we have now (which is already very few)
    train = ml_data[:3000]
    X_train = train[["TOTAL_RAIN","TOTAL_SNOW","SNOW_ON_GROUND","MEAN_TEMPERATURE","Daily Discharge","Daily Water Level"]]
    y_train = train["y"]
    valid = ml_data[3000:]
    X_valid = valid[["TOTAL_RAIN","TOTAL_SNOW","SNOW_ON_GROUND","MEAN_TEMPERATURE","Daily Discharge","Daily Water Level"]]
    y_valid = valid["y"]

    model = make_pipeline(
        StandardScaler(),
        PCA(6),
        KNeighborsRegressor(n_neighbors=50, weights='distance')
    )
    model.fit(X_train, y_train)
    print("Train Score: ", model.score(X_train, y_train))
    print("Test Score: ", model.score(X_valid, y_valid))



if __name__ == "__main__":
    main()