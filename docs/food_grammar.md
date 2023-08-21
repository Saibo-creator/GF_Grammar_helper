# Food Grammar

We show how to use this library to generate a simplistic grammar for food comments.
The grammar is taken from the GF-book.

Check the example in `example/` folder.
- run `python food_grammar.py` to generate the grammar file `Food.gf` and `FoodEng.gf` in `FoodExample/` folder.
- run `gf` to start GF shell
- load the grammar file `FoodEng.gf` in GF shell via `import FoodExample/FoodEng.gf`, you should see the following output
```terminal
- compiling FoodExample/Foods.gf...   write file FoodExample/Foods.gfo
- compiling FoodExample/FoodEng.gf...   write file FoodExample/FoodEng.gfo
linking ... OK

Languages: FoodEng
```
- try autocomplete with this grammar file
```terminal
Foods> p "this
```
and press `Tab` key, you should see the following output
```terminal
Italian    boring     cheese     delicious  expensive  fish       fresh      very       warm       wine
```
