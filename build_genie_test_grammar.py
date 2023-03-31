#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : test_gen_abs_grmr
# @Date : 2023-03-25-13-28
# @Project: GFLM
# @AUTHOR : Saibo Geng
# @Desc :
import os
import pdb

from src.config.config import AUTO_GEN_GF_DIR,RES_DIR
from src.base_grammar import AbsCrtGrammarPair
from src.v2.abs_grammar import GenieAbsGrammarBuilder
from src.v2.crt_grammar import GenieCrtGrammarBuilder


if __name__ == '__main__':


    abs_builder = GenieAbsGrammarBuilder()
    crt_builder = GenieCrtGrammarBuilder()

    output_dir = os.path.join(AUTO_GEN_GF_DIR, f"v2")
    grammar_name = "GenieTest"

    ENTITIES = [" AlAq", " byAq", " AlA", " Al by"]
    RELATIONS = [" date of birth", " date of death", " date of", " is a"]

    abs_grammar = abs_builder.build(base_grammar_name=grammar_name, entities_or_path=ENTITIES, relations_or_path=RELATIONS, tokenizer_or_path="martinjosifoski/genie-rw")
    crt_grammar = crt_builder.build(base_grammar_name=grammar_name, entities_or_path=ENTITIES, relations_or_path =RELATIONS, tokenizer_or_path="martinjosifoski/genie-rw")


    grammar_pair = AbsCrtGrammarPair(abs_grammar=abs_grammar, crt_grammar=crt_grammar)
    grammar_pair.save(output_dir=output_dir, compile=True)
