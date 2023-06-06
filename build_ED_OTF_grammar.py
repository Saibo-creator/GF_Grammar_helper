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

from src.config.config import GF_AUTO_GEN_GF_DIR,DATA_DIR,ED_DATA_PATH
from src.GrammarBuild.base_grammar import AbsCrtGrammarPair


if __name__ == '__main__':
    # get env variable LLAMA_DIR
    LLAMA_DIR = os.environ.get("LLAMA_DIR")

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="aquaint", help="dataset name", choices=["aida", "ace2004", "aquaint", "clueweb", "msnbc", "wiki"])
    parser.add_argument("--split", type=str, default="test", choices=["all", "train", "dev", "test"])
    parser.add_argument("--tokenizer-path", type=str, default=f"{LLAMA_DIR}/7B", help="martinjosifoski/genie-rw, /dlabdata1/llama_hf/7B, t5-small")
    parser.add_argument("--grammar-name", type=str, default="EDotf", choices=["EDotf", "EDotfs", "ED"])
    parser.add_argument("--compile", action="store_true", help="whether to compile the grammar")
    parser.add_argument("--debug", action="store_true", help="whether to use debug mode, which will generate a small grammar from list of entities and relations")
    parser.add_argument("--literal", action="store_true", help="whether to use literal grammar")
    args = parser.parse_args()

    # grammar name
    grammar_name = args.grammar_name

    # tokenizer
    if "llama" in args.tokenizer_path:
        grammar_name += "_llama"
    elif "t5" in args.tokenizer_path:
        grammar_name += "_t5"
    else:
        raise NotImplementedError(f"tokenizer_path {args.tokenizer_path} not implemented")

    # dataset
    grammar_name += f"_{args.dataset}_{args.split}"

    grammar_name += "_literal" if args.literal else ""

    # dynamical init grammar builder depending on class name
    abs_builder = eval(f"{args.grammar_name}AbsGrammarBuilder")(tokenizer_or_path=args.tokenizer_path, literal=args.literal)
    crt_builder = eval(f"{args.grammar_name}CrtGrammarBuilder")(tokenizer_or_path=args.tokenizer_path, literal=args.literal)

    output_dir = os.path.join(GF_AUTO_GEN_GF_DIR, f"ED", grammar_name)

    datafile = ED_DATA_PATH['Tasks'][args.dataset]

    with open(datafile, "r", encoding="utf-8") as f:
        entries = [json.loads(line) for line in f]

    for entry in tqdm(entries):
        mention= entry["mention"]
        entities = entry["candidates"]
        left_context = entry["left_context"]
        right_context = entry["right_context"]
        entry_id = entry["id"]
        print(f"entry_id: {entry_id}")
        grammar_entry_name = grammar_name + f"_{entry_id}"
        abs_grammar = abs_builder.build(base_grammar_name=grammar_entry_name, entities_or_path=entities)
        crt_grammar = crt_builder.build(base_grammar_name=grammar_entry_name, entities_or_path=entities, mention=mention, left_context=left_context, right_context=right_context)

        grammar_pair = AbsCrtGrammarPair(abs_grammar=abs_grammar, crt_grammar=crt_grammar)
        grammar_pair.save(output_dir=output_dir, compile=args.compile, only_keep_pgf=False, individual_dir=False)

