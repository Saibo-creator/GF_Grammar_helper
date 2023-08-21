import json
import os
from typing import List, Optional, Set

from src.production import Production, AbstractProduction, ConcreteProduction


class Grammar:
    _default_flags = {"coding": "utf8"}

    Type = None  # This serves as a placeholder that child classes must override
    ProductionType = (
        None  # This serves as a placeholder that child classes must override
    )

    def __init__(
        self,
        name,
        start,
        productions: List[Production],
        categories: Optional[Set[str]] = None,
        flags=None,
        **kwargs,
    ):
        self.set_name(name)
        self._start = start
        self._productions = productions
        self._categories = categories or self._infer_categories()
        self._flags = self._default_flags.copy()
        self._flags.update({"startcat": start})
        self._flags.update(flags or {})

    @property
    def name(self):
        return self._name

    @property
    def start(self):
        return self._start

    @property
    def productions(self):
        return self._productions

    @property
    def categories(self):
        return self._categories

    def set_name(self, name):
        self._validate_name(name)
        self._name = name
        self._after_set_name(name)

    @staticmethod
    def _validate_name(name):
        if "-" in name:
            raise ValueError(f"'-' is not allowed in grammar name, but got {name}")

    def _after_set_name(self, name):
        pass

    def add_production_rules(self, prod_rules: List[Production]):
        assert isinstance(
            prod_rules[0], self.ProductionType
        ), f"Expected {self.ProductionType} but got {type(prod_rules[0])}"
        self._productions.extend(prod_rules)

    @property
    def count_prod(self):
        return len(self._productions)

    @property
    def count_cat(self):
        return len(self._categories)

    def _infer_categories(self):
        raise NotImplementedError

    def _get_grammar_header_str(self) -> str:
        raise NotImplementedError

    def _get_grammar_flags_str(self) -> str:
        raise NotImplementedError

    def _get_grammar_categories_str(self) -> str:
        raise NotImplementedError

    def _get_grammar_productions_str(self) -> str:
        raise NotImplementedError

    def __str__(self):
        header: str = self._get_grammar_header_str()
        flags: str = self._get_grammar_flags_str()
        categories: str = self._get_grammar_categories_str()
        productions: str = self._get_grammar_productions_str()
        return f"{header} = {{\n {flags} {categories} {productions} }}\n"

    def _summary(self):
        return f"Grammar {self._name} with {self.count_prod} productions and {self.count_cat} categories"

    def summary(self):
        print(self._summary())

    # save to .gf file
    def _save(self, path: str):
        with open(path, "w") as f:
            f.write(str(self))

    # save with dir and name
    def save(self, dir: str = "."):
        """
        Save the grammar to a file.
        """
        # if dir does not exist, create it
        if not os.path.exists(dir):
            os.makedirs(dir)

        name = self._name
        path = os.path.join(dir, name)

        # Ensure the path ends with .gf
        if not path.endswith(".gf"):
            path += ".gf"

        self._save(path)

    @classmethod
    def from_json(cls, path: str):
        """
        Read a grammar from a json file.
        """
        with open(path, "r") as f:
            json_obj = json.load(f)
        type = json_obj.pop("type")
        assert (
            type == cls.Type
        ), f"Expected grammar type {cls.Type}, got type {type} in json file {path}"
        name = json_obj.pop("name")
        productions = [
            cls.ProductionType.from_str(p) for p in json_obj.pop("productions")
        ]
        start = json_obj.pop("start", None)
        categories = json_obj.pop("categories", None)

        # remaining is kwargs
        kwargs = json_obj
        return cls(
            name, start=start, productions=productions, categories=categories, **kwargs
        )


class AbstractGrammar(Grammar):
    Type = "abstract"
    ProductionType = AbstractProduction

    def __init__(
        self, name, start, productions: List[Production], flags=None, **kwargs
    ):
        # categories are not mandatory for abstract grammars
        super().__init__(name, start, productions, flags=flags, **kwargs)

    def _infer_categories(self):
        categories = set()
        for production in self._productions:
            categories.update(production.lhs())
            categories.update({production.rhs()})

        return categories

    def add_production_rules(self, prod_rules: List[Production]):
        super().add_production_rules(prod_rules)
        # update categories
        self._categories = self._infer_categories()

    def _get_grammar_header_str(self) -> str:
        return f"abstract {self._name}"

    def _get_grammar_flags_str(self) -> str:
        """
        flags coding = utf8 ;
        flags startcat = Text ;
        ...
        """
        return "\n".join([f"flags {k} = {v} ;" for k, v in self._flags.items()]) + "\n"

    def _get_grammar_categories_str(self) -> str:
        """
        cat
          Text ; BOG ; EOG ; Mention; Entity ; OpenBracket ; CloseBracket ; Canonical_phrase ;
        """

        sorted_categories = sorted(self._categories)
        return f"cat\n\t{'; '.join(sorted_categories)} ;\n"

    def _get_grammar_productions_str(self) -> str:
        """
        fun
          Start: BOG -> Mention -> Canonical_phrase -> OpenBracket -> Entity -> CloseBracket -> EOG -> Text ;
          Materialise_BOG: BOG;
          Materialise_EOG: EOG;
        """
        result = "fun\n"
        for production in self._productions:
            result += f"\t{production}\n"
        return result


class ConcreteGrammar(Grammar):
    Type = "concrete"
    ProductionType = ConcreteProduction

    def __init__(
        self,
        name,
        start,
        productions: List[Production],
        categories: Set[str],
        flags=None,
        abstract_grammar_name=None,
        **kwargs,
    ):
        self._initializing = True
        super().__init__(name, start, productions, categories, flags, **kwargs)
        assert (
            abstract_grammar_name is not None
        ), "abstract_grammar_name must be provided"
        self._abstract_grammar_name = abstract_grammar_name
        self._initializing = False

    def set_name(self, name):
        # only allow setting name during initialization
        # This is because the name of a concrete grammar is derived from the name of the abstract grammar
        # so we don't want to allow changing it.
        # If you want to change the name of a concrete grammar,
        # use set_abstract_grammar_name instead.
        if not self._initializing:
            raise RuntimeError(
                "Cannot set name of concrete grammar directly. Use set_abstract_grammar_name instead."
            )
        super().set_name(name)

    def set_concrete_name(self, abs_name, str_or_int: str, tokenizer: str, **kwargs):
        self._validate_name(abs_name)
        self._abstract_grammar_name = abs_name
        str_or_int = str_or_int.lower().strip("_")
        tokenizer = tokenizer.lower().strip("_")
        crt_name = "_".join([abs_name, str_or_int, tokenizer])
        for k, v in kwargs.items():
            if v is not None:
                v = v.lower().strip("_")
                crt_name += f"_{v}"
        self._validate_name(crt_name)
        self._name = crt_name

    def _get_grammar_header_str(self) -> str:
        return f"concrete {self._name} of {self._abstract_grammar_name}"

    def _get_grammar_flags_str(self) -> str:
        return ""

    def _get_grammar_categories_str(self) -> str:
        sorted_categories = sorted(self._categories)

        result = "lincat\n"
        result += "\t" + ", ".join(sorted_categories)
        result += " = Str ;\n"
        return result

    def _get_grammar_productions_str(self) -> str:
        """
        lin
          Start = {s} ;
          Materialise_BOG = {s} ;
          Materialise_EOG = {s} ;
        """
        result = "lin\n"
        for production in self._productions:
            result += f"\t{production}\n"
        return result


if __name__ == "__main__":
    ED_dep_canonical_grammar = AbstractGrammar(
        name="ED_dep_canonical_grammar",
        start="Start",
        productions=[
            AbstractProduction(
                name="Start",
                lhs=[
                    "BOG",
                    "Mention",
                    "Canonical_phrase",
                    "OpenBracket",
                    "Entity",
                    "CloseBracket",
                    "EOG",
                ],
                rhs="Text",
            ),
            AbstractProduction(
                name="Materialise_BOG",
                lhs=[],
                rhs="BOG",
            ),
            AbstractProduction(
                name="Materialise_EOG",
                lhs=[],
                rhs="EOG",
            ),
            AbstractProduction(
                name="Materialise_Mention",
                lhs=[],
                rhs="Mention",
            ),
            AbstractProduction(
                name="Materialise_OpenBracket",
                lhs=[],
                rhs="OpenBracket",
            ),
            AbstractProduction(
                name="Materialise_CloseBracket",
                lhs=[],
                rhs="CloseBracket",
            ),
            AbstractProduction(
                name="Materialise_Canonical_phrase",
                lhs=[],
                rhs="Canonical_phrase",
            ),
            AbstractProduction(
                name="Materialise_Entity",
                lhs=[],
                rhs="Entity",
            ),
        ],
    )
    print(ED_dep_canonical_grammar)

    ED_dep_canonical_grammar = ConcreteGrammar(
        name="ED_dep_canonical_grammar",
        start="Start",
        productions=[
            ConcreteProduction(
                name="Start",
                lhs=[
                    "BOG",
                    "Mention",
                    "Canonical_phrase",
                    "OpenBracket",
                    "Entity",
                    "CloseBracket",
                    "EOG",
                ],
                rhs_elements=None,
            ),
            ConcreteProduction(
                name="Materialise_BOG",
                lhs=[],
                rhs_elements="BOG",
            ),
            ConcreteProduction(
                name="Materialise_EOG",
                lhs=[],
                rhs_elements="EOG",
            ),
            ConcreteProduction(
                name="Materialise_Mention",
                lhs=[],
                rhs_elements="Mention",
            ),
            ConcreteProduction(
                name="Materialise_OpenBracket",
                lhs=[],
                rhs_elements="[",
            ),
            ConcreteProduction(
                name="Materialise_CloseBracket",
                lhs=[],
                rhs_elements="]",
            ),
            ConcreteProduction(
                name="Materialise_Canonical_phrase",
                lhs=[],
                rhs_elements="token1 token2 token3",
            ),
            ConcreteProduction(
                name="Materialise_Entity",
                lhs=[],
                rhs_elements="Entity",
            ),
        ],
        categories={
            "BOG",
            "Mention",
            "Canonical_phrase",
            "OpenBracket",
            "Entity",
            "CloseBracket",
            "EOG",
        },
        abstract_grammar_name="ED_dep_canonical_grammar",
    )
    print(ED_dep_canonical_grammar)
