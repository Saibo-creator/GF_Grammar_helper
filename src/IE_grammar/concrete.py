import json
from typing import Dict, List

from src.grammar import TerminalItem
from src.GrammarBuild.grammar_builder import get_prod_name_for_ie
from src.new_utils import tokenize
from src.utils import get_hashed_name
from transformers import AutoTokenizer


def _get_production_rule_for_entity(entity: str) -> str:
    production_name = get_prod_name_for_ie(entity=entity)
    tokenization = tokenize(tokenizer, text=text)

    prod = TokenizationProduction._from_tokenization(
        tokenization=tokenization, literal=False, name=production_name
    )
    return f"Ent_{entity_id}: Entity"
