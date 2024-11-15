# python3 clean_data.py raw_hydrometric_data clean_hydrometric_data
import os
import sys
import csv
import gzip


def main():
    raw_data_path = sys.argv[1]
    clean_data_path = sys.argv[2]

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

                print(f'Input file {filename} has {len(reader)} non-null rows.')
                count += len(reader)
                for row in reader:
                    writer.writerow(row)

    print(f'Total lines of non-null input data: {count}')


if __name__=='__main__':
    main()

