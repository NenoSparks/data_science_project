# python3 clean_data.py raw_hydrometric_data clean_hydrometric_data
import os
import sys
import csv
import pandas as pd

# Date last modified:
# Description:
# Input:
# Output:
# Time Complexity:
def aggregateData(raw_data_path, clean_data_path):
    # if the output directory does not exist, create one
    if not os.path.isdir(clean_data_path):
        os.makedirs(clean_data_path)

    firstFile = True
    count = 0
    with open(f'{clean_data_path}\\aggregateData.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        for filename in os.listdir(raw_data_path):
            with open(f'{raw_data_path}\\{filename}', newline='') as infile:
                if (firstFile):
                    reader = list(csv.reader(infile))
                    firstFile = False
                else:
                    reader = list(csv.reader(infile))[2:]

                print(f'Input file {filename} has {len(reader)} rows.')
                count += len(reader)
                for row in reader:
                    writer.writerow(row)

    print(f'Total lines of input data: {count}')


def main():
    raw_data_path = sys.argv[1]
    clean_data_path = sys.argv[2]

    
    aggregateData(raw_data_path, clean_data_path)

    # read our data into a dataframe
    data_df = pd.read_csv("clean_hydrometric_data/aggregateData.csv", skiprows=1, dtype={' ID':'str'})
    # get rid of the annoying ' ID' column header
    data_df.rename(columns={" ID":"Station ID"}, inplace=True)

    # TODO filter all of the rows of data_df that have more than threshold null values/ less than threshold nonnull values
    data_df = data_df[data_df['Value'].notnull()]

    # TODO split into two dataframes, PARAM=1 and PARAM=2. Then join the two dataframes
    # rename into 1: Daily Discharge (m3/s) and 2: Daily Water Level (m)
    data_df1 = data_df[data_df['PARAM'] == 1]
    data_df1 = data_df1[['Station ID','Date','Value','SYM']]
    data_df1.rename(columns={"Value":"Daily Discharge", "SYM":"SYM1"}, inplace=True)
    data_df2 = data_df[data_df['PARAM'] == 2]
    data_df2 = data_df2[['Station ID','Date','Value','SYM']]
    data_df2.rename(columns={"Value":"Daily Water Level","SYM":"SYM2"}, inplace=True)

    data_df = pd.merge(data_df1, data_df2, on=["Station ID", "Date"])

    # Our data at this point has to form |Station ID|PARAM|Date|Value|SYM|
    # However, 'stationID' is an internal numbering with no meaning. Our weather data is going to
    # be based on a 'Climate ID' so ideally we can combine the stationID with additional metadata
    # so that we can then correctly match the stations between 'stationID' and 'Climate ID'
    # Station ID's have the form ##AA### while the official Climate ID's are a 7 digit number assigned
    # by the Meteorological Service of Canada to a site where official weather observations are taken,
    # and serves as a permanent, unqiue identifier.
    # Our Station ID metadata includes latitude and longitude, so if we are unable to find a perfect match
    # between BC hydrometric and MSC sites we can find one that is closest.

    # read our metadata file
    meta_df = pd.read_csv("bc_station_metadata/metadata_20241115T0843.csv")
    # change header "Station Number" -> "Station ID"
    meta_df.rename(columns={"Station Number":"Station ID"}, inplace=True)

    # TODO combine data_df with meta_df so each station has lat/long as well as additional values
    combined_df = data_df.merge(meta_df, on="Station ID", sort=True)

    # do some manual filtering of stations with data over too small a period of time
    combined_data = combined_data[combined_data['Station ID'] != '08GA026']
    combined_data = combined_data[combined_data['Station ID'] != '08HE001']
    combined_data = combined_data[combined_data['Station ID'] != '08LG070']
    combined_data = combined_data[combined_data['Station ID'] != '08LF023']
    combined_data = combined_data[combined_data['Station ID'] != '08KE018']
    combined_data = combined_data[combined_data['Station ID'] != '08ND021']
    combined_data = combined_data[combined_data['Station ID'] != '08MF035']
    combined_data = combined_data[combined_data['Station ID'] != '08CE005']
    combined_data = combined_data[combined_data['Station ID'] != '07ED001']
    combined_data = combined_data[combined_data['Station ID'] != '08GD010']
    combined_data = combined_data[combined_data['Station ID'] != '08MG028']
    combined_data = combined_data[combined_data['Station ID'] != '08NK030']
    combined_data = combined_data[combined_data['Station ID'] != '09AA006']
    combined_data = combined_data[combined_data['Station ID'] != '08LF033']
    combined_data = combined_data[combined_data['Station ID'] != '08HD035']
    combined_data = combined_data[combined_data['Station ID'] != '08FA002']
    combined_data = combined_data[combined_data['Station ID'] != '08MD013']
    combined_data = combined_data[combined_data['Station ID'] != '08KH001']
    combined_data = combined_data[combined_data['Station ID'] != '08PA012']
    combined_data = combined_data[combined_data['Station ID'] != '08LD001']
    combined_data = combined_data[combined_data['Station ID'] != '08EG012']
    combined_data = combined_data[combined_data['Station ID'] != '08EG019']
    combined_data = combined_data[combined_data['Station ID'] != '07FC003']
    combined_data = combined_data[combined_data['Station ID'] != '08NP003']
    combined_data = combined_data[combined_data['Station ID'] != '07FD019']
    combined_data = combined_data[combined_data['Station ID'] != '08LF094']
    combined_data = combined_data[combined_data['Station ID'] != '10CD004']
    combined_data = combined_data[combined_data['Station ID'] != '08NM146']
    combined_data = combined_data[combined_data['Station ID'] != '08KE024']
    combined_data = combined_data[combined_data['Station ID'] != '08LG056']
    combined_data = combined_data[combined_data['Station ID'] != '08KH019']
    combined_data = combined_data[combined_data['Station ID'] != '08KA009']
    combined_data = combined_data[combined_data['Station ID'] != '08KH010']
    combined_data = combined_data[combined_data['Station ID'] != '10CD005']
    combined_data = combined_data[combined_data['Station ID'] != '07FC001']
    combined_data = combined_data[combined_data['Station ID'] != '08MF005']

    # TODO Check for continuity within our dates, decide how to fill in missing values
    
    # pivot_data = ['Daily Discharge','SYM1','Daily Water Level','SYM2','Station Name',
    #                  'Province','Status','Latitude','Longitude','Year From','Year To',
    #                  'Gross Drainage Area (km2)','Effective Drainage Area (km2)',
    #                  'Data Type']
    # # TODO pivot into correct table format
    # pivot_df = combined_df.pivot(columns="Station ID", index="Date")
    # print(pivot_df.head())
    # # TODO drop rows with not enough data, then find the longest continuous data range
    # pivot_df.dropna(axis=0, how='all', inplace=True)

    # # TODO join data with climate data




    combined_df.to_csv("combined_data.csv", index=False)

if __name__=='__main__':
    main()

