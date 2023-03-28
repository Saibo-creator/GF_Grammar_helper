#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : abs_grammar.py
# @Date : 2023-03-24-15-22
# @Project: GFLM
# @AUTHOR : Saibo Geng
# @Desc :
import hashlib
import os
import pdb
import re
from typing import List, Union
from src.config.config import TEMPLATE_DIR

from transformers import AutoTokenizer

from src.base_grammar import Grammar, TemplateTokenGrammarBuilder


class GenieCrtGrammarBuilder(TemplateTokenGrammarBuilder):
    template = os.path.join(TEMPLATE_DIR, "v0", "GenieCrtTemplate.txt")

    def __init__(self):
        super().__init__()

    def build(self, abs_grammar_name: str, entities_or_path: Union[List[str], str],
              relations_or_path: Union[List[str], str], tokenizer_or_path, crt_grammar_name=None, literal=False) -> Grammar:
        grammar: str = self.read_template()
        if crt_grammar_name is None:
            crt_grammar_name = f"{abs_grammar_name}Crt"
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_or_path) if isinstance(tokenizer_or_path,
                                                                                   str) else tokenizer_or_path
        entities = self.read_jsonl(entities_or_path) if isinstance(entities_or_path, str) else entities_or_path
        relations = self.read_jsonl(relations_or_path) if isinstance(relations_or_path, str) else relations_or_path

        formatted_grammar: str = grammar.format(abs_grammar_name=abs_grammar_name, crt_grammar_name=crt_grammar_name,
                                                entity_lin_str=self.batch_get_decoding_lin(tokenizer, entities=entities, literal=literal),
                                                rel_lin_str=self.batch_get_decoding_lin(tokenizer, relations=relations, literal=literal))
        return Grammar(formatted_grammar, name=crt_grammar_name)


    def batch_get_decoding_lin(self, tokenizer, entities: List[str] = None, relations: List[str] = None,literal=False) -> str:
        if entities:
            return "".join(
                [self.get_entity_or_rel_decoding_lin(entity=entity, tokenizer=tokenizer, literal=literal) for entity in entities])
        elif relations:
            return "".join([self.get_entity_or_rel_decoding_lin(rel=rel, tokenizer=tokenizer, literal=literal) for rel in relations])
        else:
            raise ValueError("No input provided!")

    def get_entity_or_rel_decoding_lin(self, entity: str = None, rel: str = None, tokenizer=None, literal=False) -> str:
        """Germany = "ger"++"many"; France = "fra"++"nce"; UK = "u"++"k"; US = "u"++"s";"""
        if entity:
            func_name: str = self.get_tokenization_func_name(entity=entity)
        elif rel:
            func_name: str = self.get_tokenization_func_name(rel=rel)
            entity = rel
        else:
            raise ValueError("No input provided!")
        assert tokenizer is not None, "tokenizer is None! This is not allowed!"
        token_ids: List[int] = tokenizer.encode(entity)
        processed_token_ids: List[Union[int, str]] = self.post_process_token_ids(token_ids, tokenizer, literal=literal)
        token_id_in_quotes: List[str] = [f'"{token_id}"' for token_id in processed_token_ids]
        # token_cats: List[str] = [self.token_id2tok_cat(tok_id) for tok_id in token_ids] # tok_0, tok_1, ...
        tokens_concat = " ++ ".join(token_id_in_quotes)
        return f"{func_name}  = {tokens_concat};\n"

