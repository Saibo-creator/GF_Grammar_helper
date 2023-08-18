import json
import os
from typing import List, Optional, Set, Union, Tuple, Dict


class LiteralString(str):
    """
    A subclass of ``str`` that is used to represent terminals in grammars.
    Instead of printing as ``dog``, it prints as ``"dog"``(with quotes).
    """

    # def __str__(self):
    #     return f'"{super().__str__()}"'

    def __new__(cls, content):
        # Add quotes to the content
        instance = super().__new__(cls, f'"{content}"')
        return instance


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
    def from_string(cls, string: str):
        params: Dict = cls._parse_string(string)
        return cls(**params)

    @staticmethod
    def _parse_string(string: str) -> Dict:
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
    def _parse_string(string: str) -> Dict:
        line = string.strip().strip(";")
        _name, _production_body = line.split(":")
        name = _name.strip()
        _elements = _production_body.split("->")
        elements = [element.strip() for element in _elements]
        lhs = elements[:-2]
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
    def _parse_string(line: str) -> Dict:
        line: str = line.strip().strip(";")
        _name, _production_body = line.split(" ", maxsplit=1)
        name: str = _name.strip()
        _lhs, _rhs = _production_body.split("=")
        lhs: List[str] = _lhs.strip().split(" ")
        rhs: str = _rhs.strip()
        return {"name": name, "lhs": lhs, "rhs": rhs}


class Grammar:
    _default_flags = {"coding": "utf8"}

    ProductionType = None  # This serves as a placeholder that child classes must override

    def __init__(self, name, start, productions: List[Production], categories: Optional[Set[str]] = None, flags=None,
                 **kwargs):
        self._name = name
        self._start = start
        self._productions = productions
        self._categories = categories or self._infer_categories()
        self._flags = self._default_flags.copy()
        self._flags.update({"startcat": start})
        self._flags.update(flags or {})

    def get_start(self):
        return self._start

    def get_productions(self):
        return self._productions

    def get_categories(self):
        return self._categories

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
        if not path.endswith('.gf'):
            path += '.gf'


    # @classmethod
    # def _parse_productions(cls, src: str) -> List[Production]:
    #     """
    #     Parse a grammar file and return a list of ``Production`` objects.
    #     :param src: The grammar source string.
    #     :type src: str
    #     :return: A list of ``Production`` objects.
    #     :rtype: list(Production)
    #     """
    #     productions = []
    #     for lineno, line in enumerate(src.splitlines()):
    #         line = line.strip()
    #         if not line:
    #             continue
    #         productions.append(cls.ProductionType.from_string(line))
    #     return productions

    # @staticmethod
    # def _parse_categories(src: str) -> Optional[Dict]:
    #     """
    #     Parse a grammar file and return a set of categories.
    #     :param src: The grammar source string.
    #     :type src: str
    #     :return: A set of categories.
    #     :rtype: set(str)
    #     """
    #     # read the first line and check if it is "cat"
    #     first_line = src.splitlines()[0].strip()
    #     if first_line.startswith("cat:"):
    #         # remove "cat:" and split by ", "
    #         start = first_line[4:].split(", ")[0]
    #         categories = set(first_line[4:].split(", "))
    #         # remove empty strings
    #         categories = {cat.strip() for cat in categories if cat.strip()}
    #         return {"start": start, "categories": categories}
    #     else:
    #         return None



    @classmethod
    def from_json(cls, path: str):
        """
        Read a grammar from a json file.
        """
        with open(path, "r") as f:
            json_obj = json.load(f)
        name = json_obj.pop("name")
        productions = [cls.ProductionType.from_string(p) for p in json_obj.pop("productions")]
        start = json_obj.pop("start", None)
        categories = json_obj.pop("categories", None)

        # remaining is kwargs
        kwargs = json_obj
        return cls(name, start=start, productions=productions, categories=categories, **kwargs)


class AbstractGrammar(Grammar):
    ProductionType = AbstractProduction

    def __init__(self, name, start, productions: List[Production],categories=None, flags=None, **kwargs):
         # categories are not mandatory for abstract grammars
        super().__init__(name, start, productions, categories=categories, flags=flags, **kwargs)

    def _infer_categories(self):
        categories = set()
        for production in self._productions:
            categories.union(production.lhs())
            categories.add(production.rhs())

        return categories

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
    ProductionType = ConcreteProduction

    def __init__(self, name, start, productions: List[Production], categories: Set[str], flags=None,
                 abstract_grammar_name=None, **kwargs):
        super().__init__(name, start, productions, categories, flags, **kwargs)
        assert abstract_grammar_name is not None, "abstract_grammar_name must be provided"
        self._abstract_grammar_name = abstract_grammar_name

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




if __name__ == '__main__':
    ED_dep_canonical_grammar = AbstractGrammar(
        name="ED_dep_canonical_grammar",
        start="Start",
        productions=[
            AbstractProduction
                (
                name="Start",
                lhs=["BOG", "Mention", "Canonical_phrase", "OpenBracket", "Entity", "CloseBracket", "EOG"],
                rhs="Text",
            ),
            AbstractProduction
                (
                name="Materialise_BOG",
                lhs=[],
                rhs="BOG",
            ),
            AbstractProduction
                (
                name="Materialise_EOG",
                lhs=[],
                rhs="EOG",
            ),
            AbstractProduction
                (
                name="Materialise_Mention",
                lhs=[],
                rhs="Mention",
            ),
            AbstractProduction
                (
                name="Materialise_OpenBracket",
                lhs=[],
                rhs="OpenBracket",
            ),
            AbstractProduction
                (
                name="Materialise_CloseBracket",
                lhs=[],
                rhs="CloseBracket",
            ),
            AbstractProduction
                (
                name="Materialise_Canonical_phrase",
                lhs=[],
                rhs="Canonical_phrase",
            ),
            AbstractProduction
                (
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
            ConcreteProduction
                (
                name="Start",
                lhs=["BOG", "Mention", "Canonical_phrase", "OpenBracket", "Entity", "CloseBracket", "EOG"],
                rhs=None,
            ),
            ConcreteProduction
                (
                name="Materialise_BOG",
                lhs=[],
                rhs="BOG",
            ),
            ConcreteProduction
                (
                name="Materialise_EOG",
                lhs=[],
                rhs="EOG",
            ),
            ConcreteProduction
                (
                name="Materialise_Mention",
                lhs=[],
                rhs="Mention",
            ),
            ConcreteProduction
                (
                name="Materialise_OpenBracket",
                lhs=[],
                rhs="[",
            ),
            ConcreteProduction
                (
                name="Materialise_CloseBracket",
                lhs=[],
                rhs="]",
            ),
            ConcreteProduction
                (
                name="Materialise_Canonical_phrase",
                lhs=[],
                rhs="token1 token2 token3",
            ),
            ConcreteProduction
                (
                name="Materialise_Entity",
                lhs=[],
                rhs="Entity",
            ),
        ],
        categories={"BOG", "Mention", "Canonical_phrase", "OpenBracket", "Entity", "CloseBracket", "EOG"},
        abstract_grammar_name="ED_dep_canonical_grammar"
    )
    print(ED_dep_canonical_grammar)
