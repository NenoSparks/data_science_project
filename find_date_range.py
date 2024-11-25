# Just a small script used to find a date range where we have mostly complete data :)
import pandas as pd

combined_data = pd.read_csv("combined_data.csv")
combined_data['Date'] = pd.to_datetime(combined_data['Date'], format="%Y/%m/%d")#.dt.date

minDate = combined_data['Date'].min()
maxDate = combined_data['Date'].max()
minStation = ""
maxStation = ""
for station in combined_data['Station ID'].unique():
    stationMin = combined_data[combined_data["Station ID"] == station]['Date'].min()
    stationMax = combined_data[combined_data["Station ID"] == station]['Date'].max()
    if stationMin > minDate:
        minDate = stationMin
        minStation = station
    if stationMax < maxDate:
        maxDate = stationMax
        maxStation = station

print(f'MinDate: {minDate}\nMaxDate: {maxDate}')
print(minStation, maxStation)