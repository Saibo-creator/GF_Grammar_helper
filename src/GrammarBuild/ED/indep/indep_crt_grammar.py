#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : indep_abs_grammar.py
# @Date : 2023-03-24-15-22
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os
import pdb
from abc import ABC, abstractmethod
from typing import List, Union

from tqdm import tqdm

from src.config.config import TEMPLATE_DIR

from transformers import AutoTokenizer

from src.GrammarBuild.base_grammar import Grammar
from src.GrammarBuild.grammar_builder import TemplateTokenGrammarBuilder


class ED_IndepMinimalCrtGrammarBuilder(TemplateTokenGrammarBuilder, ABC):

    template = os.path.join(TEMPLATE_DIR, "ED", "indep", "minimal", "ED-Indep-Minimal-CrtTemplate.hs")
    grammar_prefix = "" # "SubjectCollapsed"

    Open_bracket_marker = "["
    Close_bracket_marker = "]"


    def __init__(self, tokenizer_or_path:str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)

    def build(self, base_grammar_name: str,  **kwargs) -> Grammar:
        grammar: str = self.read_template()
        entities_or_path: Union[List[str], str, List[List[str]]]= kwargs["entities_or_path"]
        crt_grammar_name = kwargs.get("crt_grammar_name", None)
        abs_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name)
        if crt_grammar_name is None:
            crt_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name, crt=True)
        entities = self.read_jsonl(entities_or_path) if isinstance(entities_or_path, str) else entities_or_path
        formatted_grammar_plain_text: str = grammar.format(abs_grammar_name=abs_grammar_name, crt_grammar_name=crt_grammar_name,
                                                bog_tokens="[]",
                                                eog_tokens=f'"{self.tokenizer.encode(self.tokenizer.eos_token, add_special_tokens=False)[0]}"',
                                                open_bracket_tokens=self.get_entity_tokens(self.Open_bracket_marker, rm_eos=True),
                                                close_bracket_tokens=self.get_entity_tokens(self.Close_bracket_marker, rm_eos=True),
                                                Materialize_Entities=self.batch_get_decoding_linearization_rules(entities=entities, rm_eos=True, rm_bos=True))
        return Grammar(formatted_grammar_plain_text, name=crt_grammar_name)


    def batch_get_decoding_linearization_rules(self, entities: List[str] = None, relations: List[str] = None, rm_bos=True, rm_eos=False) -> str:
        if entities:
            statements = [self.get_entity_or_rel_decoding_linearization_rule(entity=entity, rm_bos=rm_bos, rm_eos=rm_eos) for entity in tqdm(entities, desc="get linearization for entities")]
        elif relations:
            statements = [self.get_entity_or_rel_decoding_linearization_rule(rel=rel, rm_bos=rm_bos, rm_eos=rm_eos) for rel in tqdm(relations, desc="get linearization for relations")]
        else:
            raise ValueError("No input_ids provided!")
        return self.join_statements_multi_line(statements)

    def get_entity_or_rel_decoding_linearization_rule(self, entity: str = None, rel: str = None, rm_bos=True, rm_eos=False) -> str:
        """Germany = "ger"++"many"; France = "fra"++"nce"; UK = "u"++"k"; US = "u"++"s";"""
        if entity:
            func_name: str = self.get_tokenization_func_name(entity=entity)
        elif rel:
            func_name: str = self.get_tokenization_func_name(rel=rel)
            entity = rel
        else:
            raise ValueError("No input_ids provided!")
        token_ids: List[int] = self.tokenizer.encode(entity)
        processed_token_ids: List[Union[int, str]] = self.post_process_token_ids(token_ids, rm_bos=rm_bos, rm_eos=rm_eos)
        token_id_in_quotes: List[str] = [f'"{token_id}"' for token_id in processed_token_ids]
        # token_cats: List[str] = [self.token_id2tok_cat(tok_id) for tok_id in token_ids] # tok_0, tok_1, ...
        tokens_concat = " ++ ".join(token_id_in_quotes)
        return f"{func_name}  = {tokens_concat};"


