import json
from typing import List, Dict

from src.IE_grammar.factory import IEGrammarFactory
from src.compilation import compile_for_task
from src.config.config import DATA_PATHS

if __name__ == "__main__":
    tokenizer_path = "saibo/llama-7B"

    task, grammar_type, dataset_name = "IE", "fe", "wikinre"
    literal = False

    factory = IEGrammarFactory(
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

    # compile_grammar_dir(grammar_src_dir, pgf_output_dir, verbose=True, clean=True)

    compile_for_task(
        task=task, grammar_type=grammar_type, dataset=dataset_name, verbose=True
    )
