#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : run_grammar_autocomplete(outdated).py
# @Date : 2023-03-29-12-28
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
from time import sleep

from src.constrained_generation.pgf import HttpPgf
from src.config.config import PGF_ASSET_DIR

if __name__ == "__main__":
    pgf_dir = PGF_ASSET_DIR
    pgf = HttpPgf(pgf="FoodRepeat.pgf", port=41396, root_dir=pgf_dir)
    sleep(1000)
    print(pgf.complete(""))
    # print(pgf.complete('this fish'))
    # print (pgf.complete('this fish is'))
    # print (pgf.complete('this fish is warm'))

    # pgf = HttpPgf(pgf='GenieWikiNum.pgf', port=41396, root_dir=pgf_dir)
    # print(pgf.complete(''))
    # print(pgf.complete('<'))
    # print(pgf.complete('< 8481'))
    # print(pgf.complete('< 8481 9851'))
