#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : indep_abs_grammar.py
# @Date : 2023-03-24-15-22
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os
from src.config.config import TEMPLATE_DIR

from src.GrammarBuild.ED.indep.indep_abs_grammar import ED_IndepMinimalAbsGrammarBuilder


class ED_DepMinimalAbsGrammarBuilder(ED_IndepMinimalAbsGrammarBuilder):

    template = os.path.join(TEMPLATE_DIR, "ED", "Dep", "minimal", "ED-Dep-Minimal-AbsTemplate.hs")
    grammar_prefix = ""


    def __init__(self, tokenizer_or_path:str, literal=False):
        super().__init__(tokenizer_or_path=tokenizer_or_path, literal=literal)

