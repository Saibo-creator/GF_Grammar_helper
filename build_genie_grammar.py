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
    parser.add_argument("--constrained-world", type=str, default="wiki_ner", help="constrained_world name", choices=["wiki_ner", "rebel", "rebel_medium"])
    parser.add_argument("--linearization-class-id", type=str, default="fully_expanded", choices=["fully_expanded", "subject_collapsed"])
    parser.add_argument("--tokenizer-path", type=str, default="/dlabdata1/llama_hf/7B", help="martinjosifoski/genie-rw, /dlabdata1/llama_hf/7B, t5-small")
    parser.add_argument("--grammar-name", type=str, default="auto", help="name of the grammar") # genie_llama_fully_expanded
    parser.add_argument("--compile", action="store_true", help="whether to compile the grammar")
    parser.add_argument("--debug", action="store_true", help="whether to use debug mode, which will generate a small grammar from list of entities and relations")
    parser.add_argument("--literal", action="store_true", help="whether to use literal grammar")
    args = parser.parse_args()


    if args.grammar_name == "auto":
        grammar_name="genie"
        if "llama" in args.tokenizer_path:
            grammar_name += "_llama"
        elif "t5" in args.tokenizer_path:
            grammar_name += "_t5"
        else:
            raise NotImplementedError(f"tokenizer_path {args.tokenizer_path} not implemented")

        grammar_name += f"_{args.linearization_class_id}"

        if args.constrained_world == "wiki_ner":
            grammar_name += "_wiki_ner"
        elif args.constrained_world == "rebel":
            grammar_name += "_rebel"
        elif args.constrained_world == "rebel_medium":
            grammar_name += "_rebel_medium"
        else:
            raise NotImplementedError(f"constrained_world {args.constrained_world} not implemented")
        if args.debug:
            grammar_name = "debug"
    else:
        grammar_name = args.grammar_name

    if args.linearization_class_id == "fully_expanded":
        submodule_name = "FullyExpanded"
    elif args.linearization_class_id == "subject_collapsed":
        submodule_name = "SubjectCollapsed"
    else:
        raise NotImplementedError(f"linearization_class_id {args.linearization_class_id} not implemented")

    #dynamic import based on linearization_class_id
    GenieAbsGrammarBuilderModule = __import__(f"src.GrammarBuild.v2", fromlist=[f"Genie{submodule_name}AbsGrammarBuilder"])
    GenieCrtGrammarBuilderModule = __import__(f"src.GrammarBuild.v2", fromlist=[f"Genie{submodule_name}CrtGrammarBuilder"])

    GenieAbsGrammarBuilder = getattr(GenieAbsGrammarBuilderModule, f"Genie{submodule_name}AbsGrammarBuilder")
    GenieCrtGrammarBuilder = getattr(GenieCrtGrammarBuilderModule, f"Genie{submodule_name}CrtGrammarBuilder")

    abs_builder = GenieAbsGrammarBuilder()
    crt_builder = GenieCrtGrammarBuilder()

    output_dir = os.path.join(GF_AUTO_GEN_GF_DIR, f"v2")

    if args.debug:
        abs_grammar = abs_builder.build(base_grammar_name=grammar_name, entities_or_path=["entity1", "entity2"], relations_or_path=["relation1", "relation2"], tokenizer_or_path=args.tokenizer_path)
        crt_grammar = crt_builder.build(base_grammar_name=grammar_name, entities_or_path=["entity1", "entity2"], relations_or_path =["relation1", "relation2"], tokenizer_or_path=args.tokenizer_path)

    else:

        entities_path = TRAINING_DATA_PATH[args.constrained_world]["entity"]
        relations_path = TRAINING_DATA_PATH[args.constrained_world]["relation"]
        print("start building abstract grammar...")
        abs_grammar = abs_builder.build(base_grammar_name=grammar_name, entities_or_path=entities_path, relations_or_path=relations_path, tokenizer_or_path=args.tokenizer_path)
        print("finished building abstract grammar...")
        print("start building concrete grammar...")
        crt_grammar = crt_builder.build(base_grammar_name=grammar_name, entities_or_path=entities_path, relations_or_path=relations_path, tokenizer_or_path=args.tokenizer_path, literal=args.literal)
        print("finished building concrete grammar...")


    grammar_pair = AbsCrtGrammarPair(abs_grammar=abs_grammar, crt_grammar=crt_grammar)
    grammar_pair.save(output_dir=output_dir, compile=args.compile)
