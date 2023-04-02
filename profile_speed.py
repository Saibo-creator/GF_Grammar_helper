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

    Max = 1000
    prefix = ""
    times = np.zeros((12, 128))
    for i in range(12):
        for j in range(128):
            completions = pgf.complete(prefix)
            # randomly choose one completion
            if len(completions) > 0:
                idx = np.random.randint(0, len(completions))
                start_time = time.time()
                next_token_id = completions[idx]
                end_time = time.time()
                times[i][j] = end_time - start_time
                prefix += " " + next_token_id
                print(prefix)

    # save the time as csv
    np.savetxt("time.csv", times, delimiter=",")


    print(pgf.complete(''))
    print(pgf.complete('<'))
    print(pgf.complete('< 8481'))
    print(pgf.complete('< 8481 9851'))