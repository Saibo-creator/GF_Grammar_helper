# Grammar Module

We strongly recommend reading the [Lesson 2: Designing a grammar for complex phrases](https://www.grammaticalframework.org/doc/tutorial/gf-tutorial.html#toc16)
section of the GF tutorial before reading this section.

## Table of Contents

- [Grammar](#grammar-module)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Grammar](#grammar)
  - [AbstractGrammar](#abstractgrammar)
  - [ConcreteGrammar](#concretegrammar)

## Overview
As we have seen in the [Food Grammar](food_grammar.md) example, we have two types of grammars: `AbstractGrammar` and `ConcreteGrammar`.
The two grammars are used together to represent a formal grammar.

### Grammar

The abstract class `Grammar` is used to represent a formal grammar.
It is inherited by `AbstractGrammar` and `ConcreteGrammar`.

A `Grammar` object is instantiated with

`def __init__(
    self,
    name: str,
    start: str,
    productions: List[Production],
    categories: Optional[Set[str]] = None,
    flags=None,
    **kwargs,
):`

It can be saved to a `.gf` file using the `save_to_gf()` method.

It can also be read from a `.json` file using the `_from_json()` method.

### AbstractGrammar
The `AbstractGrammar` is used to represent the abstract syntax of a formal grammar.

It implements the four methods required by the `Grammar` class:
- `_get_grammar_header_str(self) -> str:` returns the string representation of the header of the grammar.
- `_get_grammar_flags_str(self) -> str:` returns the string representation of the flags of the grammar.
- `_get_grammar_categories_str(self) -> str:` returns the string representation of the categories of the grammar.
- `_get_grammar_productions_str(self) -> str:` returns the string representation of the productions of the grammar.


### ConcreteGrammar

The `ConcreteGrammar` is used to represent the concrete syntax of a formal grammar.

It also implements the four methods required by the `Grammar` class


### BiGrammar

The `BiGrammar` class is used to encapsulate a pair of `AbstractGrammar` and `ConcreteGrammar` objects.
