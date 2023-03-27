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
    template = os.path.join(TEMPLATE_DIR, "v1", "GenieCrtTemplate.txt")

    def __init__(self):
        super().__init__()

    def build(self, abs_grammar_name: str, entities_or_path: Union[List[str],str], relations_or_path: Union[List[str],str], tokenizer_or_path, crt_grammar_name=None) -> Grammar:
        grammar: str = self.read_template()
        if crt_grammar_name is None:
            crt_grammar_name = f"{abs_grammar_name}Crt"
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_or_path) if isinstance(tokenizer_or_path, str) else tokenizer_or_path
        entities = self.read_jsonl(entities_or_path) if isinstance(entities_or_path, str) else entities_or_path
        relations = self.read_jsonl(relations_or_path) if isinstance(relations_or_path, str) else relations_or_path
        formatted_grammar: str = grammar.format( abs_grammar_name=abs_grammar_name, crt_grammar_name=crt_grammar_name,
            entire_vocab_token_ids_starting_with_tok=self.get_argument_entire_vocab_token_ids_starting_with_tok(
                tokenizer),
            entities_decoding_lin=self.batch_get_decoding_lin(tokenizer, entities=entities),
            relations_decoding_lin=self.batch_get_decoding_lin(tokenizer, relations=relations),
            tokens_decoding_lin=self.batch_get_decoding_lin(tokenizer, token_ids=tokenizer.vocab.values()))
        return Grammar(formatted_grammar, name=crt_grammar_name)

    def get_argument_entire_vocab_token_ids_starting_with_tok(self, tokenizer):
        "Tok_0, Tok_1, ... Tok_50257: str;"
        return ", ".join([self.token_id2tok_cat(tok_id) for tok_id in tokenizer.vocab.values()])

    def batch_get_decoding_lin(self, tokenizer, entities: List[str] = None, relations: List[str] = None,
                                    token_ids: List[int] = None):
        if entities:
            return "".join([self.get_entity_or_rel_decoding_lin(entity=entity, tokenizer=tokenizer) for entity in entities])
        elif relations:
            return "".join([self.get_entity_or_rel_decoding_lin(rel=rel, tokenizer=tokenizer) for rel in relations])
        else:
            raise ValueError("No input provided!")

    def get_entity_or_rel_decoding_lin(self, entity: str=None, rel:str=None, tokenizer=None) -> str:
        "Germany g e r m a n y = g ++ e ++ r ++ m ++ a ++ n ++ y;"
        "Has h a s = h ++ a ++ s ;"
        if entity:
            func_name: str = self.get_tokenization_func_name(entity=entity)
        elif rel:
            func_name: str = self.get_tokenization_func_name(rel=rel)
            entity = rel
        else:
            raise ValueError("No input provided!")
        assert tokenizer is not None, "tokenizer is None! This is not allowed!"
        token_ids: List[int] = tokenizer.encode(entity)
        token_ids: List[int] = self.post_process_token_ids(token_ids, tokenizer)
        # token_cats: List[str] = [self.token_id2tok_cat(tok_id) for tok_id in token_ids] # tok_0, tok_1, ...
        output_string = " ++ ".join(token_ids)
        return f"{func_name} {input_string} = {output_string};"






def get_lin_for_items(trie_tokens: List[List[str]], save_path=None):
    gf_lines: List[str] = []
    for tokens in trie_tokens:
        gf_lines.append(get_lin_for_item(tokens))
    if save_path is not None:
        with open(save_path, "w") as file:
            file.write("\n".join(gf_lines))
    return gf_lines


def get_lin_for_item(tokens: List[str]) -> str:
    # US = "u" + +"s";
    name = tokens_to_func_name(tokens)
    tokens_with_quotes = [f'"{token}"' for token in tokens]
    template = f"\t\t{name} = {' ++ '.join(tokens_with_quotes)};"
    return template


def get_entities_func(tokens: List[List[str]]) -> str:
    entity_names = []
    for ent_tokens in tokens:
        entity_names.append(tokens_to_func_name(ent_tokens))
    return ", ".join(entity_names)


def generate_abs_grammar(rel_trie, ent_trie, save_path=None):
    template_path = "GF-grammars/templates/GenieAbsTemplate.gf"
    with open(template_path, "r") as file:
        template = file.read().splitlines()

    rel_func: str = get_entities_func(rel_trie) + ": Rel;"
    ent_func: str = get_entities_func(ent_trie) + ": Entity;"

    # replace lines
    template[-2] = rel_func
    template[-3] = ent_func

    if save_path is not None:
        with open(save_path, "w") as file:
            file.write("\n".join(template))
    return template


def generate_crt_grammar(rel_trie, ent_trie, save_path=None):
    template_path = "GF-grammars/templates/GenieCrtTemplate.gf"
    with open(template_path, "r") as file:
        template = file.read().splitlines()

    rel_lins: List[str] = get_lin_for_items(rel_trie)
    ent_lins: List[str] = get_lin_for_items(ent_trie)

    # replace lines
    template[-2] = "\n".join(rel_lins)
    template[-3] = "\n".join(ent_lins)

    if save_path is not None:
        with open(save_path, "w") as file:
            file.write("\n".join(template))
    return template


def tokens_to_func_name(tokens: List[str]):
    input_string = "_".join(tokens)

    # Generate a SHA-256 hash object from the input string
    hash_object = hashlib.sha256(input_string.encode())

    # Get the hash value as a string of hexadecimal digits
    hash_string = hash_object.hexdigest()
    hash_string_without_numbers = re.sub(r'\d', '', hash_string)

    return hash_string_without_numbers.capitalize()
