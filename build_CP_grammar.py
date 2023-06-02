#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : test_gen_abs_grmr
# @Date : 2023-03-25-13-28
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os
import pdb

from src.config.config import GF_AUTO_GEN_GF_DIR,DATA_DIR,EL_TRAINING_DATA_PATH
from src.GrammarBuild.base_grammar import AbsCrtGrammarPair
from src.GrammarBuild.CP import CPAbsGrammarBuilder, CPCrtGrammarBuilder, CPotfAbsGrammarBuilder, CPotfCrtGrammarBuilder



if __name__ == '__main__':
    # get env variable LLAMA_DIR
    LLAMA_DIR = os.environ.get("LLAMA_DIR")

    import argparse
    parser = argparse.ArgumentParser()
    # parser.add_argument("--dataset", type=str, default="aida", help="dataset name", choices=["aida"])
    parser.add_argument("--tokenizer-path", type=str, default=f"{LLAMA_DIR}/7B", help="martinjosifoski/genie-rw, /dlabdata1/llama_hf/7B, t5-small")
    parser.add_argument("--grammar-name", type=str, default="auto", help="name of the grammar") # genie_llama_fully_expanded
    parser.add_argument("--compile", action="store_true", help="whether to compile the grammar")
    parser.add_argument("--debug", action="store_true", help="whether to use debug mode, which will generate a small grammar from list of entities and relations")
    parser.add_argument("--literal", action="store_true", help="whether to use literal grammar")
    parser.add_argument("--otf", action="store_true", help="whether to use OTF grammar")
    args = parser.parse_args()

    output_dir = os.path.join(GF_AUTO_GEN_GF_DIR, f"CP")


    if args.grammar_name == "auto":
        grammar_name="CP" if not args.otf else "CP_OTF"
        if "llama" in args.tokenizer_path:
            grammar_name += "_llama"
        elif "t5" in args.tokenizer_path:
            grammar_name += "_t5"
        else:
            raise NotImplementedError(f"tokenizer_path {args.tokenizer_path} not implemented")

        if args.debug:
            grammar_name = "debug"
    else:
        grammar_name = args.grammar_name

    if args.otf:
        abs_builder = CPotfAbsGrammarBuilder(tokenizer_or_path=args.tokenizer_path, literal=args.literal)
        crt_builder = CPotfCrtGrammarBuilder(tokenizer_or_path=args.tokenizer_path, literal=args.literal)

        abs_grammar = abs_builder.build(base_grammar_name=grammar_name,input_sentence="hello world")
        crt_grammar = crt_builder.build(base_grammar_name=grammar_name,input_sentence="hello world")

        grammar_pair = AbsCrtGrammarPair(abs_grammar=abs_grammar, crt_grammar=crt_grammar)
        grammar_pair.save(output_dir=output_dir, compile=args.compile)

    else:
        abs_builder = CPAbsGrammarBuilder(tokenizer_or_path=args.tokenizer_path, literal=args.literal)
        crt_builder = CPCrtGrammarBuilder(tokenizer_or_path=args.tokenizer_path, literal=args.literal)



        abs_grammar = abs_builder.build(base_grammar_name=grammar_name)
        crt_grammar = crt_builder.build(base_grammar_name=grammar_name)

        grammar_pair = AbsCrtGrammarPair(abs_grammar=abs_grammar, crt_grammar=crt_grammar)
        grammar_pair.save(output_dir=output_dir, compile=args.compile)


