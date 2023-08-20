from src.GrammarBuild.grammar_builder import get_prod_name_for_ie
from src.grammar import CrtTerminalProduction
from src.new_utils import tokenize
from transformers import AutoTokenizer

from src.utils import get_hashed_name

if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained("saibo/llama-7B", use_fast=False)
    text = "Byera Village"
    tokenization = tokenize(tokenizer, text=text)

    _production_name = get_prod_name_for_ie(entity=text)
    prod = CrtTerminalProduction._from_tokenization(
        tokenization=tokenization, literal=False, name=_production_name
    )
    print(prod)
