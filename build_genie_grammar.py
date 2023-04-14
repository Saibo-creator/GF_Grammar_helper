#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : test_gen_abs_grmr
# @Date : 2023-03-25-13-28
# @Project: GFLM
# @AUTHOR : Saibo Geng
# @Desc :
import os

from src.config.config import AUTO_GEN_GF_DIR,RES_DIR
from src.GrammarBuild.base_grammar import AbsCrtGrammarPair


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", type=int, default=2, help="version of the grammar")
    parser.add_argument("--grammar_name", type=str, default="GenieWiki", help="name of the grammar")
    parser.add_argument("--mode", type=int, default=2, help="case 1: build from entities and relations list; case 2: build from entities and relations file")
    parser.add_argument("--literal", action="store_true", help="whether to use literal grammar")
    args = parser.parse_args()


    version=args.version
    grammar_name = args.grammar_name
    mode = args.mode

    #dynamic import based on version
    GenieAbsGrammarBuilder = __import__(f"src.GrammarBuild.v{version}.abs_grammar",
                                        fromlist=["GenieAbsGrammarBuilder"]).GenieAbsGrammarBuilder
    GenieCrtGrammarBuilder = __import__(f"src.GrammarBuild.v{version}.crt_grammar",
                                        fromlist=["GenieCrtGrammarBuilder"]).GenieCrtGrammarBuilder

    abs_builder = GenieAbsGrammarBuilder()
    crt_builder = GenieCrtGrammarBuilder()

    output_dir = os.path.join(AUTO_GEN_GF_DIR, f"v{version}")

    if mode == 1:
        abs_grammar = abs_builder.build(base_grammar_name=grammar_name, entities_or_path=["entity1", "entity2"], relations_or_path=["relation1", "relation2"], tokenizer_or_path="martinjosifoski/genie-rw")
        crt_grammar = crt_builder.build(base_grammar_name=grammar_name, entities_or_path=["entity1", "entity2"], relations_or_path =["relation1", "relation2"], tokenizer_or_path="martinjosifoski/genie-rw")

    elif mode == 2:
        entities_path = os.path.join(RES_DIR, "genie-data", "jsonl", "small", "wiki_ner_entity_trie_original_strings.jsonl")
        relations_path = os.path.join(RES_DIR, "genie-data", "jsonl", "small", "wiki_ner_relation_trie_original_strings.jsonl")
        abs_grammar = abs_builder.build(base_grammar_name=grammar_name, entities_or_path=entities_path, relations_or_path=relations_path, tokenizer_or_path="martinjosifoski/genie-rw")
        crt_grammar = crt_builder.build(base_grammar_name=grammar_name, entities_or_path=entities_path, relations_or_path=relations_path, tokenizer_or_path="martinjosifoski/genie-rw", literal=args.literal)
    else:
        raise ValueError("mode must be 1 or 2.")


    grammar_pair = AbsCrtGrammarPair(abs_grammar=abs_grammar, crt_grammar=crt_grammar)
    grammar_pair.save(output_dir=output_dir)
