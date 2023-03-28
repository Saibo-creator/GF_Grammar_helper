#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : config.py
# @Date : 2023-03-25-14-44
# @Project: GFLM
# @AUTHOR : Saibo Geng
# @Desc :

import os

# Get the absolute path of the directory containing the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Set the ROOT_DIR variable to the parent directory of the script directory
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))

# Set the resource directory
RES_DIR = os.path.join(ROOT_DIR, "res")

# Set the asset directory
ASSET_DIR = os.path.join(ROOT_DIR, "asset")

# Set the gf directory
ASSET_GF_DIR = os.path.join(ASSET_DIR, "GF-grammars", "gf")

#AUTO GENERATED
AUTO_GEN_GF_DIR = os.path.join(ASSET_GF_DIR, "autogen")

# Set the gf directory
ASSET_PGF_DIR = os.path.join(ASSET_DIR, "GF-grammars", "pgf")

# Set the templates directory
TEMPLATE_DIR = os.path.join(RES_DIR, "GF-grammars", "templates")