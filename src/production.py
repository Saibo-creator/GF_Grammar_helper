from typing import List, Dict, Union

from src.new_utils import Tokenization, tokenize
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

    def __init__(
        self, name: str, lhs: List[str], rhs_elements: List[str] = None, rhs: str = None
    ):
        if rhs_elements:
            rhs: str = self._join_rhs(rhs_elements)
        super().__init__(name, lhs, rhs)

        if rhs_elements is None and rhs is None:
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
        return cls(name, lhs=[], rhs_elements=rhs)

    @classmethod
    def from_terminal(cls, terminal: TerminalItem, tokenizer, literal: bool):
        name = terminal.name
        tokenization = tokenize(tokenizer, text=terminal.text)
        return cls._from_tokenization(tokenization, literal, name=name)
