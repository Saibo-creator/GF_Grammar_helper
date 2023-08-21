#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : test_gen_abs_grmr
# @Date : 2023-03-25-13-28
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import json
import os

from tqdm import tqdm

from src.config.config import (
    GF_AUTO_GEN_GF_DIR,
    DATA_PATHS,
    GRAMMAR_JSON_CONFIG_ASSET_DIR,
)
from src.legacy_GrammarBuild.base_grammar import AbsCrtGrammarPair

if __name__ == "__main__":
    import argparse

    # Define valid tasks, grammars, and datasets using a nested dictionary.
    TASKS = {
        "IE": {
            "grammar": ["FullyExpanded", "SubjectCollapsed"],
            "dataset": ["wiki_ner", "rebel", "rebel_medium"],
        },
        "CP": {"grammar": ["re"], "dataset": ["ptb"]},
        "ED": {
            "grammar": ["Minimal", "Canonical"],
            "dataset": ["aida", "ace2004", "aquaint", "clueweb", "msnbc", "wiki"],
        },
    }

    parser = argparse.ArgumentParser(description="A script for various NLP tasks.")

    # General Arguments
    parser.add_argument(
        "--task",
        choices=TASKS.keys(),
        required=True,
        help="Specify the task to be performed.",
    )
    parser.add_argument(
        "--grammar", type=str, required=True, help="Specify the grammar type."
    )
    parser.add_argument(
        "--dataset", type=str, required=True, help="Specify the dataset to be used."
    )
    parser.add_argument(
        "--tokenizer-path",
        type=str,
        choices=["saibo/llama-7B"],
        help="Path to the tokenizer.",
    )
    parser.add_argument(
        "--str_or_int",
        type=str,
        default="str",
        choices=["str", "int"],
        help="Whether to use string or integer as the terminal symbol.",
    )

    # Flags
    parser.add_argument(
        "--compile", action="store_true", help="Whether to compile the grammar."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Use debug mode, which will generate a small grammar from list of entities and relations.",
    )
    parser.add_argument(
        "--clean", action="store_true", help="Whether to clean the grammar."
    )

    args = parser.parse_args()

    # Check the validity of provided grammar and dataset based on the task.
    if args.grammar not in TASKS[args.task]["grammar"]:
        valid_grammars = ", ".join(TASKS[args.task]["grammar"])
        raise ValueError(
            f"Invalid grammar for task '{args.task}'. Valid options are: {valid_grammars}"
        )

    if args.dataset not in TASKS[args.task]["dataset"]:
        valid_datasets = ", ".join(TASKS[args.task]["dataset"])
        raise ValueError(
            f"Invalid dataset for task '{args.task}'. Valid options are: {valid_datasets}"
        )

    task, grammar_type, dataset = args.task, args.grammar, args.dataset

    abs_grammar_name = f"{task}_{grammar_type}_{dataset}"
    crt_grammar_name = "_".join([abs_grammar_name, args.str_or_int, "llama"])

    dataset = f"_{args.dataset}" if args.dataset is not None else ""
    grammar_name = f"{args.task}_{args.grammar}_llama"
    grammar_name += "_debug" if args.debug else ""

    if args.task == "CP":
        abs_grammar_cls = CP_AbstractGrammar
        crt_grammar_cls = CP_ConcreteGrammar

    elif args.task == "IE":
        abs_grammar_cls = IE_AbstractGrammar
        crt_grammar_cls = IE_ConcreteGrammar
    elif args.task == "ED":
        abs_grammar_cls = ED_AbstractGrammar
        crt_grammar_cls = ED_ConcreteGrammar
    else:
        raise NotImplementedError

    CRT_GRAMMAR_BASE_CONFIG_PATH = os.path.join(
        GRAMMAR_JSON_CONFIG_ASSET_DIR, task, grammar_type, "concrete.json"
    )

    ABS_GRAMMAR_BASE_CONFIG_PATH = os.path.join(
        GRAMMAR_JSON_CONFIG_ASSET_DIR, task, grammar_type, "abstract.json"
    )

    abs_grammar_name = f"{task}_{grammar_type}_{dataset}"

    abs_grammar = abs_grammar_cls(
        base_abs_grammar_path=ABS_GRAMMAR_BASE_CONFIG_PATH,
        num_input_words=len(tokens),
        name="CP_re_ptb_dp0",
    )

    abs_builder = absGrammarBuilder(
        tokenizer_or_path=args.tokenizer_path, literal=args.literal
    )
    crt_builder = crtGrammarBuilder(
        tokenizer_or_path=args.tokenizer_path, literal=args.literal
    )

    output_dir = os.path.join(
        GF_AUTO_GEN_GF_DIR, f"{args.task}", f"{dependency}", grammar_name
    )

    if args.task == "IE":

        entities_path = DATA_PATHS[args.task]["KB"][args.KB]["entity"]
        relations_path = DATA_PATHS[args.task]["KB"][args.KB]["relation"]

    elif args.task == "CP":
        entities_path = None
        relations_path = None
    elif args.task == "ED":
        entities_path = (
            DATA_PATHS[args.task]["KB"][args.KB]["entity"] if not args.dep else None
        )
        relations_path = None
    else:
        raise NotImplementedError

    if not args.dep:
        print("start building abstract grammar...")
        abs_grammar = abs_builder.build(
            base_grammar_name=grammar_name,
            entities_or_path=entities_path,
            relations_or_path=relations_path,
        )
        print("finished building abstract grammar...")
        print("start building concrete grammar...")
        crt_grammar = crt_builder.build(
            base_grammar_name=grammar_name,
            entities_or_path=entities_path,
            relations_or_path=relations_path,
        )
        print("finished building concrete grammar...")

        grammar_pair = AbsCrtGrammarPair(
            abs_grammar=abs_grammar, crt_grammar=crt_grammar
        )
        grammar_pair.save(
            output_dir=output_dir, compile=args.compile, only_keep_pgf=args.clean
        )
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
            abs_grammar = abs_builder.build(
                base_grammar_name=grammar_entry_name,
                entities_or_path=entities,
                mention=mention,
                left_context=left_context,
                right_context=right_context,
                text=text,
                words=tokens,
            )

            crt_grammar = crt_builder.build(
                base_grammar_name=grammar_entry_name,
                entities_or_path=entities,
                mention=mention,
                left_context=left_context,
                right_context=right_context,
                text=text,
                words=tokens,
            )

            grammar_pair = AbsCrtGrammarPair(
                abs_grammar=abs_grammar, crt_grammar=crt_grammar
            )
            grammar_pair.save(
                output_dir=output_dir,
                compile=args.compile,
                only_keep_pgf=args.clean,
                individual_dir=False,
            )

        print(f"empty_entries: {empty_entries}")
