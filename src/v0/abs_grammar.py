#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : abs_grammar.py
# @Date : 2023-03-24-15-22
# @Project: GFLM
# @AUTHOR : Saibo Geng
# @Desc :
import os
import pdb
from typing import List, Union, Dict
from src.config.config import TEMPLATE_DIR

from transformers import AutoTokenizer
import line_profiler

from src.base_grammar import Grammar, TemplateTokenGrammarBuilder
from src.utils import get_hashed_name





class GenieAbsGrammarBuilder(TemplateTokenGrammarBuilder):
    template = os.path.join(TEMPLATE_DIR, "v0", "GenieAbsTemplate.txt")

    def __init__(self):
        super().__init__()


    def build(self, abs_grammar_name: str, entities_or_path: Union[List[str], str],
              relations_or_path: Union[List[str], str], tokenizer_or_path) -> Grammar:
        grammar: str = self.read_template()
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_or_path) if isinstance(tokenizer_or_path,
                                                                                   str) else tokenizer_or_path
        entities: List[str] = self.read_jsonl(entities_or_path) if isinstance(entities_or_path,
                                                                              str) else entities_or_path
        relations: List[str] = self.read_jsonl(relations_or_path) if isinstance(relations_or_path,
                                                                                str) else relations_or_path

        formatted_grammar: str = grammar.format(abs_grammar_name=abs_grammar_name,
                                                entities_str=self.get_entities_str(entities=entities),
                                                relations_str=self.get_relations_str(relations=relations))
        grammar_meta = self.build_meta(entities=entities, relations=relations)
        return Grammar(formatted_grammar, name=abs_grammar_name, meta=grammar_meta)

    def build_entities_ids(self, entities: List[str]) -> Dict[str, str]:
        return {self.get_tokenization_func_name(entity=entity): entity for entity in entities}

    def build_relations_ids(self, relations: List[str]) -> Dict[str, str]:
        return {self.get_tokenization_func_name(rel=relation): relation for relation in relations}

    def build_meta(self, entities: List[str], relations: List[str]):
        entities_ids: dict[str, str] = self.build_entities_ids(entities=entities)
        relations_ids: dict[str, str] = self.build_relations_ids(relations=relations)
        return {"entities": entities_ids, "relations": relations_ids}

    def get_entities_str(self, entities: List[str]) -> str:
        entities_ids: dict[str, str] = self.build_entities_ids(entities=entities)
        return ',\n'.join([f'{entity_key}' for entity_key in entities_ids.keys()])

    def get_relations_str(self, relations: List[str]) -> str:
        relations_ids: dict[str, str] = self.build_relations_ids(relations=relations)
        return ',\n'.join([f'{relation_key}' for relation_key in relations_ids.keys()])

#
# def get_lin_for_items(trie_tokens: List[List[str]], save_path=None):
#     gf_lines: List[str] = []
#     for tokens in trie_tokens:
#         gf_lines.append(get_lin_for_item(tokens))
#     if save_path is not None:
#         with open(save_path, "w") as file:
#             file.write("\n".join(gf_lines))
#     return gf_lines
#
#
# def get_lin_for_item(tokens: List[str]) -> str:
#     # US = "u" + +"s";
#     name = tokens_to_func_name(tokens)
#     tokens_with_quotes = [f'"{token}"' for token in tokens]
#     template = f"\t\t{name} = {' ++ '.join(tokens_with_quotes)};"
#     return template
#
#
# def get_entities_func(tokens: List[List[str]]) -> str:
#     entity_names = []
#     for ent_tokens in tokens:
#         entity_names.append(tokens_to_func_name(ent_tokens))
#     return ", ".join(entity_names)
#
#
# def generate_abs_grammar(rel_trie, ent_trie, save_path=None):
#     template_path = "GF-grammars/templates/GenieAbsTemplate.gf"
#     with open(template_path, "r") as file:
#         template = file.read().splitlines()
#
#     rel_func: str = get_entities_func(rel_trie) + ": Rel;"
#     ent_func: str = get_entities_func(ent_trie) + ": Entity;"
#
#     # replace lines
#     template[-2] = rel_func
#     template[-3] = ent_func
#
#     if save_path is not None:
#         with open(save_path, "w") as file:
#             file.write("\n".join(template))
#     return template
#
#
# def generate_crt_grammar(rel_trie, ent_trie, save_path=None):
#     template_path = "GF-grammars/templates/GenieCrtTemplate.gf"
#     with open(template_path, "r") as file:
#         template = file.read().splitlines()
#
#     rel_lins: List[str] = get_lin_for_items(rel_trie)
#     ent_lins: List[str] = get_lin_for_items(ent_trie)
#
#     # replace lines
#     template[-2] = "\n".join(rel_lins)
#     template[-3] = "\n".join(ent_lins)
#
#     if save_path is not None:
#         with open(save_path, "w") as file:
#             file.write("\n".join(template))
#     return template
#
#
# def tokens_to_func_name(tokens: List[str]):
#     input_string = "_".join(tokens)
#
#     return get_hashed_name(input_string)
