#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : test_pgf.py
# @Date : 2023-03-29-12-28
# @Project: GFLM
# @AUTHOR : Saibo Geng
# @Desc :

from src.constrained_generation.pgf import ServerPgf
from src.config.config import ASSET_PGF_DIR

if __name__ == '__main__':
    pgf_dir = ASSET_PGF_DIR
    pgf = ServerPgf(pgf='FoodRepeat.pgf', port=41296, root_dir=pgf_dir)
    print(pgf.complete('this fish'))
    print (pgf.complete('this fish is'))
    print (pgf.complete('this fish is warm'))

    pgf = ServerPgf(pgf='GenieWikiNum.pgf', port=41296, root_dir=pgf_dir)
    print(pgf.complete(''))
    print(pgf.complete('<'))
    print(pgf.complete('< 8481'))
    print(pgf.complete('< 8481 9851'))