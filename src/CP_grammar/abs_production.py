from src.production import AbstractProduction


class Rule1Production(AbstractProduction):
    @classmethod
    def instantiate(cls, i: int, j: int):
        name = f"Rule1_B_{i}_{j}"
        lhs = ["Left", "FullPhraseLevelTag", f"B_{i}_{j + 1}"]
        rhs = f"B_{i}_{j}"
        return cls(name=name, lhs=lhs, rhs=rhs)


class Rule2Production(AbstractProduction):
    @classmethod
    def instantiate(cls, i: int, j: int):
        name = f"Rule2_B_{i}_{j}"
        lhs = ["Left", "WordLevelTag", f"C_{i}_{j + 1}"]
        rhs = f"B_{i}_{j}"
        return cls(name=name, lhs=lhs, rhs=rhs)


class Rule4Production(AbstractProduction):
    @classmethod
    def instantiate(cls, i: int, j: int):
        name = f"Rule4_C_{i}_{j}"
        lhs = [f"W{i}", f"E_{i + 1}_{j}"]
        rhs = f"C_{i}_{j}"
        return cls(name=name, lhs=lhs, rhs=rhs)


class Rule5Production(AbstractProduction):
    @classmethod
    def instantiate(cls, i: int, n_words: int):
        name = f"Rule5_C_{n_words}_{i}"
        lhs = [f"E_{n_words}_{i}"]
        rhs = f"C_{n_words}_{i}"

        return cls(name=name, lhs=lhs, rhs=rhs)


class Rule6Production(AbstractProduction):
    @classmethod
    def instantiate(cls, i: int, j: int):
        name = f"Rule6_E_{i}_{j}"
        lhs = [f"Right", f"E_{i}_{j - 1}"]
        rhs = f"E_{i}_{j}"
        return cls(name=name, lhs=lhs, rhs=rhs)


class Rule7Production(AbstractProduction):
    @classmethod
    def instantiate(cls, i: int, j: int):
        name = f"Rule7_E_{i}_{j}"
        lhs = [f"Right", f"B_{i}_{j - 1}"]
        rhs = f"E_{i}_{j}"
        return cls(name=name, lhs=lhs, rhs=rhs)


class Rule8Production(AbstractProduction):
    @classmethod
    def instantiate(cls, i: int, n_words: int):
        name = f"Rule8_E_{n_words}_{i}"
        lhs = [f"Right", f"E_{n_words}_{i - 1}"]
        rhs = f"E_{n_words}_{i}"
        return cls(name=name, lhs=lhs, rhs=rhs)


class Rule9Production(AbstractProduction):
    @classmethod
    def instantiate(cls, n_words: int):
        name = f"Rule9_E_{n_words}_0"
        lhs = []
        rhs = f"E_{n_words}_0"
        return cls(name=name, lhs=lhs, rhs=rhs)


class RuleWProduction(AbstractProduction):
    @classmethod
    def instantiate(cls, i: int):
        name = f"Materialize_W{i}"
        lhs = []
        rhs = f"W{i}"
        return cls(name=name, lhs=lhs, rhs=rhs)


class RuleFullPhraseLevelTagProduction(AbstractProduction):
    @classmethod
    def instantiate(cls, tag: str):
        tag = tag.replace("-", "_")
        name = f"Derive_FullPhraseLevelTag_{tag}"
        lhs = []
        rhs = f"FullPhraseLevelTag"
        return cls(name=name, lhs=lhs, rhs=rhs)


class RuleWordLevelTagProduction(AbstractProduction):
    @classmethod
    def instantiate(cls, tag: str):
        # we need to replace - and $ because they are not allowed in variable names
        tag = tag.replace("-", "_").replace("$", "Dollar")
        name = f"Derive_WordLevelTag_{tag}"
        lhs = []
        rhs = f"WordLevelTag"
        return cls(name=name, lhs=lhs, rhs=rhs)
