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
from typing import List, Union

from src.utils import get_hashed_name


class Grammar:

    def __init__(self, grammar: str, name:str, meta: dict = None):
        self.grammar = grammar
        self.name = name
        self.meta = meta

    def save(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        "if path exists, ask user to overwrite or not."
        self._save(output_dir=output_dir)

    def _save(self, output_dir: str):
        grammar_fpath = os.path.join(output_dir, self.name + ".gf")
        with open(grammar_fpath, "w") as file:
            file.write(self.grammar)

        if self.meta is not None:
            meta_fpath = os.path.join(output_dir, self.name + "_meta" +".json")
            with open(meta_fpath, "w") as file:
                json.dump(self.meta, file)



class AbsCrtGrammarPair:

    def __init__(self, abs_grammar: Grammar, crt_grammar: Grammar):
        self.abs_grammar = abs_grammar
        self.crt_grammar = crt_grammar
        self.name = self.abs_grammar.name

    def save(self, output_dir: str):
        dir = os.path.join(output_dir, self.name)
        os.makedirs(output_dir, exist_ok=True)
        if os.path.exists(dir):
            overwrite = input(f"Grammar {dir} already exists. Overwrite? (y/n)")
            if overwrite == "y":
                self._save(dir)
            else:
                print("Aborted.")
        else:
            self._save(dir)

    def _save(self, output_dir: str):
        self.abs_grammar.save(output_dir)
        self.crt_grammar.save(output_dir)


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

    def post_process_token_ids(self, token_ids: List[int], tokenizer, literal: bool = False) -> List[Union[int,str]]:
        "remove_bos=True, remove_eos=False"
        if token_ids[0] == tokenizer.bos_token_id:
            token_ids = token_ids[1:]
        if literal:
            token_ids = [tokenizer.decode(token_id) for token_id in token_ids]
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


