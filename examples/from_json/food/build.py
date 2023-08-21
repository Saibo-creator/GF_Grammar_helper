import os

from src.grammar import AbstractGrammar, ConcreteGrammar

if __name__ == "__main__":
    # get directory of current file
    dir_of_this_script = os.path.dirname(os.path.abspath(__file__))

    abs_gmr_file_path = os.path.join(dir_of_this_script, "Food.json")
    crt_gmr_file_path = os.path.join(dir_of_this_script, "FoodEng.json")

    output_dir = os.path.join(dir_of_this_script, "output")

    abstract_grammar = AbstractGrammar.from_json(abs_gmr_file_path)
    print(abstract_grammar)

    abstract_grammar.save_to_gf(output_dir)

    concrete_grammar = ConcreteGrammar.from_json(crt_gmr_file_path)
    print(concrete_grammar)

    concrete_grammar.save_to_gf(output_dir)
