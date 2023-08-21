from src.production import ConcreteProduction, CrtTerminalProduction, TerminalItem


class Rule0Production(ConcreteProduction):
    @classmethod
    def instantiate(cls):
        # Rule0_A_{i}_{j} a b c = a ++ b ++ c ; ;
        name = f"Rule0"
        lhs = ["a", "b", "c", "d", "e", "f", "g", "h"]
        rhs = None  # rhs will be inferred from lhs
        return cls(name=name, lhs=lhs, rhs_elements=rhs)


class Rule1Production(ConcreteProduction):
    @classmethod
    def instantiate(cls, i: int, j: int):
        # Rule1_B_{i}_{j} a b c = a ++ b ++ c ; ;
        name = f"Rule1_B_{i}_{j}"
        lhs = ["a", "b", "c"]
        rhs = None  # rhs will be inferred from lhs
        return cls(name=name, lhs=lhs, rhs_elements=rhs)


class Rule2Production(ConcreteProduction):
    @classmethod
    def instantiate(cls, i: int, j: int):
        # Rule2_B_{i}_{j} a b c = a ++ b ++ c ; ;
        name = f"Rule2_B_{i}_{j}"
        lhs = ["a", "b", "c"]
        rhs = None  # rhs will be inferred from lhs
        return cls(name=name, lhs=lhs, rhs_elements=rhs)


class Rule4Production(ConcreteProduction):
    @classmethod
    def instantiate(cls, i: int, j: int):
        # Rule4_C_{i}_{j} a b c = a ++ b ++ c ; ;
        name = f"Rule4_C_{i}_{j}"
        lhs = ["a", "b"]
        rhs = None  # rhs will be inferred from lhs
        return cls(name=name, lhs=lhs, rhs_elements=rhs)


class Rule5Production(ConcreteProduction):
    @classmethod
    def instantiate(cls, i: int, n_words: int):
        # Rule5_C_{n_words}_{i} a b c = a ++ b ++ c ; ;
        name = f"Rule5_C_{n_words}_{i}"
        lhs = ["a"]
        rhs = None  # rhs will be inferred from lhs
        return cls(name=name, lhs=lhs, rhs_elements=rhs)


class Rule6Production(ConcreteProduction):
    @classmethod
    def instantiate(cls, i: int, j: int):
        # Rule6_E_{i}_{j} a b c = a ++ b ++ c ; ;
        name = f"Rule6_E_{i}_{j}"
        lhs = ["a", "b"]
        rhs = None  # rhs will be inferred from lhs
        return cls(name=name, lhs=lhs, rhs_elements=rhs)


class Rule7Production(ConcreteProduction):
    @classmethod
    def instantiate(cls, i: int, j: int):
        # Rule7_E_{i}_{j} a b c = a ++ b ++ c ; ;
        name = f"Rule7_E_{i}_{j}"
        lhs = ["a", "b"]
        rhs = None  # rhs will be inferred from lhs
        return cls(name=name, lhs=lhs, rhs_elements=rhs)


class Rule8Production(ConcreteProduction):
    @classmethod
    def instantiate(cls, i: int, n_words: int):
        # Rule8_E_{i}_{j} a b c = a ++ b ++ c ; ;
        name = f"Rule8_E_{n_words}_{i}"
        lhs = ["a", "b"]
        rhs = None  # rhs will be inferred from lhs
        return cls(name=name, lhs=lhs, rhs_elements=rhs)


class Rule9Production(ConcreteProduction):
    @classmethod
    def instantiate(cls, n_words: int):
        name = f"Rule9_E_{n_words}_0"
        lhs = []
        rhs = "[]"
        return cls(name=name, lhs=lhs, rhs=rhs)


class RuleWProduction(CrtTerminalProduction):
    @classmethod
    def instantiate(cls, i: int, word: str, tokenizer, literal):
        name = f"Materialize_W{i}"

        terminal = TerminalItem(text=word, name=name)
        return cls.from_terminal(
            terminal=terminal, tokenizer=tokenizer, literal=literal
        )


class RuleFullPhraseLevelTagProduction(CrtTerminalProduction):
    @classmethod
    def instantiate(cls, tag: str, tokenizer, literal):
        name = f"Derive_FullPhraseLevelTag_{tag}".replace("-", "_")

        terminal = TerminalItem(text=tag, name=name)
        return cls.from_terminal(
            terminal=terminal, tokenizer=tokenizer, literal=literal
        )


class RuleWordLevelTagProduction(CrtTerminalProduction):
    @classmethod
    def instantiate(cls, tag: str, tokenizer, literal):
        name = f"Derive_WordLevelTag_{tag}".replace("-", "_").replace("$", "Dollar")

        terminal = TerminalItem(text=tag, name=name)
        return cls.from_terminal(
            terminal=terminal, tokenizer=tokenizer, literal=literal
        )
