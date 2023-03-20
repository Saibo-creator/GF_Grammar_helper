#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : trie2grammar.py
# @Date : 2023-03-17-17-19
# @Project: GF-LM
# @AUTHOR : Saibo Geng
# @Desc :

import argparse
import os
import re
import sys
import time

import hashlib
import json
from collections import defaultdict
from typing import List

import transformers
import numpy as np
from utils import convert_punctuation_to_characters, replace_numbers_with_letters


def read_trie(trie_path):
    with open(trie_path, 'r') as f:
        trie = json.load(f)
    return trie


def tokens_to_func_name(tokens: List[str]):
    # return tokenizer.decode(tokens).strip().replace(tokenizer.eos_token, '').replace(' ', '_')
    # return replace_numbers_with_letters(convert_punctuation_to_characters("_".join(tokens).capitalize()))


    # Define the input string
    input_string = "_".join(tokens)

    # Generate a SHA-256 hash object from the input string
    hash_object = hashlib.sha256(input_string.encode())

    # Get the hash value as a string of hexadecimal digits
    hash_string = hash_object.hexdigest()
    hash_string_without_numbers = re.sub(r'\d', '', hash_string)

    return hash_string_without_numbers.capitalize()

def load_trie(trie_path, save=False, save_path=None):
    """
    trie_as_tokens("./genie-data/small/relation_trie.json")
    """
    tokenizer = transformers.BartTokenizer.from_pretrained('martinjosifoski/genie-rw')
    # vocab = {v: k for k, v in tokenizer.get_vocab().items()}
    trie_tokens = []
    trie = read_trie(trie_path)
    for token_ids in trie:
        # remove eos: "</s>"
        token_ids = token_ids[:-1] if token_ids[-1] == tokenizer.eos_token_id else token_ids
        tokens = [tokenizer.decode(token_id).strip() for token_id in token_ids]
        trie_tokens.append(tokens)
    if save_path is None:
        save_path = os.path.splitext(trie_path)[0] + '.tokens'
    if save:
        with open(save_path, 'w') as f:
            json.dump(trie_tokens, f)
    return trie_tokens


def get_lin_for_items(trie_tokens: List[List[str]], save_path=None):
    gf_lines: List[str] = []
    for tokens in trie_tokens:
        gf_lines.append(get_lin_for_item(tokens))
    if save_path is not None:
        with open(save_path, "w") as file:
            file.write("\n".join(gf_lines))
    return gf_lines


def get_lin_for_item(tokens: List[str]) -> str:
    # US = "u" + +"s";
    name = tokens_to_func_name(tokens)
    tokens_with_quotes = [f'"{token}"' for token in tokens]
    template = f"\t\t{name} = {' ++ '.join(tokens_with_quotes)};"
    return template


def get_entities_func(tokens: List[List[str]]) -> str:
    entity_names = []
    for ent_tokens in tokens:
        entity_names.append(tokens_to_func_name(ent_tokens))
    return ", ".join(entity_names)


def generate_abs_grammar(rel_trie, ent_trie, save_path=None):
    template_path = "GF-grammars/template/GenieAbsTemplate.gf"
    with open(template_path, "r") as file:
        template = file.read().splitlines()

    rel_func: str = get_entities_func(rel_trie)+": Rel;"
    ent_func: str = get_entities_func(ent_trie)+": Entity;"

    # replace lines
    template[-2] = rel_func
    template[-3] = ent_func

    if save_path is not None:
        with open(save_path, "w") as file:
            file.write("\n".join(template))
    return template


def generate_crt_grammar(rel_trie, ent_trie, save_path=None):
    template_path = "GF-grammars/template/GenieCrtTemplate.gf"
    with open(template_path, "r") as file:
        template = file.read().splitlines()

    rel_lins: List[str] = get_lin_for_items(rel_trie)
    ent_lins: List[str] = get_lin_for_items(ent_trie)

    # replace lines
    template[-2] = "\n".join(rel_lins)
    template[-3] = "\n".join(ent_lins)

    if save_path is not None:
        with open(save_path, "w") as file:
            file.write("\n".join(template))
    return template

if __name__ == '__main__':

    tokenizer = transformers.BartTokenizer.from_pretrained('martinjosifoski/genie-rw')

    with open("GF-grammars/GenieBart.gf","r") as file:
        line_list = file.read().splitlines()
