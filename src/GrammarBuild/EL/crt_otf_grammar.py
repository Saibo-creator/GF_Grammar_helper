#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : abs_grammar.py
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

from src.GrammarBuild.base_grammar import Grammar, TemplateTokenGrammarBuilder
from .crt_grammar import ELCrtGrammarBuilder


class ELotfCrtGrammarBuilder(ELCrtGrammarBuilder, ABC):

    template = os.path.join(TEMPLATE_DIR, "EL", "EL-OTF-CrtTemplate-w-mention.txt")
    grammar_prefix = ""


    Open_bracket_marker = "["
    Close_bracket_marker = "]"

    Default_BOS_marker = "0"

    def __init__(self, tokenizer_or_path:str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)

    def build(self, base_grammar_name: str, entities_or_path: Union[List[str], str], crt_grammar_name=None, literal=False, mention:str=None) -> Grammar:
        assert mention is not None, "mention should not be None"
        grammar: str = self.read_template()
        abs_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name)
        if crt_grammar_name is None:
            crt_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name, crt=True)
        entities = self.read_jsonl(entities_or_path) if isinstance(entities_or_path, str) else entities_or_path
        formatted_grammar_plain_text: str = grammar.format(abs_grammar_name=abs_grammar_name, crt_grammar_name=crt_grammar_name,
                                                           bog_tokens="[]",  #self.get_entity_tokens(tokenizer.bos_token, tokenizer, literal, rm_eos=True,rm_bos=False)
                                                           eog_tokens= f'"{self.tokenizer.encode(self.tokenizer.eos_token, add_special_tokens=False)[0]}"',  # "2" for llama and "1" for T5
                                                           mention_tokens= self.get_entity_tokens(entity=mention,  rm_eos=True),
                                                           open_bracket_tokens = self.get_entity_tokens(self.Open_bracket_marker,  rm_eos=True),
                                                           close_bracket_tokens = self.get_entity_tokens(self.Close_bracket_marker,  rm_eos=True),
                                                           entity_lin_str=self.batch_get_decoding_linearization_rules(entities=entities,  rm_eos=True, rm_bos=True))
        return Grammar(formatted_grammar_plain_text, name=crt_grammar_name)




#
# class ELotfCrtGrammarBuilder(TemplateTokenGrammarBuilder, ABC):
#
#     template = os.path.join(TEMPLATE_DIR, "EL", "EL-OTF-CrtTemplate.hs")
#     grammar_prefix = ""
#
#
#     Default_BOS_marker = "0"
#
#     def __init__(self):
#         super().__init__()
#
#     def build(self, base_grammar_name: str, mention:str, entities_or_path: Union[List[str], str],
#               tokenizer_or_path, crt_grammar_name=None, literal=False) -> Grammar:
#         grammar: str = self.read_template()
#         abs_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name)
#         if crt_grammar_name is None:
#             crt_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name, crt=True)
#         tokenizer = AutoTokenizer.from_pretrained(tokenizer_or_path, use_fast=False) if isinstance(tokenizer_or_path,
#                                                                                    str) else tokenizer_or_path
#         entities = self.read_jsonl(entities_or_path) if isinstance(entities_or_path, str) else entities_or_path
#         formatted_grammar: str = grammar.format(abs_grammar_name=abs_grammar_name, crt_grammar_name=crt_grammar_name,
#                                                 bog_tokens="[]",#self.get_entity_tokens(tokenizer.bos_token, tokenizer, literal, rm_eos=True,rm_bos=False)
#                                                 eog_tokens= f'"{tokenizer.encode(tokenizer.eos_token, add_special_tokens=False)[0]}"', # "2" for llama and "1" for T5
#                                                 entity_lin_str=self.batch_get_decoding_linearization_rules(tokenizer, entities=entities, rm_eos=True, rm_bos=True))
#         return Grammar(formatted_grammar, name=crt_grammar_name)
#
#
#     def batch_get_decoding_linearization_rules(self, tokenizer, entities: List[str] = None, relations: List[str] = None,literal=False, rm_bos=True, rm_eos=False) -> str:
#         if entities:
#             statements = [self.get_entity_or_rel_decoding_linearization_rule(entity=entity, tokenizer=tokenizer,  rm_bos=rm_bos, rm_eos=rm_eos) for entity in tqdm(entities, desc="get linearization for entities")]
#         elif relations:
#             statements = [self.get_entity_or_rel_decoding_linearization_rule(rel=rel, tokenizer=tokenizer,  rm_bos=rm_bos, rm_eos=rm_eos) for rel in tqdm(relations, desc="get linearization for relations")]
#         else:
#             raise ValueError("No input_ids provided!")
#         return self.join_statements_multi_line(statements)
#
#     def get_entity_or_rel_decoding_linearization_rule(self, entity: str = None, rel: str = None, tokenizer=None, literal=False, rm_bos=True, rm_eos=False) -> str:
#         """Germany = "ger"++"many"; France = "fra"++"nce"; UK = "u"++"k"; US = "u"++"s";"""
#         if entity:
#             func_name: str = self.get_tokenization_func_name(entity=entity)
#         elif rel:
#             func_name: str = self.get_tokenization_func_name(rel=rel)
#             entity = rel
#         else:
#             raise ValueError("No input_ids provided!")
#         assert tokenizer is not None, "tokenizer is None! This is not allowed!"
#         token_ids: List[int] = tokenizer.encode(entity)
#         processed_token_ids: List[Union[int, str]] = self.post_process_token_ids(token_ids, tokenizer,  rm_bos=rm_bos, rm_eos=rm_eos)
#         token_id_in_quotes: List[str] = [f'"{token_id}"' for token_id in processed_token_ids]
#         # token_cats: List[str] = [self.token_id2tok_cat(tok_id) for tok_id in token_ids] # tok_0, tok_1, ...
#         tokens_concat = " ++ ".join(token_id_in_quotes)
#         return f"{func_name}  = {tokens_concat};"
#
#     def get_entity_tokens(self, entity:str, tokenizer, literal=False, rm_bos=True, rm_eos=False):
#         # chunk = "[s]"
#         assert entity is not None, "entity is None! This is not allowed!"
#         token_ids: List[int] = tokenizer.encode(entity)
#         processed_token_ids: List[Union[int, str]] = self.post_process_token_ids(token_ids,  tokenizer=tokenizer, rm_bos=rm_bos, rm_eos=rm_eos)
#         token_id_in_quotes: List[str] = [f'"{token_id}"' for token_id in processed_token_ids]
#         # token_cats: List[str] = [self.token_id2tok_cat(tok_id) for tok_id in token_ids] # tok_0, tok_1, ...
#         tokens_concat = " ++ ".join(token_id_in_quotes)
#         return tokens_concat

