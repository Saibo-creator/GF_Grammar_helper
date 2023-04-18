#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : visualization.py
# @Date : 2023-04-14-10-39
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :

import os
import pandas as pd
import argparse
import matplotlib.pyplot as plt
from src.config.config import BENCHMARK_DIR


def plot_time_complexity(csv_file, save_folder=None, title=None, xlabel="prefix length(# token)", ylabel="infrence time(s)", window_size=19):
    # Load the data from the CSV file
    df = pd.read_csv(csv_file,header=None)

    if save_folder is None:
        save_folder = os.path.dirname(csv_file)

    title = title if title else 'time complexity'

    # Calculate the average, minimum, and maximum values of all time series
    avg_series = df.mean()
    min_series = df.min()
    max_series = df.max()

    smoothed_avg_series = avg_series.rolling(window=window_size).mean()
    smoothed_min_series = min_series.rolling(window=window_size).mean()
    smoothed_max_series = max_series.rolling(window=window_size).mean()

    # Plot the data
    fig, ax = plt.subplots()
    # df.plot(ax=ax, legend=None)
    smoothed_avg_series.plot(ax=ax, label='Average')
    smoothed_min_series.plot(ax=ax, label='Minimum')
    smoothed_max_series.plot(ax=ax, label='Maximum')

    # Add a title and axis labels
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Add a legend
    plt.legend()

    # Save the plot to a file in the specified folder
    filename = os.path.splitext(os.path.basename(csv_file))[0] + '.png'
    filepath = os.path.join(save_folder, filename)
    plt.savefig(filepath)

    # Show the plot
    plt.show()

if __name__ == '__main__':
    default_csv = os.path.join(BENCHMARK_DIR, 'FullyExpandedGenieWiki-2023-04-14-10-37-48', "time.csv")
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--csv', type=str, default=default_csv)
    arg_parser.add_argument('--save_folder', type=str, default=None)
    args = arg_parser.parse_args()

    plot_time_complexity(args.csv, args.save_folder)

