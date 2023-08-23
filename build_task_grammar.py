#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : test_gen_abs_grmr
# @Date : 2023-03-25-13-28
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import json
import os
from typing import Dict, List

from tqdm import tqdm

from src.CP_grammar.abs_grammar import CP_AbstractGrammar
from src.CP_grammar.crt_grammar import CP_ConcreteGrammar
from src.CP_grammar.factory import CPGrammarFactory
from src.ED_grammar.abs_grammar import ED_AbstractGrammar
from src.ED_grammar.crt_grammar import ED_ConcreteGrammar
from src.ED_grammar.factory import EDGrammarFactory
from src.IE_grammar.abs_grammar import IE_AbstractGrammar
from src.IE_grammar.crt_grammar import IE_ConcreteGrammar
from src.IE_grammar.factory import IEGrammarFactory
from src.compilation import compile_for_task

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
            "grammar_type": ["fe", "sc"],
            "dataset": ["wikinre", "rebel_1M", "rebel_6M"],
        },
        "CP": {"grammar_type": ["re"], "dataset": ["ptb"]},
        "ED": {
            "grammar_type": ["minimal", "canonical"],
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
        "--grammar_type", type=str, required=True, help="Specify the grammar type."
    )
    parser.add_argument(
        "--dataset", type=str, required=True, help="Specify the dataset to be used."
    )
    parser.add_argument(
        "--tokenizer-path",
        default="saibo/llama-7B",
        type=str,
        choices=["saibo/llama-7B"],
        help="Path to the tokenizer.",
    )

    # Flags
    parser.add_argument(
        "--literal",
        action="store_true",
        help="Whether to use literal or integer encoding.",
    )

    parser.add_argument(
        "--compile", action="store_true", help="Whether to compile the grammar."
    )

    parser.add_argument(
        "--clean", action="store_true", help="Whether to clean the grammar."
    )

    args = parser.parse_args()

    # Check the validity of provided grammar and dataset based on the task.
    if args.grammar_type not in TASKS[args.task]["grammar_type"]:
        valid_grammars = ", ".join(TASKS[args.task]["grammar_type"])
        raise ValueError(
            f"Invalid grammar_type for task '{args.task}'. Valid options are: {valid_grammars}"
        )

    if args.dataset not in TASKS[args.task]["dataset"]:
        valid_datasets = ", ".join(TASKS[args.task]["dataset"])
        raise ValueError(
            f"Invalid dataset for task '{args.task}'. Valid options are: {valid_datasets}"
        )

    task, grammar_type, dataset_name = args.task, args.grammar_type, args.dataset
    tokenizer_path, literal = args.tokenizer_path, args.literal

    if args.task == "CP":
        GrammarFactoryClass = CPGrammarFactory
    elif args.task == "ED":
        GrammarFactoryClass = EDGrammarFactory
    elif args.task == "IE":
        GrammarFactoryClass = IEGrammarFactory
    else:
        raise ValueError(f"Invalid task: {args.task}")

    factory = GrammarFactoryClass(
        tokenizer_path=tokenizer_path, grammar_type=grammar_type, literal=literal
    )

    dataset_jsonl = DATA_PATHS[task]["Tasks"][dataset_name]

    # entities_path = DATA_PATHS["ED"]["KB"][None]["entity"]
    # entities: List[str] = read_jsonl(entities_path)
    with open(dataset_jsonl, "r", encoding="utf-8") as f:
        dps: List[Dict] = [json.loads(line) for line in f]

    dataset = {
        "dps": dps,
        "name": dataset_name,
    }

    bigrammars, grammar_src_dir = factory.build_bigrammars(
        dataset=dataset, total=None, save_to_gf=True
    )
    # pgf_output_dir = "output/ED/aida"

    if args.compile:
        compile_for_task(
            task=task,
            grammar_type=grammar_type,
            dataset=dataset_name,
            verbose=True,
            clean=args.clean,
        )
