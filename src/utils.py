#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : utils
# @Date : 2023-03-24-15-24
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import hashlib
import json
import os
import re
from typing import List

import transformers


def read_json(json_path):
    with open(json_path, "r") as f:
        trie = json.load(f)
    return trie


def read_jsonl(entities_path: str) -> List[str]:
    # entities_path is a json file
    entities = []
    with open(entities_path, "r") as file:
        for line in file:
            json_obj = json.loads(line)
            entities.append(json_obj)
    return entities


def nested_merge_json(dict1, dict2):

    """
    # Example
        dict1 = {
            'a': 1,
            'b': {'x': 10, 'y': 20},
            'c': 3
        }

        dict2 = {
            'a': 4,
            'b': {'y': 25, 'z': 30},
            'd': 5
        }

        result = deep_merge(dict1, dict2)
        print(result)
    """
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            nested_merge_json(dict1[key], value)
        else:
            dict1[key] = value
    return dict1


def load_gf_template(template_path) -> str:
    with open(template_path, "r") as f:
        gf_template = f.read()
    return gf_template


def entity_num2str(entities_num_path, save=False, output_path=None):
    """
    trie_as_tokens("./genie-data/small/wiki-ner-relation.json")
    """
    tokenizer = transformers.BartTokenizer.from_pretrained("martinjosifoski/genie-rw")
    # vocab = {v: k for k, v in tokenizer.get_vocab().items()}
    entity_str_tokens = []
    entity_num_tokens = read_json(entities_num_path)
    for token_ids in entity_num_tokens:
        # remove eos: "</s>"
        token_ids = (
            token_ids[:-1] if token_ids[-1] == tokenizer.eos_token_id else token_ids
        )
        tokens = [tokenizer.decode(token_id).strip() for token_id in token_ids]
        entity_str_tokens.append(tokens)
    if output_path is None:
        output_path = os.path.splitext(entities_num_path)[0] + ".tokens"
    if save:
        with open(output_path, "w") as f:
            json.dump(entity_str_tokens, f)
    return entity_str_tokens


def get_hashed_name(string: str, no_numbers: bool = False) -> str:

    # # Generate a SHA-256 hash object from the input string
    # hash_object = hashlib.sha256(string.encode())
    #
    # # Get the hash value as a string of hexadecimal digits
    hash_string = generate_id(string)

    if no_numbers:
        hash_string_without_numbers = re.sub(r"\d", "", hash_string)
        return hash_string_without_numbers.capitalize()

    return hash_string.capitalize()


def generate_id(string):
    # Generate a hash object using md5
    hash_object = hashlib.md5(string.encode())

    # Get the hash value as a string of hexadecimal digits
    hash_string = hash_object.hexdigest()

    # Return the first 12 characters of the hash string
    # this should be enough to avoid collisions, as long as the number of strings is less than 1 billion
    # c.f. https://stackoverflow.com/questions/30561096/chance-of-a-duplicate-hash-when-using-first-8-characters-of-sha1
    return hash_string[:12]
