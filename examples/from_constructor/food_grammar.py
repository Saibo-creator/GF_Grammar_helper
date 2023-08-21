import os

from src.grammar import (
    AbstractGrammar,
    ConcreteGrammar,
)
from src.production import AbstractProduction, ConcreteProduction
from src.new_utils import LiteralStr

if __name__ == "__main__":
    abstract_grammar = AbstractGrammar(
        start="Comment",
        name="Foods",
        productions=[
            AbstractProduction(name="Pred", lhs=["Item", "Quantity"], rhs="Comment"),
            AbstractProduction(name="This", lhs=["Kind"], rhs="Item"),
            AbstractProduction(name="That", lhs=["Kind"], rhs="Item"),
            AbstractProduction(name="Mod", lhs=["Quantity", "Kind"], rhs="Kind"),
            AbstractProduction(name="Wine", lhs=[], rhs="Kind"),
            AbstractProduction(name="Cheese", lhs=[], rhs="Kind"),
            AbstractProduction(name="Fish", lhs=[], rhs="Kind"),
            AbstractProduction(name="Very", lhs=["Quantity"], rhs="Quantity"),
            AbstractProduction(name="Fresh", lhs=[], rhs="Quantity"),
            AbstractProduction(name="Warm", lhs=[], rhs="Quantity"),
            AbstractProduction(name="Italian", lhs=[], rhs="Quantity"),
            AbstractProduction(name="Expensive", lhs=[], rhs="Quantity"),
            AbstractProduction(name="Delicious", lhs=[], rhs="Quantity"),
            AbstractProduction(name="Boring", lhs=[], rhs="Quantity"),
        ],
    )

    print(abstract_grammar)
    abstract_grammar.save_to_gf("FoodExample")

    concrete_grammar = ConcreteGrammar(
        start="Comment",
        name="FoodEng",
        abstract_grammar_name="Foods",
        categories={"Item", "Quantity", "Kind", "Comment"},
        productions=[
            ConcreteProduction(
                name="Pred",
                lhs=["item", "quantity"],
                rhs_elements=["item", LiteralStr("is"), "quantity"],
            ),
            ConcreteProduction(
                name="This", lhs=["kind"], rhs_elements=[LiteralStr("this"), "kind"]
            ),
            ConcreteProduction(
                name="That", lhs=["kind"], rhs_elements=[LiteralStr("that"), "kind"]
            ),
            ConcreteProduction(
                name="Mod", lhs=["quantity", "kind"], rhs_elements=["quantity", "kind"]
            ),
            ConcreteProduction(name="Wine", lhs=[], rhs_elements=[LiteralStr("wine")]),
            ConcreteProduction(
                name="Cheese", lhs=[], rhs_elements=[LiteralStr("cheese")]
            ),
            ConcreteProduction(name="Fish", lhs=[], rhs_elements=[LiteralStr("fish")]),
            ConcreteProduction(
                name="Very",
                lhs=["quantity"],
                rhs_elements=[LiteralStr("very"), "quantity"],
            ),
            ConcreteProduction(
                name="Fresh", lhs=[], rhs_elements=[LiteralStr("fresh")]
            ),
            ConcreteProduction(name="Warm", lhs=[], rhs_elements=[LiteralStr("warm")]),
            ConcreteProduction(
                name="Italian", lhs=[], rhs_elements=[LiteralStr("Italian")]
            ),
            ConcreteProduction(
                name="Expensive", lhs=[], rhs_elements=[LiteralStr("expensive")]
            ),
            ConcreteProduction(
                name="Delicious", lhs=[], rhs_elements=[LiteralStr("delicious")]
            ),
            ConcreteProduction(
                name="Boring", lhs=[], rhs_elements=[LiteralStr("boring")]
            ),
        ],
    )

    print(concrete_grammar)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.join(dir_path, "output")

    abstract_grammar.save_to_gf(output_dir)
    concrete_grammar.save_to_gf(output_dir)
