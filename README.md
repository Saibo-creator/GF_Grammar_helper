# GFLM

TODO:
- measure speed between trie and GF



## Commands

### Compile Grammar

- compile grammar `python -m src.grammar.compile --grammar_path data/grammars/GenieWiki.gf --output_path data/grammars/GenieWiki.pgf`

### Benchmark

- run time complexity benchmark `python -m src.benchmark.time_complexity --num_repeat 5 --max_seq_len 128 --pgf FullyExpandedGenieWiki`
- plot benchmark result `python -m src.benchmark.visualization`

