import os.path
from typing import Dict, List

from src.GrammarFactory import GrammarFactory
from src.grammar import ConcreteGrammar


class CPGrammarFactory(GrammarFactory):
    def __init__(self, grammar_type: str, tokenizer_path: str, literal: bool = False):
        super().__init__(
            task="CP",
            grammar_type=grammar_type,
            tokenizer_path=tokenizer_path,
            literal=literal,
        )
        self._default_grammar_output_dir = os.path.join(
            self._default_grammar_output_dir, "CP", grammar_type
        )

    def _preprocess_dp_for_abs_grammar(self, data_point: Dict):
        base_config = super()._preprocess_dp_for_abs_grammar(data_point)
        tokens: List[str] = data_point.get("tokens", None)
        num_input_words = len(tokens)
        base_config.update({"num_input_words": num_input_words})
        return base_config

    def _preprocess_dp_for_crt_grammar(self, data_point: Dict):
        base_config = super()._preprocess_dp_for_crt_grammar(data_point)
        words: List[str] = data_point.get("words", None)
        base_config.update({"words": words})
        return base_config
