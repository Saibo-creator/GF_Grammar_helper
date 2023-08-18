from src.grammar import AbstractGrammar, ConcreteGrammar, AbstractProduction, ConcreteProduction, LiteralString

if __name__ == '__main__':
    abstract_grammar = AbstractGrammar(
        start="Comment",
        name="Foods",
        productions=[
            AbstractProduction(
                name="Pred",
                lhs= ["Item", "Quantity"],
                rhs= "Comment"
            ),
            AbstractProduction(
                name="This",
                lhs= ["Kind"],
                rhs= "Item"
            ),
            AbstractProduction(
                name="That",
                lhs= ["Kind"],
                rhs= "Item"
            ),
            AbstractProduction(
                name="Mod",
                lhs= ["Quantity", "Kind"],
                rhs= "Kind"
            ),
            AbstractProduction(
                name="Wine",
                lhs= [],
                rhs= "Kind"
            ),
            AbstractProduction(
                name="Cheese",
                lhs= [],
                rhs= "Kind"
            ),
            AbstractProduction(
                name="Fish",
                lhs= [],
                rhs= "Kind"
            ),
            AbstractProduction(
                name="Very",
                lhs= ["Quantity"],
                rhs= "Quantity"
            ),
            AbstractProduction(
                name="Fresh",
                lhs= [],
                rhs= "Quantity"
            ),
            AbstractProduction(
                name="Warm",
                lhs= [],
                rhs= "Quantity"
            ),
            AbstractProduction(
                name="Italian",
                lhs= [],
                rhs= "Quantity"
            ),
            AbstractProduction(
                name="Expensive",
                lhs= [],
                rhs= "Quantity"
            ),
            AbstractProduction(
                name="Delicious",
                lhs= [],
                rhs= "Quantity"
            ),
            AbstractProduction(
                name="Boring",
                lhs= [],
                rhs= "Quantity"
            )
        ]
    )

    print(abstract_grammar)
    abstract_grammar.save("FoodExample")

    concrete_grammar = ConcreteGrammar(
        start="Comment",
        name="FoodEng",
        abstract_grammar_name="Foods",
        categories={"Item", "Quantity", "Kind", "Comment"},
        productions=[
            ConcreteProduction(
                name="Pred",
                lhs= ["item", "quantity"],
                rhs= ["item", LiteralString("is"), "quantity"]
            ),
            ConcreteProduction(
                name="This",
                lhs= ["kind"],
                rhs= [LiteralString("this"), "kind"]
            ),
            ConcreteProduction(
                name="That",
                lhs= ["kind"],
                rhs= [LiteralString("that"), "kind"]
            ),
            ConcreteProduction(
                name="Mod",
                lhs= ["quantity", "kind"],
                rhs= ["quantity", "kind"]
            ),
            ConcreteProduction(
                name="Wine",
                lhs= [],
                rhs= [LiteralString("wine")]
            ),
            ConcreteProduction(
                name="Cheese",
                lhs= [],
                rhs= [LiteralString("cheese")]
            ),
            ConcreteProduction(
                name="Fish",
                lhs= [],
                rhs= [LiteralString("fish")]
            ),
            ConcreteProduction(
                name="Very",
                lhs= ["quantity"],
                rhs= [LiteralString("very"), "quantity"]
            ),
            ConcreteProduction(
                name="Fresh",
                lhs= [],
                rhs= [LiteralString("fresh")]
            ),
            ConcreteProduction(
                name="Warm",
                lhs= [],
                rhs= [LiteralString("warm")]
            ),
            ConcreteProduction(
                name="Italian",
                lhs= [],
                rhs= [LiteralString("Italian")]
            ),
            ConcreteProduction(
                name="Expensive",
                lhs= [],
                rhs= [LiteralString("expensive")]
            ),
            ConcreteProduction(
                name="Delicious",
                lhs= [],
                rhs= [LiteralString("delicious")]
            ),
            ConcreteProduction(
                name="Boring",
                lhs= [],
                rhs= [LiteralString("boring")]
            )
        ]
    )

    print(concrete_grammar)
    concrete_grammar.save("FoodExample")









