# Grammar Factory

`GrammarFactory` is a class that helps to generate GF grammar files for NLP tasks.

The repo contains three `subclasses` of `GrammarFactory`:
- `IEGrammarFactory` for Information Extraction tasks
- `EDGrammarFactory` for Entity Disambiguation tasks
- `CPGrammarFactory` for Constituency Parsing tasks


## Main Methods

- `GrammarFactory.build_bigrammar(data_point)`: build a bigrammar for a single data point
- `GrammarFactory.build_bigrammars(dataset)`: build bigrammars for the whole dataset(one bigrammar for each data point)
