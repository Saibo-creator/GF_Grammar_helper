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
from tqdm import tqdm

from src.constrained_generation.pgf import HttpPgf
from src.config.config import PGF_ASSET_DIR, BENCHMARK_DIR
from src.benchmark.visualization import plot_time_complexity


def measure_speed(pgf_name='FullyExpandedGenieWiki', port=41296, pgf_dir=PGF_ASSET_DIR, num_repeat=6, max_seq_len=1024, tokens2exclude=None):
    pgf_fname = pgf_name + ".pgf"
    pgf = HttpPgf(pgf=pgf_fname, port=port, root_dir=pgf_dir)
    tokens2exclude = tokens2exclude or []

    times_matrix = np.zeros((num_repeat, max_seq_len))
    for i in tqdm(range(num_repeat), desc="Repeat"):
        prefix = ""
        for j in tqdm(range(max_seq_len), desc="Seq Len", leave=False):
            start_time = time.time()
            completions = pgf.complete(prefix)
            # randomly choose one completion
            if len(completions) > 0:
                idx = np.random.randint(0, len(completions))
                next_token_id = completions[idx]
                while next_token_id in tokens2exclude:
                    idx = np.random.randint(0, len(completions))
                    next_token_id = completions[idx]
                end_time = time.time()
                times_matrix[i][j] = round(end_time - start_time, 4)
                prefix += " " + next_token_id

    # save the time as csv
    # mkdir if not exist
    time_id = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    session_name = f"{pgf_name}-{time_id}"
    benchmark_session_dir = os.path.join(BENCHMARK_DIR, session_name)
    if not os.path.exists(BENCHMARK_DIR):
        os.mkdir(benchmark_session_dir)
    csv_fpath = os.path.join(benchmark_session_dir, f"time.csv")
    os.makedirs(os.path.dirname(csv_fpath), exist_ok=True)
    np.savetxt(csv_fpath, times_matrix, delimiter=",")

    return csv_fpath


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--pgf', type=str, default='FullyExpandedGenieWiki')
    arg_parser.add_argument('--port', type=int, default=41296)
    arg_parser.add_argument('--pgf_dir', type=str, default=PGF_ASSET_DIR)
    arg_parser.add_argument('--num_repeat', type=int, default=6)
    arg_parser.add_argument('--max_seq_len', type=int, default=1024)
    arg_parser.add_argument('--tokens2exclude', type=list, default=[])
    args = arg_parser.parse_args()

    csv_fpath = measure_speed(pgf_name=args.pgf, port=args.port, pgf_dir=args.pgf_dir, num_repeat=args.num_repeat,
                              max_seq_len=args.max_seq_len, tokens2exclude=args.tokens2exclude)
    plot_time_complexity(csv_fpath)
