#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : config.py
# @Date : 2023-03-25-14-44
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :

import os

# Get the absolute path of the directory containing the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Set the ROOT_DIR variable to the parent directory of the script directory
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))


# Set the asset directory
ASSET_DIR = os.path.join(ROOT_DIR, "asset")
# Set the gf directory
GF_ASSET_DIR = os.path.join(ASSET_DIR, "GF-grammars", "gf")
# Set the asset directory
PGF_ASSET_DIR = os.path.join(ASSET_DIR, "GF-grammars", "pgf")

#AUTO GENERATED GF GRAMMARS
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")
GF_AUTO_GEN_GF_DIR = os.path.join(OUTPUT_DIR, "grammars", "autogen")
PGF_AUTO_GEN_DIR = os.path.join(OUTPUT_DIR, "grammars", "autogen")
# Benchmarks
BENCHMARK_DIR = os.path.join(OUTPUT_DIR, "benchmarks")


# Set the resource directory
RES_DIR = os.path.join(ROOT_DIR, "res")
# Set the templates directory
TEMPLATE_DIR = os.path.join(RES_DIR, "GF-grammars", "templates")

# entity file paths
TRAINING_DATA_PATH ={
    "wiki-ner": {
        "entity":os.path.join(RES_DIR, "genie-data", "jsonl", "small", "wiki_ner_entity_trie_original_strings.jsonl"),
        "relation":os.path.join(RES_DIR, "genie-data", "jsonl", "small", "wiki_ner_relation_trie_original_strings.jsonl"),
    },
    "rebel": {
        "entity": os.path.join(RES_DIR, "genie-data", "jsonl", "large", "rebel_entity_trie_original_strings.jsonl"),
        "relation": os.path.join(RES_DIR, "genie-data", "jsonl", "large", "rebel_relation_trie_original_strings.jsonl"),
    }
}

