# [CMPT353 Project] Predicting Future Floods in British Columbia

For this project, we explored the daily weather and hydrometric data in British Columbia (BC) in order to determine if there are any relationships between the two datasets that would help predict areas that would be susceptible to flooding.

---

## Table of Contents

1. [General Information](#general-information)
   1. [Members](#members)
2. [How to Run the Code](#how-to-run-the-code)
   1. [Step 0) Install Python and Necessary Libraries](#step-0-install-python-and-necessary-libraries)
   2. [Step 1) Run _extract_weather_data.py_](#step-1-run-_extract_weather_datapy_)
   3. [Step 2) Run _clean_weather_data.py_](#step-2-run-_clean_weather_datapy_)
   4. [Step 3) Run _clean_hydrometric_data.py_](#step-3-run-_clean_hydrometric_datapy_)
   5. [Step 4) Run _match_stations.py_](#step-4-run-_match_stationspy_-)
   6. [Step 5) OPTIONAL Run _plot_stations.py_](#step-5-_optional_-run-_plot_stationspy_)
   7. [Step 6) Run _analysis.py_](#step-6-run-_analysispy_)
   8. [Extras](#extras)

---

## General Information

### Members

- Amy Jia Ying Tan [301388738]
- Christopher Halim [301365204]

---

## How to Run the Code

### Step 0) Install Python and Necessary Libraries

In order to run the code in this project, you must have [Python 3.12.4](https://www.python.org/downloads/) or higher installed on your computer.

The following Python libraries are required:
- [NumPy](https://numpy.org/install/)
- [pandas](https://pandas.pydata.org/docs/getting_started/install.html)

### Step 1) Run _extract_weather_data.py_

**Expected Input:** N/A

**Expected Output:** A new folder called _raw_bc_daily_weather_data_ with nine csv files

#### Instructions

1. Run the file called _extract_weather_data.py_ with no input parameters.
2. Check to see a folder with the raw data csv files has been created.

### Step 2) Run _clean_weather_data.py_

**Expected Input:** N/A

**Expected Output:** A new folder called _clean_bc_daily_weather_data_ with one csv file

#### Instructions

1. Run the file called _clean_weather_data.py_ with no input parameters.
2. Check to see a folder with the clean data csv file has been created.

### Step 3) Run _clean_hydrometric_data.py_

**Command:** python clean_hydrometric_data.py raw_hydrometric_data clean_hydrometric_data

**Expected Input:** A folder called raw_hydrometric_data.py

**Expected Output:** A new folder called clean_hydrometric_data

#### Instructions

1. Run _clean_hydrometric_data.py_ with raw_hydrometric_data as its first input parameter and clean_hydrometric_data as its second.
2. Check to see that a folder has been created with clean_hydrometric_data.csv inside. There will also be a rawAggregateData.csv file inside, feel free to ignore it, it's just an intermediate file used by clean_hydrometric_data.py

### Step 4) Run _match_stations.py_ 

**Command:** python match_stations.py clean_bc_daily_weather_data/clean_bc_daily_weather_data.csv clean_hydrometric_data/clean_hydrometric_data.csv

**Expected Input:** Two input files: clean_bc_daily_weather_data/clean_bc_daily_weather_data.csv & clean_hydrometric_data/clean_hydrometric_data.csv

**Expected Output:** Will output list of available match keys to the console.

### Step 5) _OPTIONAL_ Run _plot_stations.py_

**Command:** python plot_stations.py valid_data/weather.csv valid_data/hydrometric.csv

**Expected Input:** Two input files: valid_data/weather.csv & valid_data/hydrometric.csv

**Expected Output:** A browser tab will open with a map of British Columbia as well points showing the location of matched weather and hydrometric stations. trace0 (red points) represent weather stations and trace1 (blue points) represent hydrometric stations. Feel free to zoom in and interact with the map, hover over points to view the station name as well as the latitude and longitude of the station.

### Step 6) Run _analysis.py_

**Command:** python analysis.py 0 (or another valid match key)

**Expected Input:** A valid match key from the list provided after executing Step 4

**Expected Output:** Train and test accuracy scores for a K-Neighbors Regressor Model for data of a given matched station pair.

---

### Extras

Programs used to aid in the development of the above code:
- _find_date_range.py_
- _explore.ipynb_
- _verify_date_fill.ipynb_

Notebook used to create plots of data for use in report
- _analysis.ipynb_
---