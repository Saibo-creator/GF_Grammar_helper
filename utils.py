#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : utils.py
# @Date : 2023-03-19-15-38
# @Project: GFLM
# @AUTHOR : Saibo Geng
# @Desc :

import string

def convert_punctuation_to_characters(text):
    # Define the punctuation marks to be replaced and their corresponding character names
    punctuation_to_characters = {
        '.': 'DOT',
        ',': 'COMMA',
        '?': 'QUESTION_MARK',
        '!': 'EXCLAMATION_MARK',
        ';': 'SEMICOLON',
        ':': 'COLON',
        "'": 'SINGLE_QUOTE',
        '"': 'DOUBLE_QUOTE',
        '(': 'OPEN_PARENTHESIS',
        ')': 'CLOSE_PARENTHESIS',
        '[': 'OPEN_BRACKET',
        ']': 'CLOSE_BRACKET',
        '{': 'OPEN_BRACE',
        '}': 'CLOSE_BRACE',
        '-': 'HYPHEN',
        # '_': 'UNDERSCORE',
        '+': 'PLUS',
        '=': 'EQUALS',
        '&': 'AMPERSAND',
        '%': 'PERCENT',
        '$': 'DOLLAR',
        '#': 'POUND',
        '@': 'AT',
        '*': 'ASTERISK',
        '^': 'CARET',
        '~': 'TILDE',
        '`': 'BACKTICK',
        '/': 'FORWARD_SLASH',
        '\\': 'BACKSLASH',
        '|': 'PIPE',
        '<': 'LESS_THAN',
        '>': 'GREATER_THAN',
    }

    # Create a translation table using str.maketrans()
    translation_table = str.maketrans(punctuation_to_characters)

    # Translate the text using the translation table
    translated_text = text.translate(translation_table)

    return translated_text

def replace_numbers_with_letters(input_string):
    """
    input_string = "I have 3 apples and 2 oranges"
    :param input_string:
    :return: "I have d apples and c oranges"
    """
    # Define the mapping of numbers to letters
    num_to_letter = {
        '0': 'a',
        '1': 'b',
        '2': 'c',
        '3': 'd',
        '4': 'e',
        '5': 'f',
        '6': 'g',
        '7': 'h',
        '8': 'i',
        '9': 'j',
    }

    # Create a translation table
    translation_table = str.maketrans(num_to_letter)

    # Replace numbers with letters using the translation table
    return input_string.translate(translation_table)

