#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : trie2grammar.py
# @Date : 2023-03-17-17-19
# @Project: GF-LM
# @AUTHOR : Saibo Geng
# @Desc :

import transformers

if __name__ == '__main__':

    tokenizer = transformers.BartTokenizer.from_pretrained('martinjosifoski/genie-rw')

    with open("res/GF-grammars/GenieBart.gf", "r") as file:
        line_list = file.read().splitlines()
