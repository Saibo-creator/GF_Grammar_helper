import json
import os
from typing import List, Dict

from src.CP_grammar.abs_grammar import CP_AbstractGrammar
from src.config.config import DATA_PATHS, JSON_GF_ASSET_DIR

if __name__ == "__main__":

    WORKING_FILE_DIR = os.path.dirname(os.path.abspath(__file__))

    task, grammar_type, dataset = "CP", "re", "ptb"

    ABS_BASE_JSON_PATH = os.path.join(
        JSON_GF_ASSET_DIR, task, grammar_type, "abstract.json"
    )

    dataset_jsonl = DATA_PATHS[task]["Tasks"][dataset]

    # entities_path = DATA_PATHS["ED"]["KB"][None]["entity"]
    # entities: List[str] = read_jsonl(entities_path)
    with open(dataset_jsonl, "r", encoding="utf-8") as f:
        dps: List[Dict] = [json.loads(line) for line in f]

    for dp in dps[:1]:
        tokens = dp.get("tokens", None)

        abs_grammar = CP_AbstractGrammar(
            base_abs_grammar_path=ABS_BASE_JSON_PATH,
            num_input_words=len(tokens),
            name="CP_re_ptb_dp0",
        )
        abs_grammar.save(dir=os.path.join(WORKING_FILE_DIR))

        abs_grammar.summary()
