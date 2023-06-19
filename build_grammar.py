#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : test_gen_abs_grmr
# @Date : 2023-03-25-13-28
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import json
import os
import importlib
import pdb

from tqdm import tqdm

from src.config.config import GF_AUTO_GEN_GF_DIR,DATA_PATHS
from src.GrammarBuild.base_grammar import AbsCrtGrammarPair


if __name__ == '__main__':
    # get env variable LLAMA_DIR
    LLAMA_DIR = os.environ.get("LLAMA_DIR")

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["IE", "CP", "ED"])
    parser.add_argument("--dep", action="store_true", help="whether to use dep grammar")
    parser.add_argument("--grammar", type=str, default=None)
    parser.add_argument("--KB", type=str, default=None)
    parser.add_argument("--dataset", type=str, default=None)
    parser.add_argument("--tokenizer-path", type=str, default="saibo/llama-7B")
    parser.add_argument("--compile", action="store_true", help="whether to compile the grammar")
    parser.add_argument("--literal", action="store_true", help="whether to use literal grammar")
    parser.add_argument("--debug", action="store_true", help="whether to use debug mode, which will generate a small grammar from list of entities and relations")
    parser.add_argument("--clean", action="store_true", help="whether to clean the grammar")
    args = parser.parse_args()
    dependency = "Dep" if args.dep else "Indep"
    
    if args.task == "IE":
        assert args.KB in ["wiki_ner", "rebel", "rebel_medium"], f"KB {args.KB} not implemented, choose from [wiki_ner, rebel, rebel_medium]"
        assert args.grammar in ["FullyExpanded", "SubjectCollapsed"], f"grammar {args.grammar} not implemented, choose from [FullyExpanded, SubjectCollapsed]"
    elif args.task == "CP":
        assert args.KB is None, f"KB should be None for CP task"
        assert args.grammar in ["PtbRe", "PtbCfg"], f"grammar {args.grammar} not implemented, choose from [PtbRe, PtbCfg]"
    elif args.task == "ED":
        if args.dep:
            assert args.KB is None, f"KB should be None for ED task"
        else:
            assert args.KB in ["kilt_wiki", "YAGO_KB"], f"KB {args.KB} not implemented, choose from [wiki_kilt, YAGO_KB]"
        assert args.grammar in ["Minimal", "Canonical"], f"grammar {args.grammar} not implemented, choose from [Minimal]"
    else:
        raise NotImplementedError

    KB_name = args.KB if args.KB is not None else "NoKB"
    dataset = f"_{args.dataset}" if args.dataset is not None else ""
    grammar_name = f"{args.task}{dataset}_{KB_name}_{args.grammar}_{args.tokenizer_path.split('/')[-1].replace('-','_')}"
    grammar_name += "_debug" if args.debug else ""

    submodule_name = args.grammar

    task_abs_grammar_module = importlib.import_module(f"src.GrammarBuild.{args.task}")
    task_crt_grammar_module = importlib.import_module(f"src.GrammarBuild.{args.task}")

    absGrammarBuilder = getattr(task_abs_grammar_module, f"{args.task}_{dependency}{submodule_name}AbsGrammarBuilder")
    crtGrammarBuilder = getattr(task_crt_grammar_module, f"{args.task}_{dependency}{submodule_name}CrtGrammarBuilder")

    abs_builder = absGrammarBuilder(tokenizer_or_path=args.tokenizer_path, literal=args.literal)
    crt_builder = crtGrammarBuilder(tokenizer_or_path=args.tokenizer_path, literal=args.literal)

    output_dir = os.path.join(GF_AUTO_GEN_GF_DIR, f"{args.task}", f"{dependency}", grammar_name)

    if args.task == "IE":

        entities_path = DATA_PATHS[args.task]["KB"][args.KB]["entity"]
        relations_path = DATA_PATHS[args.task]["KB"][args.KB]["relation"]

    elif args.task == "CP":
        entities_path = None
        relations_path = None
    elif args.task == "ED":
        entities_path = DATA_PATHS[args.task]["KB"][args.KB]["entity"] if not args.dep else None
        relations_path = None
    else:
        raise NotImplementedError



    if not args.dep:
        print("start building abstract grammar...")
        abs_grammar = abs_builder.build(base_grammar_name=grammar_name, entities_or_path=entities_path, relations_or_path=relations_path)
        print("finished building abstract grammar...")
        print("start building concrete grammar...")
        crt_grammar = crt_builder.build(base_grammar_name=grammar_name, entities_or_path=entities_path, relations_or_path=relations_path)
        print("finished building concrete grammar...")

        grammar_pair = AbsCrtGrammarPair(abs_grammar=abs_grammar, crt_grammar=crt_grammar)
        grammar_pair.save(output_dir=output_dir, compile=args.compile,only_keep_pgf=args.clean)
    else:
        dataset_jsonl = DATA_PATHS[args.task]["Tasks"][args.dataset]

        with open(dataset_jsonl, "r", encoding="utf-8") as f:
            entries = [json.loads(line) for line in f]

        empty_entries = 0
        for entry in tqdm(entries):
            mention = entry.get("mention", None)
            entities = entry.get("candidates", None)
            if entities == []:
                empty_entries += 1
                continue
            left_context = entry.get("left_context", None)
            right_context = entry.get("right_context", None)
            entry_id = entry.get("id", None)
            text = entry.get("text", None)
            tokens = entry.get("tokens", None)
            print(f"entry_id: {entry_id}")
            grammar_entry_name = grammar_name + f"_{entry_id}"
            abs_grammar = abs_builder.build(base_grammar_name=grammar_entry_name, entities_or_path=entities, mention=mention, left_context=left_context, right_context=right_context, text=text, words=tokens)

            crt_grammar = crt_builder.build(base_grammar_name=grammar_entry_name, entities_or_path=entities,
                                            mention=mention, left_context=left_context, right_context=right_context, text=text, words=tokens)

            grammar_pair = AbsCrtGrammarPair(abs_grammar=abs_grammar, crt_grammar=crt_grammar)
            grammar_pair.save(output_dir=output_dir, compile=args.compile, only_keep_pgf=args.clean,
                              individual_dir=False)

        print(f"empty_entries: {empty_entries}")



