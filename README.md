# GF GrammarHelper

GF GrammarHelper is a library designed to facilitate the generation of Grammatical Framework (GF) grammar files tailored for various NLP tasks.

Before diving into the library, we highly recommend familiarizing yourself with the basics of GF by reading the [Grammatical Framework Tutorial](https://www.grammaticalframework.org/doc/tutorial/gf-tutorial.html) first to get a basic understanding of GF.

To reproduce the grammars used in the paper, please refer to the [Reproduce the grammars needed for the paper](#reproduce-the-grammars-needed-for-the-paper) section.

## Overview

Incorporating the insights presented in this [paper](https://arxiv.org/abs/2305.13971), formal grammar can be employed to represent a task-specific language.
Leveraging a [runtime](https://www.grammaticalframework.org/doc/runtime-api.html#haskell) that supports partial parsing, this formal grammar can incrementally parse sentences, guiding the production of the subsequent permissible tokens.

Using the GF GrammarHelper library, the process of employing formal grammar for constrained language generation is delineated into four steps:

- **Grammar Definition**: Initiate the task-specific formal grammar by constructing a `Grammar` object (refer to `src/grammar.py`).
- **Grammar File Creation**: Store the Grammar object into a GF grammar file(`.gf`) using the `Grammar.save()` method.
- **Compilation**: Utilize the GF runtime to transform the GF grammar file into a `.pgf` file.
- **Constrained Text Generation**: Rely on the Python GF wrapper to load the `.pgf` file and execute constrained text generation. For a practical demonstration, see the xxx repository.

## Features:

- Offers a abstraction of `Grammar` and `ProductionRule` to encapsulate a GF grammar.
- Introduces three specialized modules: `IE_grammar`, `ED_grammar`, and `CP_grammar`. These are dedicated to generating GF grammar files for Information Extraction, Entity Disambiguation, and Constituency Parsing tasks, respectively.
- Provides a `GrammarFactory` class to facilitate the creation of `Grammar` objects in batch.


## Requirements


```shell
pip install -r requirements.txt
```

Add the root folder of this repository to `PYTHONPATH` environment variable.
```shell
# in the root folder of this repository
export PYTHONPATH="$(pwd):$PYTHONPATH"  # this is required to run scripts in `example/` folder
```


## Reproduce the grammars needed for the paper

```shell
bash generate_gcd_grammars.sh
```

The generated grammars are saved in `output/grammars/gf/` and `output/grammars/pgf/` folders.
The `gf` files are the source files of the grammars, and the `pgf` files are the compiled files of the grammars.
Only the `pgf` files are directly used by the GF runtime for constrained text generation.

## Docs

- [Intro: Food Grammar](docs/food_grammar.md)
- [Grammar](docs/grammar.md)
- [Grammar Factory](docs/grammar_factory.md)
- [Examples](docs/examples.md)
- [Add new task](docs/add_new_task.md)
- [Constrained Decoding](docs/constrained_decoding.md)
- [Benchmark(outdated)](docs/benchmark.md)
