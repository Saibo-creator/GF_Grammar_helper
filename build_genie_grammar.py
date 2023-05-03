#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Filename : test_gen_abs_grmr
# @Date : 2023-03-25-13-28
# @Project: GF-Grammar-Factory
# @AUTHOR : Saibo Geng
# @Desc :
import os

from src.config.config import GF_AUTO_GEN_GF_DIR,RES_DIR,TRAINING_DATA_PATH
from src.GrammarBuild.base_grammar import AbsCrtGrammarPair


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="wiki-ner", help="dataset name", choices=["wiki-ner", "rebel", "rebel-medium"])
    parser.add_argument("--format", type=str, default="FullyExpanded", choices=["FullyExpanded", "FullyExpandedEt",
                            "SubjectCollapsed"])
    parser.add_argument("--grammar-name", type=str, default=None, help="name of the grammar")
    parser.add_argument("--grammar-version", type=int, default=2, help="version of the grammar")
    parser.add_argument("--compile", action="store_true", help="whether to compile the grammar")
    parser.add_argument("--debug", action="store_true", help="whether to use debug mode, which will generate a small grammar from list of entities and relations")
    parser.add_argument("--literal", action="store_true", help="whether to use literal grammar")
    args = parser.parse_args()


    version=args.grammar_version

    if args.grammar_name is None:
        if args.dataset == "wiki-ner":
            grammar_name = "GenieWiki"
        elif args.dataset == "rebel":
            grammar_name = "GenieRebel"
        elif args.dataset == "rebel-medium":
            grammar_name = "GenieRebelMedium"
        else:
            raise NotImplementedError(f"dataset {args.dataset} not implemented")
        if args.debug:
            grammar_name = "debug"
    else:
        grammar_name = args.grammar_name

    # #dynamic import based on version
    # GenieAbsGrammarBuilder = __import__(f"src.GrammarBuild.v{version}.abs_grammar",
    #                                     fromlist=["GenieAbsGrammarBuilder"]).GenieAbsGrammarBuilder
    # GenieCrtGrammarBuilder = __import__(f"src.GrammarBuild.v{version}.crt_grammar",
    #                                     fromlist=["GenieCrtGrammarBuilder"]).GenieCrtGrammarBuilder

    #dynamic import based on format
    GenieAbsGrammarBuilderModule = __import__(f"src.GrammarBuild.v2", fromlist=[f"Genie{args.format}AbsGrammarBuilder"])
    GenieCrtGrammarBuilderModule = __import__(f"src.GrammarBuild.v2", fromlist=[f"Genie{args.format}CrtGrammarBuilder"])

    GenieAbsGrammarBuilder = getattr(GenieAbsGrammarBuilderModule, f"Genie{args.format}AbsGrammarBuilder")
    GenieCrtGrammarBuilder = getattr(GenieCrtGrammarBuilderModule, f"Genie{args.format}CrtGrammarBuilder")

    abs_builder = GenieAbsGrammarBuilder()
    crt_builder = GenieCrtGrammarBuilder()

    output_dir = os.path.join(GF_AUTO_GEN_GF_DIR, f"v{version}")

    if args.debug:
        abs_grammar = abs_builder.build(base_grammar_name=grammar_name, entities_or_path=["entity1", "entity2"], relations_or_path=["relation1", "relation2"], tokenizer_or_path="martinjosifoski/genie-rw")
        crt_grammar = crt_builder.build(base_grammar_name=grammar_name, entities_or_path=["entity1", "entity2"], relations_or_path =["relation1", "relation2"], tokenizer_or_path="martinjosifoski/genie-rw")

    else:

        entities_path = TRAINING_DATA_PATH[args.dataset]["entity"]
        relations_path = TRAINING_DATA_PATH[args.dataset]["relation"]
        abs_grammar = abs_builder.build(base_grammar_name=grammar_name, entities_or_path=entities_path, relations_or_path=relations_path, tokenizer_or_path="martinjosifoski/genie-rw")
        crt_grammar = crt_builder.build(base_grammar_name=grammar_name, entities_or_path=entities_path, relations_or_path=relations_path, tokenizer_or_path="martinjosifoski/genie-rw", literal=args.literal)


    grammar_pair = AbsCrtGrammarPair(abs_grammar=abs_grammar, crt_grammar=crt_grammar)
    grammar_pair.save(output_dir=output_dir, compile=args.compile)
