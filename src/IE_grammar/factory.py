import os.path
from typing import Dict, List

from src.GrammarFactory import GrammarFactory
from src.grammar import ConcreteGrammar


class IEGrammarFactory(GrammarFactory):
    def __init__(self, grammar_type: str, tokenizer_path: str, literal: bool = False):
        super().__init__(
            task="IE",
            grammar_type=grammar_type,
            tokenizer_path=tokenizer_path,
            literal=literal,
        )
        self._default_grammar_output_dir = os.path.join(
            self._default_grammar_output_dir, "IE", grammar_type
        )

    def _preprocess_dp_for_abs_grammar(self, data_point: Dict):
        base_config = super()._preprocess_dp_for_abs_grammar(data_point)
        entities: List[str] = data_point.get("entities", None)
        relations: List[str] = data_point.get("relations", None)
        base_config.update({"entities": entities, "relations": relations})
        return base_config

    def _preprocess_dp_for_crt_grammar(self, data_point: Dict):
        base_config = super()._preprocess_dp_for_crt_grammar(data_point)
        entities: List[str] = data_point.get("entities", None)
        relations: List[str] = data_point.get("relations", None)
        base_config.update({"entities": entities, "relations": relations})
        return base_config
