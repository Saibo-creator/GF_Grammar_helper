import os
from src.grammar import AbstractGrammar, ConcreteGrammar, AbstractProduction, ConcreteProduction, LiteralString

if __name__ == '__main__':
    # get directory of current file
    path_of_this_script = os.path.dirname(os.path.abspath(__file__))

    abs_gmr_file_path = os.path.join(path_of_this_script, "Food.json")
    crt_gmr_file_path = os.path.join(path_of_this_script, "FoodEng.json")


    # abstract_grammar = AbstractGrammar.from_json(abs_gmr_file_path)
    # print(abstract_grammar)
    concrete_grammar = ConcreteGrammar.from_json(crt_gmr_file_path)
    print(concrete_grammar)
