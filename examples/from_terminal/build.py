from src.GrammarBuild.grammar_builder import get_prod_name_for_ie
from src.grammar import CrtTerminalProduction, EntityTerminalItem
from src.new_utils import tokenize
from transformers import AutoTokenizer

from src.utils import get_hashed_name

if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained("saibo/llama-7B", use_fast=False)
    text = "Byera Village"
    tokenization = tokenize(tokenizer, text=text)

    terminal = EntityTerminalItem(entity=text)

    prod = CrtTerminalProduction.from_terminal(
        terminal=terminal, tokenizer=tokenizer, literal=False
    )
    print(prod)
