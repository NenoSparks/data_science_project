# [CMPT353 Project] Title

For this project, we explored the daily weather and hydrometric data in British Columbia (BC) in order to determine if there are any relationships between the two datasets that would help predict areas that would be susceptible to flooding.

---

## Table of Contents

1. [General Information](#general-information)
   1. [Members](#members)
2. [How to Run the Code](#how-to-run-the-code)
   1. [Step 0) Install Python and Necessary Libraries](#step-0-install-python-and-necessary-libraries)
   2. [Step 1) Run _extract_weather_data.py_](#step-1-run-_extract_weather_datapy_)
   3. [Step 2) Run _clean_weather_data.py_](#step-2-run-_clean_weather_datapy_)
   4. 

---

## General Information

### Members

- Amy Jia Ying Tan [301388738]
- Christopher Halim [301365204]

---

## How to Run the Code

### Step 0) Install Python and Necessary Libraries

In order to run the code in this project, you must have the latest version of [Python](https://www.python.org/downloads/) installed on your computer.

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

### Step 3) Run  _clean_hydrometric_data.py_

**Expected Input:** A folder called raw_hydrometric_data.py

**Expected Output:** A new folder called clean_hydrometric_data

#### Instructions

1. Run _clean_hydrometric_data.py_ with raw_hydrometric_data as its first input parameter and clean_hydrometric_data as its second.
2. Check to see that a folder has been created with clean_hydrometric_data.csv inside. There will also be a rawAggregateData.csv file inside, feel free to ignore it, it's just an intermediate file used by clean_hydrometric_data.py

---

clean_data.py takes an input directory and output directory as arguments. It will filter for valid input rows, then aggregate all valid rows from all input files into a single csv file output into the output directory.

Include how/where we downloaded the raw hydrometric data and raw climate data
