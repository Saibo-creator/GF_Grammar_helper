#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : test_gen_abs_grmr
# @Date : 2023-03-25-13-28
# @Project: GFLM
# @AUTHOR : Saibo Geng
# @Desc :
import os

from src.abs_grammar import GenieAbsGrammarBuilder
from src.config.config import ASSET_GF_DIR,RES_DIR
from src.crt_grammar import GenieCrtGrammarBuilder

if __name__ == '__main__':
    abs_builder = GenieAbsGrammarBuilder()
    crt_builder = GenieCrtGrammarBuilder()

    case = 2

    if case == 1:
        abs_grammar = abs_builder.build(abs_grammar_name="Genie" ,entities_or_path=["entity1", "entity2"], relations_or_path=["relation1", "relation2"], tokenizer_or_path="martinjosifoski/genie-rw")
        crt_grammar = crt_builder.build(abs_grammar_name="Genie", entities_or_path=["entity1", "entity2"], relations_or_path =["relation1", "relation2"], tokenizer_or_path="martinjosifoski/genie-rw")


    elif case == 2:
        entities_path = os.path.join(RES_DIR, "genie-data", "jsonl", "small", "wiki_ner_entity_trie_original_strings.jsonl")
        relations_path = os.path.join(RES_DIR, "genie-data", "jsonl", "small", "wiki_ner_relation_trie_original_strings.jsonl")
        abs_grammar = abs_builder.build(abs_grammar_name="GenieWiki", entities_or_path=entities_path, relations_or_path=relations_path, tokenizer_or_path="martinjosifoski/genie-rw")
        crt_grammar = crt_builder.build(abs_grammar_name="GenieWiki", entities_or_path=entities_path, relations_or_path=relations_path, tokenizer_or_path="martinjosifoski/genie-rw")
    else:
        raise ValueError("case must be 1 or 2.")

    abs_grammar.save(output_dir=ASSET_GF_DIR)
    crt_grammar.save(output_dir=ASSET_GF_DIR)
