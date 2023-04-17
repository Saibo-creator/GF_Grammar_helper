#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : abs_grammar.py
# @Date : 2023-03-24-15-22
# @Project: GFLM
# @AUTHOR : Saibo Geng
# @Desc :
import os
from typing import List, Union
from src.config.config import TEMPLATE_DIR

from transformers import AutoTokenizer

from src.GrammarBuild.base_grammar import Grammar, TemplateTokenGrammarBuilder


class GenieAbsGrammarBuilder(TemplateTokenGrammarBuilder):
    template = os.path.join(TEMPLATE_DIR, "v1", "GenieFullyExpandedAbsTemplate.txt")
    grammar_prefix = ""

    def __init__(self):
        super().__init__()

    def build(self, base_grammar_name:str, entities_or_path: Union[List[str], str], relations_or_path: Union[List[str], str], tokenizer_or_path) -> Grammar:
        grammar: str = self.read_template()
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_or_path) if isinstance(tokenizer_or_path, str) else tokenizer_or_path
        entities = self.read_jsonl(entities_or_path) if isinstance(entities_or_path, str) else entities_or_path
        relations = self.read_jsonl(relations_or_path) if isinstance(relations_or_path, str) else relations_or_path
        abs_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name)
        formatted_grammar: str = grammar.format(abs_grammar_name=abs_grammar_name,
                                                entire_vocab_token_ids_starting_with_tok=self.get_argument_entire_vocab_token_ids_starting_with_tok(
                tokenizer),
                                                entities_tokenization_funcs=self.batch_get_tokenization_func(tokenizer, entities=entities),
                                                relations_tokenization_funcs=self.batch_get_tokenization_func(tokenizer, relations=relations),
                                                tokens_tokenization_funcs=self.batch_get_tokenization_func(tokenizer, token_ids=tokenizer.vocab.values()))
        return Grammar(formatted_grammar, name=abs_grammar_name)

    def get_argument_entire_vocab_token_ids_starting_with_tok(self, tokenizer):
        "Tok_0; Tok_1; ... Tok_50257;"
        return "".join([self.token_id2tok_cat(tok_id) + "; " for tok_id in tokenizer.vocab.values()])


    def batch_get_tokenization_func(self, tokenizer, entities: List[str] = None, relations: List[str] = None,
                                    token_ids: List[int] = None):
        if entities:
            statements = [self.get_entity_tokenization_func(entity, tokenizer) for entity in entities]
        elif relations:
            statements = [self.get_relation_tokenization_func(rel, tokenizer) for rel in relations]
        elif token_ids:
            statements = [self.get_token_tokenization_func(tok_id) for tok_id in token_ids]
        else:
            raise ValueError("No input provided!")

        return self.join_statements_multi_line(statements=statements)

    def get_entity_tokenization_func(self, entity: str, tokenizer):
        "Germany: G -> E -> R -> M -> A -> N -> Y -> Entity;"
        func_name: str = self.get_tokenization_func_name(entity=entity)
        token_ids: List[int] = tokenizer.encode(entity)
        token_ids: List[int] = self.post_process_token_ids(token_ids, tokenizer)
        token_cats: List[str] = [self.token_id2tok_cat(tok_id) for tok_id in token_ids]
        return f"{func_name} : {' -> '.join(token_cats)} -> Entity;"

    def get_relation_tokenization_func(self, relation: str, tokenizer):
        "Has: H -> A -> S -> Rel;"
        func_name: str = self.get_tokenization_func_name(rel=relation)
        token_ids: List[int] = tokenizer.encode(relation)
        token_ids: List[int] = self.post_process_token_ids(token_ids, tokenizer)
        token_cats: List[str] = [self.token_id2tok_cat(tok_id) for tok_id in token_ids]
        return f"{func_name} : {' -> '.join(token_cats)} -> Rel;"

    def get_token_tokenization_func(self, token_id: int):
        "Tok_0: T -> O -> K -> Tok_0;"
        func_name: str = self.get_tokenization_func_name(token_id=token_id)
        token_cat: str = self.token_id2tok_cat(token_id)
        return f"{func_name} : {token_cat};"
