#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : test_gen_abs_grmr
# @Date : 2023-03-25-13-28
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os
import pdb

from src.config.config import GF_AUTO_GEN_GF_DIR,DATA_DIR,ED_DATA_PATH
from src.GrammarBuild.base_grammar import AbsCrtGrammarPair
from src.GrammarBuild.ED import ED_IndepMinimalAbsGrammarBuilder, ED_IndepMinimalCrtGrammarBuilder


if __name__ == '__main__':
    # get env variable LLAMA_DIR
    LLAMA_DIR = os.environ.get("LLAMA_DIR")

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="aida", help="dataset name", choices=["aida"])
    parser.add_argument("--split", type=str, default="all", choices=["all", "train", "dev", "test"])
    parser.add_argument("--tokenizer-path", type=str, default=f"{LLAMA_DIR}/7B", help="martinjosifoski/genie-rw, /dlabdata1/llama_hf/7B, t5-small")
    parser.add_argument("--grammar-name", type=str, default="auto", help="name of the grammar") # genie_llama_fully_expanded
    parser.add_argument("--compile", action="store_true", help="whether to compile the grammar")
    parser.add_argument("--debug", action="store_true", help="whether to use debug mode, which will generate a small grammar from list of entities and relations")
    parser.add_argument("--literal", action="store_true", help="whether to use literal grammar")
    args = parser.parse_args()


    if args.grammar_name == "auto":
        grammar_name="ED"
        if "llama" in args.tokenizer_path:
            grammar_name += "_llama"
        elif "t5" in args.tokenizer_path:
            grammar_name += "_t5"
        else:
            raise NotImplementedError(f"tokenizer_path {args.tokenizer_path} not implemented")

        if args.dataset == "aida":
            grammar_name += "_aida"
        else:
            raise NotImplementedError(f"dataset {args.dataset} not implemented")

        # split
        grammar_name += f"_{args.split}"

        if args.debug:
            grammar_name = "debug"
    else:
        grammar_name = args.grammar_name


    abs_builder = ED_IndepMinimalAbsGrammarBuilder(tokenizer_or_path=args.tokenizer_path, literal=args.literal)
    crt_builder = ED_IndepMinimalCrtGrammarBuilder(tokenizer_or_path=args.tokenizer_path, literal=args.literal)

    output_dir = os.path.join(GF_AUTO_GEN_GF_DIR, f"ED")

    if args.debug:
        abs_grammar = abs_builder.build(base_grammar_name=grammar_name, entities_or_path=["entity1", "entity2"])
        crt_grammar = crt_builder.build(base_grammar_name=grammar_name, entities_or_path=["entity1", "entity2"])

    else:

        entities_path = ED_DATA_PATH[f"{args.dataset}-{args.split}"]["entity"]
        print("start building abstract grammar...")
        abs_grammar = abs_builder.build(base_grammar_name=grammar_name, entities_or_path=entities_path)
        print("finished building abstract grammar...")
        print("start building concrete grammar...")
        crt_grammar = crt_builder.build(base_grammar_name=grammar_name, entities_or_path=entities_path)
        print("finished building concrete grammar...")


    grammar_pair = AbsCrtGrammarPair(abs_grammar=abs_grammar, crt_grammar=crt_grammar)
    grammar_pair.save(output_dir=output_dir, compile=args.compile)