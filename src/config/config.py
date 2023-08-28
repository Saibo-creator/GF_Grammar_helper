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
# Set the asset directory
GRAMMAR_JSON_CONFIG_ASSET_DIR = os.path.join(ASSET_DIR, "grammar_json")

# AUTO GENERATED GF GRAMMARS
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")
# GF_AUTO_GEN_GF_DIR = os.path.join(OUTPUT_DIR, "grammars", "autogen")
NEW_GF_AUTO_GEN_GF_DIR = os.path.join(OUTPUT_DIR, "grammars", "autogen", "gf")
# PGF_AUTO_GEN_DIR = os.path.join(OUTPUT_DIR, "grammars", "autogen")
NEW_PGF_AUTO_GEN_DIR = os.path.join(OUTPUT_DIR, "grammars", "autogen", "pgf")
# Benchmarks
BENCHMARK_DIR = os.path.join(OUTPUT_DIR, "benchmarks")


# Set the resource directory
DATA_DIR = os.path.join(ROOT_DIR, "data")
# Set the templates directory
TEMPLATE_DIR = os.path.join(ASSET_DIR, "templates")

# entity file paths
IE_DATA_PATH = {
    "KB": {
        "wiki_ner": {
            "entity": os.path.join(
                DATA_DIR,
                "IE",
                "KB",
                "small",
                "wiki_ner_entity_trie_original_strings.jsonl",
            ),
            "relation": os.path.join(
                DATA_DIR,
                "IE",
                "KB",
                "small",
                "wiki_ner_relation_trie_original_strings.jsonl",
            ),
        },
        "rebel": {
            "entity": os.path.join(
                DATA_DIR,
                "IE",
                "KB",
                "large",
                "rebel_entity_trie_original_strings.jsonl",
            ),
            "relation": os.path.join(
                DATA_DIR,
                "IE",
                "KB",
                "large",
                "rebel_relation_trie_original_strings.jsonl",
            ),
        },
        "rebel_medium": {
            "entity": os.path.join(
                DATA_DIR,
                "IE",
                "KB",
                "medium",
                "llama_constrained_rebel_entity_names.jsonl",
            ),
            "relation": os.path.join(
                DATA_DIR,
                "IE",
                "KB",
                "medium",
                "llama_constrained_rebel_relation_names.jsonl",
            ),
        },
    },
    "Tasks": {
        "wikinre": os.path.join(DATA_DIR, "IE", "Tasks", "wikinre.jsonl"),
    },
}

ED_DATA_PATH = {
    "KB": {
        "kilt_wiki": {
            "entity": os.path.join(
                DATA_DIR, "ED", "KB", "kilt_wikipedia_entities_1K.jsonl"
            ),
        },
        "YAGO_KB": {
            "entity": os.path.join(DATA_DIR, "ED", "KB", "YAGO-KB.jsonl"),
        },
    },
    "Tasks": {
        "ace2004": os.path.join(
            DATA_DIR, "ED", "Tasks", "ace2004-test-processed-short.jsonl"
        ),
        "aida": os.path.join(
            DATA_DIR, "ED", "Tasks", "aida-test-processed-short.jsonl"
        ),
        "aquaint": os.path.join(
            DATA_DIR, "ED", "Tasks", "aquaint-test-processed-short.jsonl"
        ),
        "clueweb": os.path.join(
            DATA_DIR, "ED", "Tasks", "clueweb-test-processed-short.jsonl"
        ),
        "msnbc": os.path.join(
            DATA_DIR, "ED", "Tasks", "msnbc-test-processed-short.jsonl"
        ),
        "wiki": os.path.join(
            DATA_DIR, "ED", "Tasks", "wiki-test-processed-short.jsonl"
        ),
        "wikiLinksNED": os.path.join(
            DATA_DIR, "ED", "Tasks", "wikiLinksNED-test-processed-short.jsonl"
        ),
    },
}

CP_DATA_PATH = {
    "KB": None,
    "Tasks": {
        "ptb": os.path.join(DATA_DIR, "CP", "Tasks", "ptb-test-processed.jsonl"),
    },
}


DATA_PATHS = {
    "IE": IE_DATA_PATH,
    "ED": ED_DATA_PATH,
    "CP": CP_DATA_PATH,
}
