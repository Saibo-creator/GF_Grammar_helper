
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
python build_grammar.py --task ED --grammar Minimal --KB kilt_wiki --compile --clean
python build_grammar.py --task ED --grammar Minimal --KB YAGO-KB --compile --clean

# input dependent grammars - Minimal
python build_grammar.py --task ED --grammar Minimal --compile  --dataset aida --dep --clean
python build_grammar.py --task ED --grammar Minimal --compile  --dataset ace2004 --dep --clean
python build_grammar.py --task ED --grammar Minimal --compile  --dataset aquaint --dep --clean
python build_grammar.py --task ED --grammar Minimal --compile  --dataset clueweb --dep --clean
python build_grammar.py --task ED --grammar Minimal --compile  --dataset msnbc --dep --clean
python build_grammar.py --task ED --grammar Minimal --compile  --dataset wiki --dep --clean
python build_grammar.py --task ED --grammar Minimal --compile  --dataset wikiLinksNED --dep --clean

######################### Canonical instruction #############################
python build_grammar.py --task ED --grammar Canonical --compile  --dataset aida --dep --clean
python build_grammar.py --task ED --grammar Canonical --compile  --dataset ace2004 --dep --clean
python build_grammar.py --task ED --grammar Canonical --compile  --dataset aquaint --dep --clean
python build_grammar.py --task ED --grammar Canonical --compile  --dataset clueweb --dep --clean
python build_grammar.py --task ED --grammar Canonical --compile  --dataset msnbc --dep --clean
python build_grammar.py --task ED --grammar Canonical --compile  --dataset wiki --dep --clean
python build_grammar.py --task ED --grammar Canonical --compile  --dataset wikiLinksNED --dep --clean



# input dependent grammars - sentence
python build_grammar.py --task ED --grammar sentence --compile  --dataset kilt_wiki --dep