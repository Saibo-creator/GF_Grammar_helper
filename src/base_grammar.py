#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : base_grammar.py
# @Date : 2023-03-25-15-16
# @Project: GFLM
# @AUTHOR : Saibo Geng
# @Desc :
import json
import os
import pdb
from abc import abstractmethod
from typing import List

from src.utils import get_hashed_name


class Grammar:

    def __init__(self, grammar: str, name:str, meta: dict = None):
        self.grammar = grammar
        self.name = name
        self.meta = meta

    def save(self, output_dir: str):
        output_path = os.path.join(output_dir, self.name + ".gf")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        "if path exists, ask user to overwrite or not."
        if os.path.exists(output_path):
            overwrite = input(f"File {output_path} already exists. Overwrite? (y/n)")
            if overwrite == "y":
                with open(output_path, "w") as file:
                    file.write(self.grammar)
            else:
                print("Aborted.")
        else:
            with open(output_path, "w") as file:
                file.write(self.grammar)


class TemplateTokenGrammarBuilder:

    def __init__(self):
        pass

    @property
    @abstractmethod
    def template(self):
        """
        This enforce the subclass to define a template property.
        we define an abstract base class Animal that has a name property defined as an abstract method using the @property and @abstractmethod decorators.
        This means that any subclass of Animal must define a name property or method, or it will raise a TypeError when an instance is created.
        """
        pass

    def read_template(self) -> str:
        with open(self.template, "r") as file:
            grammar = file.read()
        return grammar

    def read_jsonl(self, entities_path: str) -> List[str]:
        # entities_path is a json file
        entities = []
        with open(entities_path, "r") as file:
            for line in file:
                json_obj = json.loads(line)
                entities.append(json_obj)
        return entities

    def build(self, **kwargs) -> Grammar:
        raise NotImplementedError

    @staticmethod
    def token_id2tok_cat(token_id: int):
        "Tok_0, Tok_1, ..."
        return f"Tok_{token_id}"

    def post_process_token_ids(self, token_ids: List[int], tokenizer):
        "remove_bos=True, remove_eos=False"
        if token_ids[0] == tokenizer.bos_token_id:
            token_ids = token_ids[1:]
        return token_ids

    def get_tokenization_func_name(self, entity: str = None, rel: str = None, token_id: int = None) -> str:
        if entity is not None:
            return "Ent_" + get_hashed_name(entity)
        elif rel is not None:
            return "Rel_" + get_hashed_name(rel)
        elif token_id is not None:
            return "Tok_" + str(token_id) + "_lin"
        else:
            raise ValueError("Must specify either entity or relation or token_id")


