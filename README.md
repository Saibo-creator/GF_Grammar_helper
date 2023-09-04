# GF GrammarHelper

This is a helper library to generate GF grammar files for NLP tasks.

This library
- Provides an abstraction of `Grammar` and `ProductionRule` to represent a GF grammar.
- Provides a `IE_grammar`, `ED_grammar` and `CP_grammar` three modules to generate GF grammar files for Information Extraction, Entity Disambiguation and Consituency Parsing tasks respectively.

## High level design

As shown in the [paper](https://arxiv.org/abs/2305.13971), one can use formal grammar to represent the language of a task.
Given a runtime that supports partial parsing, one can use the formal grammar to incrementally parse a sentence and get the next allowed tokens.

With this library, the task of using formal grammar to do constrained language generation is divided into two three steps:
- Step 1: Define the formal grammar for the task by creating a task-specific `Grammar` object(see `grammar.py`).
- Step 2: Save the `Grammar` object to a GF grammar file by calling `Grammar.save()`.
- Step 3: Use the GF runtime to compile the GF grammar file into `pgf` file
- Step 4: Use the python gf wrapper to load the `pgf` file and do constrained text generation.(see `xxx` repository for an example)



## Requirements

```
export PYTHONPATH=/path/to/my_project:$PYTHONPATH # this is required to run scripts in `example/` folder
export PYTHONPATH=/Users/saibo/Research/Projects/GCD/GF_editor:$PYTHONPATH # this is required to run scripts in `example/` folder
```

## Installation

```
pip install -r requirements.txt
```

## Reproduce the grammars needed for the paper

```
bash reproduce_all_grammars_for_gcd.sh
```

The generated grammars are saved in `output/grammars/gf/` and `output/grammars/pgf/` folders.
The `gf` files are the source files of the grammars, and the `pgf` files are the compiled files of the grammars.
Only the `pgf` files are directly used by the GF runtime for constrained text generation.

## Docs

- [Intro: Food Grammar](docs/food_grammar.md)
- [Grammar](docs/grammar.md)
- [Grammar Factory](docs/grammar_factory.md)
- [Grammar Examples](docs/example_grammar.md)
- [Examples](docs/examples.md)
- [Add new task](docs/add_new_task.md)
- [Benchmark](docs/benchmark.md)
