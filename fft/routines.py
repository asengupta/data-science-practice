# # Library Imports
import getopt
import logging
import math
import sys
import warnings

import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from matplotlib import pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import periodogram

# # Constants
# A bunch of constants are set up so that strings don't clutter the source everywhere.
from sklearn.preprocessing import MinMaxScaler

DEFAULT_DATASET_LOCATION = "~/Downloads"
DEFAULT_DATA_CSV_FILENAME = "ecg1.csv"
VALUE_FIELD = "value"
VALUES_FIELD = "values"
COLUMNS_TO_SCALE = []

def with_dummies_builder(categorical_column, metadata):
    return lambda dataset: with_dummy_variables(categorical_column, dataset, metadata)


# This utility function pretty prints a dataframe for output
def log_df(dataframe_label, dataframe, num_rows=10):
    heading(dataframe_label)
    logging.info(dataframe.head(num_rows).to_string())


# This function actually performs conversion of categorical variables to dummy variables using the parsed metadata
def with_dummy_variables(categorical_column, dataset, metadata):
    metadata_entry = [x for x in metadata if x["name"] == categorical_column][0]
    raw_entries = list(map(lambda v: v[VALUE_FIELD], metadata_entry[VALUES_FIELD]))
    dummy_columns = pd.get_dummies(dataset.pop(categorical_column), prefix=categorical_column, drop_first=True)
    log_df(f"{categorical_column} after Renaming of Dummy Variables", dummy_columns)
    dataset_with_dummy_columns = pd.concat([dataset, dummy_columns], axis=1)
    log_df(f"All Columns after Renaming of Dummy Variables of {categorical_column}", dataset_with_dummy_columns)
    return dataset_with_dummy_columns

def log_mode(columns, frame):
    for column in columns:
        logging.debug(f"Most Common {column}: {frame[column].mode()[0]}")


def log_median(columns, frame):
    for column in columns:
        logging.debug(f"Most Common {column}: {frame[column].median()}")

# This function imputes any missing data by using the mode for categorical variables
def impute(categorical_columns, numerical_columns, frame):
    for categorical_column in categorical_columns:
        frame[categorical_column] = frame[categorical_column].fillna(
            frame[categorical_column].mode()[0])
    for categorical_column in numerical_columns:
        frame[categorical_column] = frame[categorical_column].fillna(
            frame[categorical_column].median())

    return frame



def replace(column, valueToReplace, replacingValue, dataset):
    dataset[column] = np.where((dataset[column] == valueToReplace), replacingValue, dataset[column])
    logging.info(dataset[column].unique())
    return dataset


# This function converts specified columns into ordinal variables, with a choice of ascending or descending
def mark_as_ordered(column, dataset, metadata, descending=False):
    metadata_entry = [x for x in metadata if x["name"] == column][0]
    print(metadata_entry)
    raw_entries = list(map(lambda v: v[VALUE_FIELD], metadata_entry[VALUES_FIELD]))
    raw_ordering = list(range(1, len(raw_entries) + 1))
    correct_ordering = raw_ordering if not descending else raw_ordering[-1::-1]
    mapping = {raw_entries[i]: correct_ordering[i] for i in range(len(raw_ordering))}
    heading(f"Converting {column} into ordered")
    logging.info(f"Original Unique Values: {dataset[column].unique()}")
    dataset[column] = dataset[column].map(mapping)
    logging.info(f"New Unique Values: {dataset[column].unique()}")
    return dataset



def scale(training_dataset):
    training_data_scaler = MinMaxScaler()
    training_dataset[COLUMNS_TO_SCALE] = training_data_scaler.fit_transform(training_dataset[COLUMNS_TO_SCALE])
    log_df("Training Dataset after Scaling", training_dataset)
    return training_dataset, training_data_scaler


# # Entry Point for CRISPR
#  This function is the entry point for the entire CRISPR process. This is called by `main()`

def study(raw_data):
    logging.debug(raw_data.head().to_string())
    logging.debug(raw_data.shape)
    logging.debug(raw_data.columns)
    for column in raw_data.columns:
        logging.info(column)

# # Utility Functions
# This function reads command line arguments, one of which can be the input data set
def parse_commandline_options(args):
    print(f"args are: {args}")
    file_csv = f"{DEFAULT_DATASET_LOCATION}/{DEFAULT_DATA_CSV_FILENAME}"

    try:
        options, arguments = getopt.getopt(args, "i:hf:", ["input=", "help"])
        for option, argument in options:
            if option in ("-h", "--help"):
                print_help_text()
            elif option in ("-i", "--input"):
                file_csv = argument
            else:
                print(f"{option} was not recognised as a valid option")
                print_help_text()
                print("Allowing to continue since Jupyter notebook passes in other command-line options")
        return file_csv
    except getopt.GetoptError as e:
        sys.stderr.write("%s: %s\n" % (args[0], e.msg))
        print_help_text()
        exit(2)


# This function prints out the help text if either explicitly requested or in case of wrong input
def print_help_text():
    print("USAGE: python housing-price-main.py [{-i |--input=}<housing-pricing-csv>]")


# This function overrides Jupyter's default logger so that we can output things based on our formatting preferences
def setup_logging():
    warnings.filterwarnings("ignore")
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logger = logging.getLogger()
    formatter = logging.Formatter('%(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ch)


# This function reads the csv data set
def read_csv(csv):
    return pd.read_csv(csv, low_memory=False)


# This utility function pretty prints a heading for output
def heading(heading_text):
    logging.info("-" * 100)
    logging.info(heading_text)
    logging.info("-" * 100)


# # Main Entry Point: main()
# This function is the entry point of the script
def main():
    setup_logging()
    study(read_csv(parse_commandline_options(sys.argv[1:])))


main()
