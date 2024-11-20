import pandas as pd



def main():

    # read our data into a dataframe
    df = pd.read_csv("clean_hydrometric_data/aggregateData.csv", skiprows=1)
    # get rid of the annoying ' ID' column header
    df.rename(columns={" ID":"ID"}, inplace=True)



    print(df['ID'].unique())
    print(len(df['ID'].unique()))




if __name__ == '__main__':
    main()