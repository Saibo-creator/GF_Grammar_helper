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
from src.config.config import TEMPLATE_DIR

from transformers import AutoTokenizer

from src.GrammarBuild.base_grammar import Grammar, TemplateTokenGrammarBuilder


class GenieCrtGrammarBuilder(TemplateTokenGrammarBuilder, ABC):



    def __init__(self):
        super().__init__()

    def build(self, base_grammar_name: str, entities_or_path: Union[List[str], str],
              relations_or_path: Union[List[str], str], tokenizer_or_path, crt_grammar_name=None, literal=False) -> Grammar:
        grammar: str = self.read_template()
        abs_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name)
        if crt_grammar_name is None:
            crt_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name, crt=True)
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_or_path) if isinstance(tokenizer_or_path,
                                                                                   str) else tokenizer_or_path
        entities = self.read_jsonl(entities_or_path) if isinstance(entities_or_path, str) else entities_or_path
        relations = self.read_jsonl(relations_or_path) if isinstance(relations_or_path, str) else relations_or_path
        formatted_grammar: str = grammar.format(abs_grammar_name=abs_grammar_name, crt_grammar_name=crt_grammar_name,
                                                bog_tokens=self.get_marker_tokens(tokenizer.bos_token, tokenizer, literal, rm_eos=True,rm_bos=False),
                                                eog_tokens=self.get_marker_tokens(tokenizer.eos_token, tokenizer, literal, rm_eos=True),
                                                Subject_marker_tokens = self.get_marker_tokens(self.Subject_marker, tokenizer, literal=literal, rm_eos=True),
                                                Relation_marker_tokens = self.get_marker_tokens(self.Relation_marker, tokenizer, literal=literal, rm_eos=True),
                                                Object_marker_tokens = self.get_marker_tokens(self.Object_marker, tokenizer, literal=literal, rm_eos=True),
                                                Triplet_ending_marker_tokens = self.get_marker_tokens(self.Triplet_ending_marker, tokenizer, literal=literal, rm_eos=True),
                                                entity_lin_str=self.batch_get_decoding_lin(tokenizer, entities=entities, literal=literal,rm_eos=True, rm_bos=True),
                                                rel_lin_str=self.batch_get_decoding_lin(tokenizer, relations=relations, literal=literal,rm_eos=True, rm_bos=True))
        return Grammar(formatted_grammar, name=crt_grammar_name)


    def batch_get_decoding_lin(self, tokenizer, entities: List[str] = None, relations: List[str] = None,literal=False, rm_bos=True, rm_eos=False) -> str:
        if entities:
            statements = [self.get_entity_or_rel_decoding_lin(entity=entity, tokenizer=tokenizer, literal=literal, rm_bos=rm_bos, rm_eos=rm_eos) for entity in entities]
        elif relations:
            statements = [self.get_entity_or_rel_decoding_lin(rel=rel, tokenizer=tokenizer, literal=literal, rm_bos=rm_bos, rm_eos=rm_eos) for rel in relations]
        else:
            raise ValueError("No input provided!")
        return self.join_statements_multi_line(statements)

    def get_entity_or_rel_decoding_lin(self, entity: str = None, rel: str = None, tokenizer=None, literal=False, rm_bos=True, rm_eos=False) -> str:
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
        processed_token_ids: List[Union[int, str]] = self.post_process_token_ids(token_ids, tokenizer, literal=literal, rm_bos=rm_bos, rm_eos=rm_eos)
        token_id_in_quotes: List[str] = [f'"{token_id}"' for token_id in processed_token_ids]
        # token_cats: List[str] = [self.token_id2tok_cat(tok_id) for tok_id in token_ids] # tok_0, tok_1, ...
        tokens_concat = " ++ ".join(token_id_in_quotes)
        return f"{func_name}  = {tokens_concat};"

    def get_marker_tokens(self, marker:str, tokenizer, literal=False, rm_bos=True, rm_eos=False):
        # chunk = "[s]"
        assert marker is not None, "marker is None! This is not allowed!"
        token_ids: List[int] = tokenizer.encode(marker)
        processed_token_ids: List[Union[int, str]] = self.post_process_token_ids(token_ids, literal=literal, tokenizer=tokenizer, rm_bos=rm_bos, rm_eos=rm_eos)
        token_id_in_quotes: List[str] = [f'"{token_id}"' for token_id in processed_token_ids]
        # token_cats: List[str] = [self.token_id2tok_cat(tok_id) for tok_id in token_ids] # tok_0, tok_1, ...
        tokens_concat = " ++ ".join(token_id_in_quotes)
        return tokens_concat

    @property
    @abstractmethod
    def Subject_marker(self):
        """
        This enforce the subclass to define a template property.
        we define an abstract base class Animal that has a name property defined as an abstract method using the @property and @abstractmethod decorators.
        This means that any subclass of Animal must define a name property or method, or it will raise a TypeError when an instance is created.
        """
        pass

    @property
    @abstractmethod
    def Relation_marker(self):
        """
        This enforce the subclass to define a template property.
        we define an abstract base class Animal that has a name property defined as an abstract method using the @property and @abstractmethod decorators.
        This means that any subclass of Animal must define a name property or method, or it will raise a TypeError when an instance is created.
        """
        pass

    @property
    @abstractmethod
    def Object_marker(self):
        """
        This enforce the subclass to define a template property.
        we define an abstract base class Animal that has a name property defined as an abstract method using the @property and @abstractmethod decorators.
        This means that any subclass of Animal must define a name property or method, or it will raise a TypeError when an instance is created.
        """
        pass

    @property
    @abstractmethod
    def Triplet_ending_marker(self):
        """
        This enforce the subclass to define a template property.
        we define an abstract base class Animal that has a name property defined as an abstract method using the @property and @abstractmethod decorators.
        This means that any subclass of Animal must define a name property or method, or it will raise a TypeError when an instance is created.
        """
        pass


class GenieFullyExpandedCrtGrammarBuilder(GenieCrtGrammarBuilder):

    template = os.path.join(TEMPLATE_DIR, "v2", "GenieFullyExpandedCrtTemplate.txt")
    grammar_prefix = "FullyExpanded"
    grammar_suffix = ""

    Subject_marker = "[s]"
    Relation_marker = "[r]"
    Object_marker = "[o]"
    Triplet_ending_marker = "[e]"

    Default_BOS_marker = "0"


class GenieFullyExpandedEtCrtGrammarBuilder(GenieCrtGrammarBuilder):

    template = os.path.join(TEMPLATE_DIR, "v2", "GenieFullyExpandedCrtTemplate.txt")
    grammar_prefix = "FullyExpandedEt"
    grammar_suffix = ""

    Subject_marker = "[s]"
    Relation_marker = "[r]"
    Object_marker = "[o]"
    Triplet_ending_marker = "[et]"

    Default_BOS_marker = "0"



class GenieSubjectCollapsedCrtGrammarBuilder(GenieCrtGrammarBuilder):

    template = os.path.join(TEMPLATE_DIR, "v2", "GenieSubjectCollapsedCrtTemplate.txt")
    grammar_prefix = "SubjectCollapsed"
    grammar_suffix = ""

    Subject_marker = "[s]"
    Relation_marker = "[r]"
    Object_marker = "[o]"
    Triplet_ending_marker = "[e]"

    Default_BOS_marker = "0"