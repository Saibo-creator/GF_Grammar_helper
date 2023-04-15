#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : test_gen_abs_grmr
# @Date : 2023-03-25-13-28
# @Project: GFLM
# @AUTHOR : Saibo Geng
# @Desc :
import os

from transformers import AutoTokenizer

from src.config.config import GF_AUTO_GEN_GF_DIR
from src.GrammarBuild.base_grammar import AbsCrtGrammarPair
from src.GrammarBuild.v2.abs_grammar import GenieAbsGrammarBuilder
from src.GrammarBuild.v2.crt_grammar import GenieCrtGrammarBuilder


if __name__ == '__main__':


    abs_builder = GenieAbsGrammarBuilder()
    crt_builder = GenieCrtGrammarBuilder()

    # tokenizer = "martinjosifoski/genie-rw"
    # tokenizer =

    output_dir = os.path.join(GF_AUTO_GEN_GF_DIR, f"v2")
    grammar_name = "GenieT5Test"

    ENTITIES = [" AlAq", " byAq", " AlA", " Al by"]
    RELATIONS = [" date of birth", " date of death", " date of", " is a"]

    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base", bos_token='<BOS>', bos_token_id=0)

    abs_grammar = abs_builder.build(base_grammar_name=grammar_name, entities_or_path=ENTITIES, relations_or_path=RELATIONS, tokenizer_or_path=tokenizer)
    crt_grammar = crt_builder.build(base_grammar_name=grammar_name, entities_or_path=ENTITIES, relations_or_path =RELATIONS, tokenizer_or_path=tokenizer)


    grammar_pair = AbsCrtGrammarPair(abs_grammar=abs_grammar, crt_grammar=crt_grammar)
    grammar_pair.save(output_dir=output_dir, compile=True)
