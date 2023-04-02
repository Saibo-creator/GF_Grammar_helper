#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : entity_num2str.py
# @Date : 2023-03-24-15-21
# @Project: GFLM
# @AUTHOR : Saibo Geng
# @Desc :
import os
import sys

from src import entity_num2str

sys.path.append("..")

DATA_DIR = "../res/genie-data"

if __name__ == '__main__':
    rel_trie = entity_num2str(os.path.join(DATA_DIR, "small", "wiki-ner-relation-num.json"), save=True,
                              output_path=os.path.join(DATA_DIR, "small", "wiki-ner-relation-str.json"))
    ent_trie = entity_num2str(os.path.join(DATA_DIR, "small", "wiki-ner-entity-num.json"), save=True,
                              output_path=os.path.join(DATA_DIR, "small", "wiki-ner-entity-str.json"))