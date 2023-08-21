import os.path
from typing import Dict, List

from src.GrammarFactory import GrammarFactory
from src.grammar import ConcreteGrammar


class EDGrammarFactory(GrammarFactory):
    def __init__(self, grammar_type: str, tokenizer_path: str, literal: bool = False):
        super().__init__(
            task="ED",
            grammar_type=grammar_type,
            tokenizer_path=tokenizer_path,
            literal=literal,
        )
        self._default_grammar_output_dir = os.path.join(
            self._default_grammar_output_dir, "ED", grammar_type
        )

    def _preprocess_dp_for_abs_grammar(self, data_point: Dict):
        base_config = super()._preprocess_dp_for_abs_grammar(data_point)
        entities: List[str] = data_point.get("candidates", None)
        base_config.update({"entities": entities})
        return base_config

    def _preprocess_dp_for_crt_grammar(self, data_point: Dict):
        base_config = super()._preprocess_dp_for_crt_grammar(data_point)
        entities: List[str] = data_point.get("candidates", None)
        mention: str = data_point.get("mention", None)
        base_config.update({"entities": entities, "mention": mention})
        return base_config

    def _postprocess_crt_grammar(
        self, crt_grammar: ConcreteGrammar, **kwargs
    ) -> ConcreteGrammar:
        abs_name = kwargs["abs_name"]
        str_or_int = "str" if self.literal else "int"
        tokenizer = "llama"
        crt_grammar.set_concrete_name(abs_name, str_or_int, tokenizer)
        return crt_grammar
