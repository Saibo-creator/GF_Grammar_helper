import json
import os
from typing import List, Optional, Set, Union, Dict

from src.new_utils import Tokenization, LiteralStr, tokenize
from src.utils import get_hashed_name


class TerminalItem:
    def __init__(self, text: str, name: str = None):
        self._text = text
        self._name = name

    @property
    def name(self) -> str:
        if self._name is not None:
            return self._name
        else:
            return self.hash

    @property
    def text(self) -> str:
        return self._text

    @property
    def hash(self) -> str:
        return get_hashed_name(string=self._text)

    def _get_name_from_text(self) -> str:
        return get_hashed_name(string=self._text)


class EntityTerminalItem(TerminalItem):
    def __init__(self, entity: str):
        super().__init__(text=entity, name=None)

    @property
    def name(self) -> str:
        _name = super().name
        return f"Ent_{_name}"

    def __str__(self):
        return f"{self.name}: Entity"


class RelationTerminalItem(TerminalItem):
    def __init__(self, relation: str):
        super().__init__(text=relation, name=None)

    @property
    def name(self) -> str:
        _name = super().name
        return f"Rel_{_name}"

    def __str__(self):
        return f"{self.name}: Rel"


class Production:
    """
    A grammar production.  Each production maps a single symbol
    on the "left-hand side" to a sequence of symbols on the
    "right-hand side".  (In the case of context-free productions,
    the left-hand side must be a ``Nonterminal``, and the right-hand
    side is a sequence of terminals and ``Nonterminals``.)
    "terminals" can be any immutable hashable object that is
    not a ``Nonterminal``.  Typically, terminals are strings
    representing words, such as ``"dog"`` or ``"under"``.
    """

    def __init__(self, name: str, lhs: List[str], rhs: str):
        """
        Construct a new ``Production``.

        :param lhs: The left-hand side of the new ``Production``.
        :type lhs: Nonterminal
        :param rhs: The right-hand side of the new ``Production``.
        :type rhs: sequence(Nonterminal and terminal)
        """
        if isinstance(lhs, str):
            raise TypeError(
                "production right hand side should be a list, " "not a string"
            )
        self._name = name
        self._lhs = lhs
        self._rhs = rhs

    def lhs(self) -> List[str]:
        """
        Return the left-hand side of this ``Production``.

        :rtype: Nonterminal
        """
        return self._lhs

    def rhs(self) -> str:
        """
        Return the right-hand side of this ``Production``.

        :rtype: sequence(Nonterminal and terminal)
        """
        return self._rhs

    def __str__(self):
        raise NotImplementedError

    @classmethod
    def from_str(cls, string: str):
        params: Dict = cls._parse_str(string)
        return cls(**params)

    @staticmethod
    def _parse_str(string: str) -> Dict:
        raise NotImplementedError


class AbstractProduction(Production):
    def __init__(self, name: str, lhs: List[str], rhs: str):
        super().__init__(name, lhs, rhs)

    def __str__(self):
        """
        Return a verbose string representation of the ``Production``.

        Examples:
            Derive_HyphenFunctionTag: Hyphen -> FunctionTag -> HyphenFunctionTag;
            Empty_HyphenFunctionTag: HyphenFunctionTag;

        :rtype: str
        """
        result = f"{self._name}: "
        for el in self._lhs:
            result += f"{el} -> "
        result += f"{self._rhs};"
        return result

    def is_nonlexical(self):
        """
        Return True if the right-hand side only contains ``Nonterminals``

        Derive_HyphenNumTag: Hyphen -> Num -> HyphenNumTag;

        :rtype: bool
        """
        return not self.is_lexical()

    def is_lexical(self):
        """
        Return True if the right-hand contain at least one terminal token.

        Materialize_Hyphen: Hyphen;
        Materialize_SentenceTag: SentenceTag;
        Materialize_Left: Left;
        Materialize_Right: Right;

        :rtype: bool
        """
        return len(self._rhs) == 0

    @staticmethod
    def _parse_str(string: str) -> Dict:
        line = string.strip().strip(";")
        _name, _production_body = line.split(":")
        name = _name.strip()
        _elements = _production_body.split("->")
        elements = [element.strip() for element in _elements]
        lhs = elements[:-1]
        rhs = elements[-1]
        return {"name": name, "lhs": lhs, "rhs": rhs}


class ConcreteProduction(Production):
    """
    A grammar production.  Each production maps a single symbol
    on the "left-hand side" to a sequence of symbols on the
    "right-hand side".  (In the case of context-free productions,
    the left-hand side must be a ``Nonterminal``, and the right-hand
    side is a sequence of terminals and ``Nonterminals``.)
    "terminals" can be any immutable hashable object that is
    not a ``Nonterminal``.  Typically, terminals are strings
    representing words, such as ``"dog"`` or ``"under"``.
    """

    def __init__(self, name: str, lhs: List[str], rhs: Union[List[str], str] = None):
        if isinstance(rhs, List):
            rhs: str = self._join_rhs(rhs)
        super().__init__(name, lhs, rhs)

        if rhs is None:
            self._rhs = self._full_join_lhs()

    def _full_join_lhs(self) -> str:
        rhs = self._join_rhs(self._lhs)
        return rhs

    @staticmethod
    def _join_rhs(rhs: List[str]) -> str:
        rhs = " ++ ".join(rhs)
        return rhs

    def __str__(self):
        """
        Derive_Tree a b c d = a ++ b ++ c ++ d;

        """

        result = f"{self._name} "
        result += " ".join(self._lhs)
        result += f" = {self._rhs};"

        return result

    @staticmethod
    def _parse_str(line: str) -> Dict:
        line: str = line.strip().strip(";")
        _name, _production_body = line.split(" ", maxsplit=1)
        name: str = _name.strip()
        _lhs, _rhs = _production_body.split("=")
        lhs: List[str] = _lhs.strip().split(" ")
        rhs: str = _rhs.strip()
        return {"name": name, "lhs": lhs, "rhs": rhs}


class CrtTerminalProduction(ConcreteProduction):
    @classmethod
    def _from_tokenization(
        cls, tokenization: Tokenization, literal: bool, name: str = None
    ):
        rhs = tokenization.tokens if literal else tokenization.token_ids
        rhs = [str(token) for token in rhs]
        return cls(name, lhs=[], rhs=rhs)

    @classmethod
    def from_terminal(cls, terminal: TerminalItem, tokenizer, literal: bool):
        name = terminal.name
        tokenization = tokenize(tokenizer, text=terminal.text)
        return cls._from_tokenization(tokenization, literal, name=name)


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
            categories.union(production.lhs())
            categories.add(production.rhs())

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

    def set_concrete_name(
        self, abs_name, str_or_int: str, tokenizer: str, concrete_postfix="concrete"
    ):
        self._validate_name(abs_name)
        self._abstract_grammar_name = abs_name
        str_or_int = str_or_int.lower().strip("_")
        tokenizer = tokenizer.lower().strip("_")
        concrete_postfix = concrete_postfix.lower().strip("_")
        crt_name = "_".join([abs_name, str_or_int, tokenizer, concrete_postfix])
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
                rhs=None,
            ),
            ConcreteProduction(
                name="Materialise_BOG",
                lhs=[],
                rhs="BOG",
            ),
            ConcreteProduction(
                name="Materialise_EOG",
                lhs=[],
                rhs="EOG",
            ),
            ConcreteProduction(
                name="Materialise_Mention",
                lhs=[],
                rhs="Mention",
            ),
            ConcreteProduction(
                name="Materialise_OpenBracket",
                lhs=[],
                rhs="[",
            ),
            ConcreteProduction(
                name="Materialise_CloseBracket",
                lhs=[],
                rhs="]",
            ),
            ConcreteProduction(
                name="Materialise_Canonical_phrase",
                lhs=[],
                rhs="token1 token2 token3",
            ),
            ConcreteProduction(
                name="Materialise_Entity",
                lhs=[],
                rhs="Entity",
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
