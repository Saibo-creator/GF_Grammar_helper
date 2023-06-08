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




