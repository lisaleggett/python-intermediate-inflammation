"""Module containing mechanism for calculating standard deviation between datasets.
"""

import glob
import os
import numpy as np

from inflammation import models, views

class CSVDataSource:
    """
    Loads all the inflammation CSV files within a specified directory.
    """
    def __init__(self,dir_path):
        self.dir_path = dir_path

    def load_inflammation_data(self):
        data_directory = os.path.abspath(self.dir_path)
        data_file_paths = sorted(glob.glob(os.path.join(data_directory, 'inflammation*.csv')))
        if len(data_file_paths) == 0:
            raise ValueError(f"No inflammation data CSV files found in path {data_directory}")
        data = map(models.load_csv, data_file_paths) # Load inflammation data from each CSV file
        return list(data) # Return the list of 2D NumPy arrays with inflammation data

class JSONDataSource:
    """
    Loads patient data with inflammation values from JSON files within a specified folder.
    """
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def load_inflammation_data(self):
        data_directory = os.path.abspath(self.dir_path)
        data_file_paths = sorted(glob.glob(os.path.join(data_directory, 'inflammation*.json')))
        if len(data_file_paths) == 0:
            raise ValueError(f"No inflammation JSON files found in path {data_directory}")
        data = map(models.load_json, data_file_paths)
        return list(data)

def compute_standard_deviation_by_day(data):
    means_by_day = map(models.daily_mean, data)
    means_by_day_matrix = np.stack(list(means_by_day))

    daily_standard_deviation = np.std(means_by_day_matrix, axis=0)
    return daily_standard_deviation


def analyse_data(data_source):
    """Calculate the standard deviation by day for all datasets in a source."""
    data = data_source.load_inflammation_data()
    return compute_standard_deviation_by_day(data)



