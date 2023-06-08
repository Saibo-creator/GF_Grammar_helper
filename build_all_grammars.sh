
#

#########################
# Constituency Parsing
#########################


# input independent grammars
python build_grammar.py --task CP --grammar Ptb --compile

# input dependent grammars
python build_grammar.py --task CP --grammar Ptb --compile --dataset ptb --dep


#########################
# Entity Disambiguation
#########################

# input independent grammars
python build_grammar.py --task ED --grammar Minimal --KB kilt_wiki --compile

# input dependent grammars - Minimal
python build_grammar.py --task ED --grammar Minimal --compile  --dataset aida --dep
python build_grammar.py --task ED --grammar Minimal --compile  --dataset ace2004 --dep
python build_grammar.py --task ED --grammar Minimal --compile  --dataset aquaint --dep
python build_grammar.py --task ED --grammar Minimal --compile  --dataset clueweb --dep
python build_grammar.py --task ED --grammar Minimal --compile  --dataset msnbc --dep
python build_grammar.py --task ED --grammar Minimal --compile  --dataset wiki --dep
python build_grammar.py --task ED --grammar Minimal --compile  --dataset wikiLinksNED --dep

# input dependent grammars - sentence
python build_grammar.py --task ED --grammar sentence --compile  --dataset kilt_wiki --dep