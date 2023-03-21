#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : gf_complete.py
# @Date : 2023-03-20-16-30
# @Project: GFLM
# @AUTHOR : Saibo Geng
# @Desc :
import os

import pgf
import sys
sys.path.append("../")

if __name__ == '__main__':
    # PGF initialization
    pgf_dir = "GF-grammars/pgf"
    pgf_file = "GenieMinimal.pgf"
    grammar = pgf.readPGF(os.path.join(pgf_dir, pgf_file))
    language = grammar.languages["GenieMinimalBart"]

    completions = language.complete("")
    # iterate until end
    while True:
        try:
            print(next(completions))
        except StopIteration:
            break
