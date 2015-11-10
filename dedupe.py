# coding: utf-8

import pandas as pd
import glob
import os
import sys


# Import multiple CSV files (with the same columns) and concatenate into one dataframe
# http://stackoverflow.com/questions/20906474/
# Prompt the user for the directory containing the CSVs - this can be a relative or absolute path

inputdirectory = raw_input("\nWhat's the folder name or path that contains your CSV files?\n")

try:
    allFiles = glob.glob(os.path.join(inputdirectory, "*.csv"))
    combined = pd.DataFrame()
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_, index_col=None, header=0, encoding='utf-8')
        list_.append(df)
    combined = pd.concat(list_)
except:
    print("\nSorry, there aren't any CSV files there.\n")
    sys.exit(1)


# Renumber the combined index (not important in this case, as we'll drop the index later when writing the output CSV, but otherwise avoids confusion with duplicate index numbers)
combined.reset_index(inplace=True, drop=True)


# Sort by the 'title' column (this is for the content explorer CSVs, but could be an input variable instead)
# If there's no such column, ignore the error and carry on without sorting
# .sort is deprecated, use .sort_values from pandas version 0.17
# Note that this puts titles with straight quotes at the top but curly quotes at the bottom
try:
    combined.sort_values('title', inplace=True)
except:
    pass


# Drop duplicate rows
deduplicated = combined.drop_duplicates()


# Write CSV to /output/ subdirectory using relative path
# First check whether the subdirectory already exists, and create it if necessary
# http://stackoverflow.com/questions/273192/
outputdirectory = "output"
try:
    os.makedirs(outputdirectory)
except OSError:
    if not os.path.isdir(outputdirectory):
        raise

# Set the filename for the output CSV, using the input directory name with the current date and time
# .basename gets just the last part of the directory path
directoryname = os.path.basename(inputdirectory)
filename = '{}-{}.csv'.format(directoryname.replace(" ","-"), pd.datetime.now().strftime("%Y%m%d-%H%M"))

# This simpler version uses just the date and the time as the filename
# filename = pd.datetime.now().strftime("%Y%m%d-%H%M.csv")

# Write the CSV to the output filepath
# 'w' is the file mode - https://docs.python.org/2/tutorial/inputoutput.html#reading-and-writing-files
# index=False removes the numbered index column
# encoding defaults to 'ascii' on Python 2 and 'utf-8' on Python 3
outputpath = os.path.join(outputdirectory, filename)
deduplicated.to_csv(open(outputpath, 'w'), index=False, encoding='utf-8')
print('\nThank you. Your combined and deduplicated file is: \n{}\n'.format(os.path.abspath(outputpath)))
