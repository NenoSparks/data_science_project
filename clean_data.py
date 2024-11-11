# python3 clean_data.py inputDirectory outputDirectory
import os
import sys
import pandas as pd


def main():
    raw_data_path = sys.argv[1]
    clean_data_path = sys.argv[2]
    if not os.path.isdir(clean_data_path):
        os.makedirs(clean_data_path)

    # TODO specify a schema so that we dont get a DtypeWawrning of columns having mixed types
    for filename in os.listdir(raw_data_path):
        print(filename)
        df = pd.read_csv(f'raw_data/{filename}', skiprows=1)
        df = df[df['Value'].isnull()]
        
        # df_new.to_csv(f'{clean_data_path}/{filename}')

    print(len(df))

    # concatenate all of my dataframes together and keep only the records from each station that have overlap in dates.
    # for example, if my smallest date range is from 2015-2023, then I should take the subset of all other station records for dates 2015-2023


if __name__=='__main__':
    main()

