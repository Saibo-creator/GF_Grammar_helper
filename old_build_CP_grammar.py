#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : test_gen_abs_grmr
# @Date : 2023-03-25-13-28
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import json
import os
import pdb

from tqdm import tqdm

from src.config.config import GF_AUTO_GEN_GF_DIR,DATA_DIR,ED_DATA_PATH
from src.GrammarBuild.base_grammar import AbsCrtGrammarPair
from src.GrammarBuild.CP import CP_IndepPtbAbsGrammarBuilder, CPCrtGrammarBuilder, CP_DepPtbAbsGrammarBuilder, CPotfCrtGrammarBuilder



if __name__ == '__main__':
    # get env variable LLAMA_DIR
    LLAMA_DIR = os.environ.get("LLAMA_DIR")

    import argparse
    parser = argparse.ArgumentParser()
    # parser.add_argument("--dataset", type=str, minimal="aida", help="dataset name", choices=["aida"])
    parser.add_argument("--tokenizer-path", type=str, default=f"{LLAMA_DIR}/7B", help="martinjosifoski/genie-rw, /dlabdata1/llama_hf/7B, t5-small")
    parser.add_argument("--grammar-name", type=str, default="auto", help="name of the grammar") # genie_llama_fully_expanded
    parser.add_argument("--compile", action="store_true", help="whether to compile the grammar")
    parser.add_argument("--debug", action="store_true", help="whether to use debug mode, which will generate a small grammar from list of entities and relations")
    parser.add_argument("--literal", action="store_true", help="whether to use literal grammar")
    parser.add_argument("--otf", action="store_true", help="whether to use OTF grammar")
    parser.add_argument("--otf-input-file", type=str, default=f"{DATA_DIR}/CP/ptb/ptb-test-only-text.jsonl", help="input file for OTF grammar")
    args = parser.parse_args()


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

    output_dir = os.path.join(GF_AUTO_GEN_GF_DIR, f"CP", grammar_name+"_literal" if args.literal else grammar_name)

    if args.otf:
        otf_input_file = args.otf_input_file

        with open(otf_input_file, "r", encoding="utf-8") as f:
            entries = [json.loads(line) for line in f]

        for entry in tqdm(entries):
            text = entry["text"]
            entry_id = entry["id"]
            grammar_entry_name = grammar_name + f"_{entry_id}"

            abs_builder = CP_DepPtbAbsGrammarBuilder(tokenizer_or_path=args.tokenizer_path, literal=args.literal)
            crt_builder = CPotfCrtGrammarBuilder(tokenizer_or_path=args.tokenizer_path, literal=args.literal)

            abs_grammar = abs_builder.build(base_grammar_name=grammar_entry_name,input_sentence=text)
            crt_grammar = crt_builder.build(base_grammar_name=grammar_entry_name,input_sentence=text)

            grammar_pair = AbsCrtGrammarPair(abs_grammar=abs_grammar, crt_grammar=crt_grammar)
            grammar_pair.save(output_dir=output_dir, compile=args.compile, only_keep_pgf=False, individual_dir=False)

    else:
        abs_builder = CP_IndepPtbAbsGrammarBuilder(tokenizer_or_path=args.tokenizer_path, literal=args.literal)
        crt_builder = CPCrtGrammarBuilder(tokenizer_or_path=args.tokenizer_path, literal=args.literal)



        abs_grammar = abs_builder.build(base_grammar_name=grammar_name)
        crt_grammar = crt_builder.build(base_grammar_name=grammar_name)

        grammar_pair = AbsCrtGrammarPair(abs_grammar=abs_grammar, crt_grammar=crt_grammar)
        grammar_pair.save(output_dir=output_dir, compile=args.compile)


