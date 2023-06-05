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


class GenieCrtGrammarBuilder(TemplateTokenGrammarBuilder, ABC):

    def __init__(self, tokenizer_or_path:str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)


    def build(self, base_grammar_name: str, entities_or_path: Union[List[str], str, List[List[str]]],
              relations_or_path: Union[List[str], str, List[List[str]]], crt_grammar_name=None) -> Grammar:
        grammar: str = self.read_template()
        abs_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name)
        if crt_grammar_name is None:
            crt_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name, crt=True)

        entities = self.read_jsonl(entities_or_path) if isinstance(entities_or_path, str) else entities_or_path
        relations = self.read_jsonl(relations_or_path) if isinstance(relations_or_path, str) else relations_or_path
        formatted_grammar_plain_text: str = grammar.format(abs_grammar_name=abs_grammar_name, crt_grammar_name=crt_grammar_name,
                                                           bog_tokens="[]",  #self.get_entity_tokens(tokenizer.bos_token, tokenizer, literal, rm_eos=True,rm_bos=False)
                                                           eog_tokens= f'"{self.tokenizer.encode(self.tokenizer.eos_token, add_special_tokens=False)[0]}"',  # "2" for llama and "1" for T5
                                                           SubjectMarker_tokens = self.get_entity_tokens(self.SubjectMarker, rm_eos=True),
                                                           RelationMarker_tokens = self.get_entity_tokens(self.RelationMarker, rm_eos=True),
                                                           objectMarker_tokens = self.get_entity_tokens(self.objectMarker, rm_eos=True),
                                                           TripletEndingMarker_tokens = self.get_entity_tokens(self.TripletEndingMarker, rm_eos=True),
                                                           Materialize_Entities=self.batch_get_decoding_linearization_rules( entities=entities, rm_eos=True, rm_bos=True),
                                                           rel_lin_str=self.batch_get_decoding_linearization_rules( relations=relations, rm_eos=True, rm_bos=True))
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


    @property
    @abstractmethod
    def SubjectMarker(self):
        """
        This enforce the subclass to define a template property.
        we define an abstract base class Animal that has a name property defined as an abstract method using the @property and @abstractmethod decorators.
        This means that any subclass of Animal must define a name property or method, or it will raise a TypeError when an instance is created.
        """
        pass

    @property
    @abstractmethod
    def RelationMarker(self):
        """
        This enforce the subclass to define a template property.
        we define an abstract base class Animal that has a name property defined as an abstract method using the @property and @abstractmethod decorators.
        This means that any subclass of Animal must define a name property or method, or it will raise a TypeError when an instance is created.
        """
        pass

    @property
    @abstractmethod
    def objectMarker(self):
        """
        This enforce the subclass to define a template property.
        we define an abstract base class Animal that has a name property defined as an abstract method using the @property and @abstractmethod decorators.
        This means that any subclass of Animal must define a name property or method, or it will raise a TypeError when an instance is created.
        """
        pass

    @property
    @abstractmethod
    def TripletEndingMarker(self):
        """
        This enforce the subclass to define a template property.
        we define an abstract base class Animal that has a name property defined as an abstract method using the @property and @abstractmethod decorators.
        This means that any subclass of Animal must define a name property or method, or it will raise a TypeError when an instance is created.
        """
        pass


class GenieFullyExpandedCrtGrammarBuilder(GenieCrtGrammarBuilder):

    template = os.path.join(TEMPLATE_DIR, "IE", "GenieFullyExpandedCrtTemplate.hs")
    grammar_prefix = "" # "FullyExpanded"

    SubjectMarker = "[s]"
    RelationMarker = "[r]"
    objectMarker = "[o]"
    TripletEndingMarker = "[e]"

    Default_BOS_marker = "0"


class GenieSubjectCollapsedCrtGrammarBuilder(GenieCrtGrammarBuilder):

    template = os.path.join(TEMPLATE_DIR, "IE", "GenieSubjectCollapsedCrtTemplate.hs")
    grammar_prefix = "" # "SubjectCollapsed"

    SubjectMarker = "[s]"
    RelationMarker = "[r]"
    objectMarker = "[o]"
    TripletEndingMarker = "[e]"

    Default_BOS_marker = "0"