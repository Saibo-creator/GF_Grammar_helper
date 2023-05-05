#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : time_complexity.py
# @Date : 2023-04-14-11-27
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :

import argparse
import os
import time

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from tqdm import tqdm

from genie.constrained_generation.trie import Trie


def measure_speed(trie, num_repeat=6, max_seq_len=1024, benchmark_dir="benchmark"):

    times_matrix = np.zeros((num_repeat, max_seq_len))
    for i in tqdm(range(num_repeat), desc="Repeat"):
        prefix_indices = []
        for j in tqdm(range(max_seq_len), desc="Seq Len", leave=False):
            start_time = time.time()
            completions = trie.get(prefix_indices)
            # randomly choose one completion
            if len(completions) > 0:
                idx = np.random.randint(0, len(completions))
                next_token_id = completions[idx]
                end_time = time.time()
                times_matrix[i][j] = round(end_time - start_time, 4)
                prefix_indices.append(next_token_id)

    # save the time as csv
    # mkdir if not exist
    time_id = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    session_name = f"{time_id}"
    benchmark_session_dir = os.path.join(benchmark_dir, session_name)
    os.makedirs(benchmark_session_dir, exist_ok=True)
    csv_fpath = os.path.join(benchmark_session_dir, f"time.csv")
    os.makedirs(os.path.dirname(csv_fpath), exist_ok=True)
    np.savetxt(csv_fpath, times_matrix, delimiter=",")

    return csv_fpath


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
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--trie_pkl_path', type=str, default='entity_trie.pickle')
    arg_parser.add_argument('--num_repeat', type=int, default=6)
    arg_parser.add_argument('--max_seq_len', type=int, default=1024)
    args = arg_parser.parse_args()

    trie = Trie.load(args.trie_pkl_path)

    csv_fpath = measure_speed(trie, num_repeat=args.num_repeat, max_seq_len=args.max_seq_len)
    plot_time_complexity(csv_fpath)
