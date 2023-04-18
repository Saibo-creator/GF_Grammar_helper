#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : test_gen_abs_grmr
# @Date : 2023-03-25-13-28
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import argparse
import os

from transformers import AutoTokenizer

from src.GrammarBuild.base_grammar import AbsCrtGrammarPair
from src.config.config import GF_AUTO_GEN_GF_DIR

if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--format", type=str, default="FullyExpanded", choices=["FullyExpanded", "FullyExpandedEt",
                            "SubjectCollapsed"])
    args = arg_parser.parse_args()

    #dynamic import based on format
    GenieAbsGrammarBuilderModule = __import__(f"src.GrammarBuild.v2", fromlist=[f"Genie{args.format}AbsGrammarBuilder"])
    GenieCrtGrammarBuilderModule = __import__(f"src.GrammarBuild.v2", fromlist=[f"Genie{args.format}CrtGrammarBuilder"])

    GenieAbsGrammarBuilder = getattr(GenieAbsGrammarBuilderModule, f"Genie{args.format}AbsGrammarBuilder")
    GenieCrtGrammarBuilder = getattr(GenieCrtGrammarBuilderModule, f"Genie{args.format}CrtGrammarBuilder")

    abs_builder = GenieAbsGrammarBuilder()
    crt_builder = GenieCrtGrammarBuilder()

    output_dir = os.path.join(GF_AUTO_GEN_GF_DIR, f"v2")
    grammar_name = "GenieT5Test"

    ENTITIES = [" AlAq", " byAq", " AlA", " Al by"]
    RELATIONS = [" date of birth", " date of death", " date of", " is a"]

    # By default, flan-t5-base does not have bos_token, we add it manually.
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base", bos_token='<pad>')# <pad> is the token id 0 in flan-t5-base

    abs_grammar = abs_builder.build(base_grammar_name=grammar_name, entities_or_path=ENTITIES, relations_or_path=RELATIONS, tokenizer_or_path=tokenizer)
    crt_grammar = crt_builder.build(base_grammar_name=grammar_name, entities_or_path=ENTITIES, relations_or_path =RELATIONS, tokenizer_or_path=tokenizer)

    grammar_pair = AbsCrtGrammarPair(abs_grammar=abs_grammar, crt_grammar=crt_grammar)
    grammar_pair.save(output_dir=output_dir, compile=True)
