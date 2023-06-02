#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : abs_grammar.py
# @Date : 2023-03-24-15-22
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os
import pdb
from abc import ABC, abstractmethod
from typing import List, Union

from tqdm import tqdm

from src.config.config import TEMPLATE_DIR

from transformers import AutoTokenizer

from src.GrammarBuild.base_grammar import Grammar, TemplateTokenGrammarBuilder
from .crt_grammar import ELCrtGrammarBuilder


class ELotfCrtGrammarBuilder(ELCrtGrammarBuilder, ABC):

    template = os.path.join(TEMPLATE_DIR, "EL", "EL-OTF-sentence-CrtTemplate.hs")
    grammar_prefix = ""


    Open_bracket_marker = "["
    Close_bracket_marker = "]"
    StartMarker = "[START_ENT]"
    EndMarker = "[END_ENT]"

    Default_BOS_marker = "0"

    def __init__(self, tokenizer_or_path:str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)

    def build(self, base_grammar_name: str, entities_or_path: Union[List[str], str], crt_grammar_name=None, literal=False, mention:str=None) -> Grammar:
        assert mention is not None, "mention should not be None"
        grammar: str = self.read_template()
        abs_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name)
        if crt_grammar_name is None:
            crt_grammar_name = self.get_grammar_name(base_grammar_name=base_grammar_name, crt=True)
        entities = self.read_jsonl(entities_or_path) if isinstance(entities_or_path, str) else entities_or_path
        TODO
        formatted_grammar_plain_text: str = grammar.format(abs_grammar_name=abs_grammar_name, crt_grammar_name=crt_grammar_name,
                                                           bog_tokens="[]",  #self.get_entity_tokens(tokenizer.bos_token, tokenizer, literal, rm_eos=True,rm_bos=False)
                                                           eog_tokens= f'"{self.tokenizer.encode(self.tokenizer.eos_token, add_special_tokens=False)[0]}"',  # "2" for llama and "1" for T5
                                                           mention_tokens= self.get_entity_tokens(entity=mention,  rm_eos=True),
                                                           open_bracket_tokens = self.get_entity_tokens(self.Open_bracket_marker,  rm_eos=True),
                                                           close_bracket_tokens = self.get_entity_tokens(self.Close_bracket_marker,  rm_eos=True),
                                                            LeftContext_tokens=self.get_entity_tokens(entity=left_context,  rm_eos=True),
                                                            RightContext_tokens=self.get_entity_tokens(entity=right_context,  rm_eos=True),
                                                            StartMarker_tokens=self.get_entity_tokens(entity=self.StartMarker,  rm_eos=True),
                                                            EndMarker_tokens=self.get_entity_tokens(entity=self.EndMarker,  rm_eos=True),
                                                           Materialize_Entities=self.batch_get_decoding_linearization_rules(entities=entities,  rm_eos=True, rm_bos=True))
        return Grammar(formatted_grammar_plain_text, name=crt_grammar_name)





