#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : test_gen_abs_grmr
# @Date : 2023-03-25-13-28
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os
import pdb
import json

from tqdm import tqdm

from src.config.config import GF_AUTO_GEN_GF_DIR,DATA_DIR,EL_TRAINING_DATA_PATH
from src.GrammarBuild.base_grammar import AbsCrtGrammarPair
from src.GrammarBuild.EL import ELotfAbsGrammarBuilder, ELotfCrtGrammarBuilder


if __name__ == '__main__':
    # get env variable LLAMA_DIR
    LLAMA_DIR = os.environ.get("LLAMA_DIR")

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="aida", help="dataset name", choices=["aida", "ace2004", "aquaint", "clueweb", "msnbc", "wiki"])
    parser.add_argument("--split", type=str, default="dev", choices=["all", "train", "dev", "test"])
    parser.add_argument("--tokenizer-path", type=str, default=f"{LLAMA_DIR}/7B", help="martinjosifoski/genie-rw, /dlabdata1/llama_hf/7B, t5-small")
    parser.add_argument("--grammar-name", type=str, default="auto", help="name of the grammar") # genie_llama_fully_expanded
    parser.add_argument("--compile", action="store_true", help="whether to compile the grammar")
    parser.add_argument("--debug", action="store_true", help="whether to use debug mode, which will generate a small grammar from list of entities and relations")
    parser.add_argument("--literal", action="store_true", help="whether to use literal grammar")
    args = parser.parse_args()


    if args.grammar_name == "auto":
        grammar_name="EL_OTF"
        if "llama" in args.tokenizer_path:
            grammar_name += "_llama"
        elif "t5" in args.tokenizer_path:
            grammar_name += "_t5"
        else:
            raise NotImplementedError(f"tokenizer_path {args.tokenizer_path} not implemented")

        grammar_name += f"_{args.dataset}"

        # split
        grammar_name += f"_{args.split}"

        if args.debug:
            grammar_name = "debug"
    else:
        grammar_name = args.grammar_name

    abs_builder = ELotfAbsGrammarBuilder(tokenizer_or_path=args.tokenizer_path, literal=args.literal)
    crt_builder = ELotfCrtGrammarBuilder(tokenizer_or_path=args.tokenizer_path, literal=args.literal)

    output_dir = os.path.join(GF_AUTO_GEN_GF_DIR, f"EL", grammar_name)

    datafile = f"data/el_data/{args.dataset}-{args.split}-kilt-processed-short.jsonl"

    with open(datafile, "r", encoding="utf-8") as f:
        entries = [json.loads(line) for line in f]

    for entry in tqdm(entries):
        mention= entry["mention"]
        entities = entry["candidates"]
        entry_id = entry["id"]
        grammar_entry_name = grammar_name + f"_{entry_id}"
        abs_grammar = abs_builder.build(base_grammar_name=grammar_entry_name, entities_or_path=entities)
        crt_grammar = crt_builder.build(base_grammar_name=grammar_entry_name, mention=mention, entities_or_path=entities)

        grammar_pair = AbsCrtGrammarPair(abs_grammar=abs_grammar, crt_grammar=crt_grammar)
        grammar_pair.save(output_dir=output_dir, compile=args.compile, only_keep_pgf=True, individual_dir=False)

