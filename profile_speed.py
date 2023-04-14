#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : profile_speed.py
# @Date : 2023-04-02-19-00
# @Project: GFLM
# @AUTHOR : Saibo Geng
# @Desc :
import pdb
import time

import numpy as np

from src.constrained_generation.pgf import ServerPgf
from src.config.config import ASSET_PGF_DIR

if __name__ == '__main__':
    pgf_dir = ASSET_PGF_DIR

    pgf = ServerPgf(pgf='FullyExpandedGenieWiki.pgf', port=41296, root_dir=pgf_dir)

    num_repeat = 4
    max_seq_len = 156
    times = np.zeros((num_repeat, max_seq_len))
    for i in range(max_seq_len):
        prefix = ""
        for j in range(num_repeat):
            start_time = time.time()
            completions = pgf.complete(prefix)
            # randomly choose one completion
            if len(completions) > 0:
                idx = np.random.randint(0, len(completions))
                next_token_id = completions[idx]
                end_time = time.time()
                times[i][j] = round(end_time - start_time,4)
                prefix += " " + next_token_id
                print(prefix)

    # save the time as csv
    np.savetxt("time.csv", times, delimiter=",")


    print(pgf.complete(''))
    print(pgf.complete('<'))
    print(pgf.complete('< 8481'))
    print(pgf.complete('< 8481 9851'))
