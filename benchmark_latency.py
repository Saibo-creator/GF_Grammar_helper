import os
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from src.config.config import NEW_PGF_AUTO_GEN_DIR
from src.constrained_generation.gf_runtime import GFServerRuntime
from src import logger

# fix random seed for reproducibility
random.seed(42)


def calculate_latency(gf_server):
    times = gf_server.random_decode(n=512, tokens2exclude={"2"})
    mean = np.mean(times)
    return mean


def create_gf_server():
    pgf_dir = NEW_PGF_AUTO_GEN_DIR
    task = args.task
    grammar_type = args.grammar_type
    dataset = args.dataset
    grammars = os.listdir(os.path.join(pgf_dir, task, grammar_type, dataset))
    grammar_name = random.choice(grammars)
    relative_path = f"{task}/{grammar_type}/{dataset}/{grammar_name}"
    return GFServerRuntime(default_pgf=relative_path, grammar_dir=pgf_dir)


def multithreading_run(batch=10):
    # Create a pool of gf_server instances
    gf_servers = [create_gf_server() for _ in range(batch)]
    start = time.time()
    # Use ThreadPoolExecutor to handle multithreading
    with ThreadPoolExecutor(max_workers=batch) as executor:
        latency_means = list(executor.map(calculate_latency, gf_servers))
    end = time.time()
    total_time = end - start
    mean = total_time / batch / 512
    logger.info(f"Overall Mean: {mean}")
    return mean


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

    args = parser.parse_args()

    pgf_dir = NEW_PGF_AUTO_GEN_DIR
    task = args.task
    grammar_type = args.grammar_type
    dataset = args.dataset

    REPEAT = 4
    BATCH = 1
    latency_per_token_list = []
    for _ in range(REPEAT):
        latency_per_token = multithreading_run(batch=BATCH)
        latency_per_token_list.append(latency_per_token)

    mean = np.mean(latency_per_token_list)
    std = np.std(latency_per_token_list)

    logger.info(f"Mean: {mean}")
    logger.info(f"Std: {std}")
