#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : base_grammar.py
# @Date : 2023-03-25-15-16
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import json
import os
import pdb
import subprocess
from abc import abstractmethod
from typing import List, Union

from src.utils import get_hashed_name
from src.config.config import PGF_ASSET_DIR


class Grammar:

    def __init__(self, grammar: str, name:str, meta: dict = None):
        self.grammar = grammar
        self.name = name
        self.meta = meta

    def save(self, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        "if path exists, ask user to overwrite or not."
        grammar_fpath = self._save(output_dir=output_dir)
        return grammar_fpath

    def _save(self, output_dir: str):
        grammar_fpath = os.path.join(output_dir, self.name + ".gf")
        with open(grammar_fpath, "w") as file:
            file.write(self.grammar)

        if self.meta is not None:
            meta_fpath = os.path.join(output_dir, self.name + "_meta" +".json")
            with open(meta_fpath, "w") as file:
                json.dump(self.meta, file)

        return grammar_fpath



class AbsCrtGrammarPair:

    def __init__(self, abs_grammar: Grammar, crt_grammar: Grammar):
        self.abs_grammar = abs_grammar
        self.crt_grammar = crt_grammar
        self.name = self.abs_grammar.name

    def save(self, output_dir: str, compile: bool = False, only_keep_pgf: bool = False, individual_dir: bool = True):
        # if not individual_dir, then save to output_dir, this will make all grammars in one dir(including intermediate grammars)
        if individual_dir:
            dir = os.path.join(output_dir, self.name)
        else:
            dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        if os.path.exists(dir) and individual_dir:
            # if the goal is to save all grammars in one dir, then we don't need to ask user to overwrite
            overwrite = input(f"Grammar {dir} already exists. Overwrite? (y/n)")
            if overwrite == "y":
                self._save(dir, compile=compile)
            else:
                print("Aborted.")
        else:
            self._save(dir, compile=compile)
        if only_keep_pgf:
            self._remove_gf_file(dir)

    def _save(self, output_dir: str, compile: bool = False):
        abs_grammar_fpath = self.abs_grammar.save(output_dir)
        crt_grammar_fpath = self.crt_grammar.save(output_dir)
        if compile:
            pgf_fpath = self.compile_grammar(crt_grammar_fpath, output_dir)

    def _remove_gf_file(self, dir: str):
        files = os.listdir(dir)
        for file in files:
            if not file.endswith(".pgf"):
                os.remove(os.path.join(dir, file))



    @staticmethod
    def compile_grammar(crt_grammar_fpath: str, output_dir: str, verbose: bool = True):
        """
        Compile the grammar to .gfo file.
        """
        cmd = f"gf -make {crt_grammar_fpath}"
        if verbose:
            print("Compiling grammar...")
            print(cmd)
        subprocess.run(cmd, shell=True, cwd=output_dir)
        pgf_fpath = crt_grammar_fpath.replace(".gf", ".pgf").replace("Crt", "")

        return pgf_fpath




class TemplateTokenGrammarBuilder:

    # used to indent the grammar
    INDENT = " "*4

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

    @property
    @abstractmethod
    def grammar_prefix(self):
        """
        This enforce the subclass to define a template property.
        we define an abstract base class Animal that has a name property defined as an abstract method using the @property and @abstractmethod decorators.
        This means that any subclass of Animal must define a name property or method, or it will raise a TypeError when an instance is created.
        """
        pass

    @property
    @abstractmethod
    def grammar_suffix(self):
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

    def dump_jsonl(self, entities: List[dict], entities_path: str):
        with open(entities_path, "w") as file:
            for entity in entities:
                json.dumps(entity, file)
                file.write("\n")

    def build(self, **kwargs) -> Grammar:
        raise NotImplementedError

    @staticmethod
    def token_id2tok_cat(token_id: int):
        "Tok_0, Tok_1, ..."
        return f"Tok_{token_id}"

    def post_process_token_ids(self, token_ids: List[int], tokenizer, literal: bool = False, rm_bos=True, rm_eos=False) -> List[Union[int,str]]:
        "remove_bos=True, remove_eos=False"
        if token_ids[0] == tokenizer.bos_token_id and rm_bos:
            token_ids = token_ids[1:]
        if token_ids[-1] == tokenizer.eos_token_id and rm_eos:
            token_ids = token_ids[:-1]
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

    def get_grammar_name(self, base_grammar_name: str, crt=False) -> str:
        """
        FullyExpanded + GenieWiki + Crt
        example: FullyExpandedGenieWikiCrt
        """
        return f"{self.grammar_prefix}{base_grammar_name}" if not crt else f"{self.grammar_prefix}{base_grammar_name}_Crt"

    @staticmethod
    def join_statements_multi_line(statements: List[str]) -> str:
        return f"\n{TemplateTokenGrammarBuilder.INDENT}".join(statements)


    def get_marker_tokens(self, marker:str, tokenizer, literal=False, rm_bos=True, rm_eos=False):
        # chunk = "[s]"
        assert marker is not None, "marker is None! This is not allowed!"
        token_ids: List[int] = tokenizer.encode(marker)
        processed_token_ids: List[Union[int, str]] = self.post_process_token_ids(token_ids, literal=literal, tokenizer=tokenizer, rm_bos=rm_bos, rm_eos=rm_eos)
        token_id_in_quotes: List[str] = [f'"{token_id}"' for token_id in processed_token_ids]
        # token_cats: List[str] = [self.token_id2tok_cat(tok_id) for tok_id in token_ids] # tok_0, tok_1, ...
        tokens_concat = " ++ ".join(token_id_in_quotes)
        return tokens_concat
