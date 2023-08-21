from src.grammar import AbstractGrammar, ConcreteGrammar


class BiGrammar:
    def __init__(self, abs_grammar: AbstractGrammar, crt_grammar: ConcreteGrammar):
        self.abs_grammar = abs_grammar
        self.crt_grammar = crt_grammar
        self._validate()

    def _validate(self):
        assert (
            self.abs_grammar.name == self.crt_grammar.abstract_grammar_name
        ), f"Abstract grammar name {self.abs_grammar.name} does not match concrete grammar name {self.crt_grammar.abstract_grammar_name}"

    def save_to_gf(self, output_dir):
        self.abs_grammar.save_to_gf(output_dir)
        self.crt_grammar.save_to_gf(output_dir)
