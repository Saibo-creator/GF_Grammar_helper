
#

#########################
# Constituency Parsing
#########################


# input independent grammars
#python build_grammar.py --task CP --grammar Ptb --compile # not supported anymore

# input dependent grammars
#python build_task_grammar.py --task CP --grammar_type re --dataset ptb --compile --clean


#########################
# Entity Disambiguation
#########################

# input independent grammars
# TODO

# input dependent grammars - Minimal
#python build_task_grammar.py --task ED --grammar_type minimal --dataset aida --compile --clean
#python build_task_grammar.py --task ED --grammar_type minimal --dataset ace2004 --compile --clean
#python build_task_grammar.py --task ED --grammar_type minimal --dataset aquaint --compile --clean
#python build_task_grammar.py --task ED --grammar_type minimal --dataset clueweb --compile --clean
#python build_task_grammar.py --task ED --grammar_type minimal --dataset msnbc --compile --clean
#python build_task_grammar.py --task ED --grammar_type minimal --dataset wiki --compile --clean
#python build_task_grammar.py --task ED --grammar_type minimal --dataset wikiLinksNED --compile --clean


######################### Canonical instruction #############################
python build_grammar_by_factory.py --task ED --grammar_type canonical --dataset aida --compile --clean
python build_grammar_by_factory.py --task ED --grammar_type canonical --dataset ace2004 --compile --clean
python build_grammar_by_factory.py --task ED --grammar_type canonical --dataset aquaint --compile --clean
python build_grammar_by_factory.py --task ED --grammar_type canonical --dataset clueweb --compile --clean
python build_grammar_by_factory.py --task ED --grammar_type canonical --dataset msnbc --compile --clean
python build_grammar_by_factory.py --task ED --grammar_type canonical --dataset wiki --compile --clean
#python build_task_grammar.py --task ED --grammar_type canonical --dataset wikiLinksNED --compile --clean


#########################
# Information Extraction
#########################

#python build_task_grammar.py --task IE --grammar_type fe --dataset wikinre --compile --clean
