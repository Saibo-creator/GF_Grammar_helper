#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : test_gen_abs_grmr
# @Date : 2023-03-25-13-28
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os
import importlib

from src.config.config import GF_AUTO_GEN_GF_DIR,DATA_DIR,DATA_PATHS
from src.GrammarBuild.base_grammar import AbsCrtGrammarPair


if __name__ == '__main__':
    # get env variable LLAMA_DIR
    LLAMA_DIR = os.environ.get("LLAMA_DIR")

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["IE", "CP", "ED"])
    parser.add_argument("--KB", type=str, default=None)
    parser.add_argument("--grammar", type=str, default=None)
    parser.add_argument("--tokenizer-path", type=str, default="saibo/llama-7B")
    # parser.add_argument("--grammar-name", type=str, minimal="auto", help="name of the grammar") # genie_llama_fully_expanded
    parser.add_argument("--compile", action="store_true", help="whether to compile the grammar")
    parser.add_argument("--literal", action="store_true", help="whether to use literal grammar")
    parser.add_argument("--debug", action="store_true", help="whether to use debug mode, which will generate a small grammar from list of entities and relations")
    args = parser.parse_args()
    
    if args.task == "IE":
        assert args.KB in ["wiki_ner", "rebel", "rebel_medium"], f"KB {args.KB} not implemented, choose from [wiki_ner, rebel, rebel_medium]"
        assert args.grammar in ["FullyExpanded", "SubjectCollapsed"], f"grammar {args.grammar} not implemented, choose from [FullyExpanded, SubjectCollapsed]"
    elif args.task == "CP":
        assert args.KB is None, f"KB should be None for CP task"
        assert args.grammar in ["Ptb"], f"grammar {args.grammar} not implemented, choose from [Ptb]"
    elif args.task == "ED":
        assert args.KB in ["kilt_wiki"], f"KB {args.KB} not implemented, choose from [wikipedia-kilt]"
        assert args.grammar in ["Minimal"], f"grammar {args.grammar} not implemented, choose from [Minimal]"
    else:
        raise NotImplementedError


    grammar_name = f"{args.task}_{args.KB}_{args.grammar}"
    grammar_name += "_debug" if args.debug else ""

    submodule_name = args.grammar

    task_abs_grammar_module = importlib.import_module(f"src.GrammarBuild.{args.task}")
    task_crt_grammar_module = importlib.import_module(f"src.GrammarBuild.{args.task}")

    absGrammarBuilder = getattr(task_abs_grammar_module, f"{args.task}_Indep{submodule_name}AbsGrammarBuilder")
    crtGrammarBuilder = getattr(task_crt_grammar_module, f"{args.task}_Indep{submodule_name}CrtGrammarBuilder")

    abs_builder = absGrammarBuilder(tokenizer_or_path=args.tokenizer_path, literal=args.literal)
    crt_builder = crtGrammarBuilder(tokenizer_or_path=args.tokenizer_path, literal=args.literal)

    output_dir = os.path.join(GF_AUTO_GEN_GF_DIR, f"{args.task}", "Indep", submodule_name)

    if args.task == "IE":

        entities_path = DATA_PATHS[args.task]["KB"][args.KB]["entity"]
        relations_path = DATA_PATHS[args.task]["KB"][args.KB]["relation"]

    elif args.task == "CP":
        entities_path = None
        relations_path = None
    elif args.task == "ED":
        entities_path = DATA_PATHS[args.task]["KB"][args.KB]["entity"]
        relations_path = None
    else:
        raise NotImplementedError

    print("start building abstract grammar...")
    abs_grammar = abs_builder.build(base_grammar_name=grammar_name, entities_or_path=entities_path, relations_or_path=relations_path)
    print("finished building abstract grammar...")
    print("start building concrete grammar...")
    crt_grammar = crt_builder.build(base_grammar_name=grammar_name, entities_or_path=entities_path, relations_or_path=relations_path)
    print("finished building concrete grammar...")

    grammar_pair = AbsCrtGrammarPair(abs_grammar=abs_grammar, crt_grammar=crt_grammar)
    grammar_pair.save(output_dir=output_dir, compile=args.compile)

    if args.debug:
        raise NotImplementedError
        abs_grammar = abs_builder.build(base_grammar_name=grammar_name, entities_or_path=["entity1", "entity2"], relations_or_path=["relation1", "relation2"], tokenizer_or_path=args.tokenizer_path)
        crt_grammar = crt_builder.build(base_grammar_name=grammar_name, entities_or_path=["entity1", "entity2"], relations_or_path =["relation1", "relation2"], tokenizer_or_path=args.tokenizer_path)





