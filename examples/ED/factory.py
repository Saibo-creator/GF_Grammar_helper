import json
from typing import List, Dict

from src.ED_grammar.factory import EDGrammarFactory
from src.config.config import DATA_PATHS

if __name__ == "__main__":
    tokenizer_path = "saibo/llama-7B"
    factory = EDGrammarFactory(
        tokenizer_path=tokenizer_path, grammar_type="canonical", literal=False
    )

    dataset = "aida"

    dataset_jsonl = DATA_PATHS["ED"]["Tasks"][dataset]

    # entities_path = DATA_PATHS["ED"]["KB"][None]["entity"]
    # entities: List[str] = read_jsonl(entities_path)
    with open(dataset_jsonl, "r", encoding="utf-8") as f:
        dps: List[Dict] = [json.loads(line) for line in f]

    dataset = {
        "dps": dps,
        "name": dataset,
    }

    factory.build_bigrammars(dataset=dataset, total=10, save_to_gf=True)
