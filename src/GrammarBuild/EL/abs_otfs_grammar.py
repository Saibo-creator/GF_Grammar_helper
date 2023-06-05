#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : abs_grammar.py
# @Date : 2023-03-24-15-22
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os
from typing import List, Union, Dict
from src.config.config import TEMPLATE_DIR

from src.GrammarBuild.base_grammar import Grammar, TemplateTokenGrammarBuilder
from .abs_grammar import ELAbsGrammarBuilder


class ELotfsAbsGrammarBuilder(ELAbsGrammarBuilder):

    template = os.path.join(TEMPLATE_DIR, "EL", "EL-OTF-sentence-AbsTemplate.hs")
    grammar_prefix = ""


    def __init__(self, tokenizer_or_path:str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)
