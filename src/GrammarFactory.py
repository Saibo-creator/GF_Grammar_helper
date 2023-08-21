import os.path
from typing import Tuple, Callable, Dict

from src.bigrammar import BiGrammar
from src.config.config import GF_AUTO_GEN_GF_DIR, GRAMMAR_JSON_CONFIG_ASSET_DIR
from src.CP_grammar.abs_grammar import CP_AbstractGrammar
from src.CP_grammar.crt_grammar import CP_ConcreteGrammar
from src.ED_grammar.abs_grammar import ED_AbstractGrammar
from src.ED_grammar.crt_grammar import ED_ConcreteGrammar
from src.IE_grammar.abs_grammar import IE_AbstractGrammar
from src.IE_grammar.crt_grammar import IE_ConcreteGrammar
from src.grammar import AbstractGrammar, ConcreteGrammar

from transformers import AutoTokenizer

# Define a dictionary to map tasks to their respective classes.
GRAMMAR_CLASSES = {
    "IE": {
        "AbstractGrammar": IE_AbstractGrammar,
        "ConcreteGrammar": IE_ConcreteGrammar,
    },
    "CP": {
        "AbstractGrammar": CP_AbstractGrammar,
        "ConcreteGrammar": CP_ConcreteGrammar,
    },
    "ED": {
        "AbstractGrammar": ED_AbstractGrammar,
        "ConcreteGrammar": ED_ConcreteGrammar,
    },
}


def _lookup_grammar_classes(task) -> Tuple[Callable, Callable]:
    try:
        abs_grammar_cls = GRAMMAR_CLASSES[task]["AbstractGrammar"]
        crt_grammar_cls = GRAMMAR_CLASSES[task]["ConcreteGrammar"]
    except KeyError:
        raise NotImplementedError(f"Task '{task}' is not implemented.")
    return abs_grammar_cls, crt_grammar_cls


def _lookup_grammar_base_json_config(task, grammar_type):
    try:
        base_abs_grammar_path = os.path.join(
            GRAMMAR_JSON_CONFIG_ASSET_DIR, task, grammar_type, "abstract.json"
        )
        base_crt_grammar_path = os.path.join(
            GRAMMAR_JSON_CONFIG_ASSET_DIR, task, grammar_type, "concrete.json"
        )
    except KeyError:
        raise NotImplementedError(f"Task '{task}' is not implemented.")
    return base_abs_grammar_path, base_crt_grammar_path


class GrammarFactory:

    _default_grammar_json_config_asset_dir = GRAMMAR_JSON_CONFIG_ASSET_DIR
    _default_grammar_output_dir = GF_AUTO_GEN_GF_DIR
    _grammar_product_kind: str = None

    def __init__(
        self, task: str, grammar_type: str, tokenizer_path: str, literal=False
    ):
        self.Abs_grammar_cls, self.Crt_grammar_cls = _lookup_grammar_classes(task)
        (
            self.base_abs_grammar_config_path,
            self.base_crt_grammar_config_path,
        ) = _lookup_grammar_base_json_config(task, grammar_type)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, use_fast=False)
        self.tokenizer_name = tokenizer_path.split("/")[-1].replace(
            "-", "_"
        )  # e.g. "llama_7B", "-" is not allowed in grammar name
        self.literal = literal
        self._grammar_product_kind = f"{task}_{grammar_type}"

    def __validate_data_point(self, data_point):
        if data_point.get("dataset", None) is None:
            raise ValueError("data_point must have 'dataset' key.")
        if data_point.get("id", None) is None:
            raise ValueError("data_point must have 'id' key.")
        return True

    def _preprocess_dp_for_abs_grammar(self, data_point: Dict) -> Dict:
        config = {
            "name": f"{self._grammar_product_kind}_{data_point['dataset']}_{data_point['id']}",
            "base_abs_grammar_path": self.base_abs_grammar_config_path,
        }
        return config

    def _postprocess_abs_grammar(
        self, abs_grammar: AbstractGrammar, **kwargs
    ) -> AbstractGrammar:
        return abs_grammar

    def _preprocess_dp_for_crt_grammar(self, data_point: Dict):
        config = {
            "base_crt_grammar_path": self.base_crt_grammar_config_path,
            "tokenizer": self.tokenizer,
            "literal": self.literal,
        }
        return config

    def _postprocess_crt_grammar(
        self, crt_grammar: ConcreteGrammar, **kwargs
    ) -> ConcreteGrammar:
        return crt_grammar

    def _build_abs_grammar(
        self,
        data_point: Dict,
        custom_config: Dict = None,
        postprocess_kwargs: Dict = None,
    ) -> AbstractGrammar:
        """
        data_point needs to contain two keys: 'dataset' and 'id'
        """
        custom_config = custom_config or {}  # None Type is not iterable for ** operator
        postprocess_kwargs = postprocess_kwargs or {}
        dp_config: Dict = self._preprocess_dp_for_abs_grammar(data_point)
        grammar = self.Abs_grammar_cls(**dp_config, **custom_config)
        return self._postprocess_abs_grammar(grammar, **postprocess_kwargs)

    def _build_crt_grammar(
        self,
        data_point: Dict,
        custom_config: Dict = None,
        postprocess_kwargs: Dict = None,
    ) -> ConcreteGrammar:
        """
        data_point needs to contain two keys: 'abstract_grammar_name' and 'name'
        """
        custom_config = custom_config or {}  # None Type is not iterable for ** operator
        postprocess_kwargs = postprocess_kwargs or {}
        dp_config = self._preprocess_dp_for_crt_grammar(data_point)
        grammar = self.Crt_grammar_cls(**dp_config, **custom_config)
        return self._postprocess_crt_grammar(grammar, **postprocess_kwargs)

    def build_bigrammar(self, data_point, custom_config=None):
        if self.__validate_data_point(data_point):
            abs_grammar = self._build_abs_grammar(data_point, custom_config)
            crt_grammar = self._build_crt_grammar(
                data_point,
                custom_config,
                postprocess_kwargs={"abs_name": abs_grammar.name},
            )
            return BiGrammar(abs_grammar, crt_grammar)

    def build_bigrammars(self, dataset: Dict, total=None, save_to_gf=False):
        """
        dataset: a dictionary containing two keys: 'name' and 'dps'(a list of data points)
        """
        total = min(total, len(dataset)) if total is not None else len(dataset)
        bigrammars = []
        dataset_name = dataset["name"]
        output_dir = os.path.join(self._default_grammar_output_dir, dataset_name)
        for i in range(0, total):
            dp = dataset["dps"][i]
            dp["id"] = i
            dp["dataset"] = dataset_name
            bigrammar = self.build_bigrammar(dp)
            bigrammars.append(bigrammar)
            if save_to_gf:
                bigrammar.save_to_gf(output_dir)

        return bigrammars
