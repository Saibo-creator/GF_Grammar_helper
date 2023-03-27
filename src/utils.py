#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : utils
# @Date : 2023-03-24-15-24
# @Project: GFLM
# @AUTHOR : Saibo Geng
# @Desc :
import hashlib
import json
import os
import re

import transformers


def read_json(json_path):
    with open(json_path, 'r') as f:
        trie = json.load(f)
    return trie


def load_gf_template(template_path) -> str:
    with open(template_path, 'r') as f:
        gf_template = f.read()
    return gf_template


def entity_num2str(entities_num_path, save=False, output_path=None):
    """
    trie_as_tokens("./genie-data/small/wiki-ner-relation.json")
    """
    tokenizer = transformers.BartTokenizer.from_pretrained('martinjosifoski/genie-rw')
    # vocab = {v: k for k, v in tokenizer.get_vocab().items()}
    entity_str_tokens = []
    entity_num_tokens = read_json(entities_num_path)
    for token_ids in entity_num_tokens:
        # remove eos: "</s>"
        token_ids = token_ids[:-1] if token_ids[-1] == tokenizer.eos_token_id else token_ids
        tokens = [tokenizer.decode(token_id).strip() for token_id in token_ids]
        entity_str_tokens.append(tokens)
    if output_path is None:
        output_path = os.path.splitext(entities_num_path)[0] + '.tokens'
    if save:
        with open(output_path, 'w') as f:
            json.dump(entity_str_tokens, f)
    return entity_str_tokens


def get_hashed_name(string: str):

    # Generate a SHA-256 hash object from the input string
    hash_object = hashlib.sha256(string.encode())

    # Get the hash value as a string of hexadecimal digits
    hash_string = hash_object.hexdigest()
    hash_string_without_numbers = re.sub(r'\d', '', hash_string)

    return hash_string_without_numbers.capitalize()