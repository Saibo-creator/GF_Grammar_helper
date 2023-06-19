concrete {crt_grammar_name} of {abs_grammar_name} = {{
  lincat
    StartTree , Trees , Tree , SentenceTag , Left , Right , FullPhraseLevelTag , PhraseLevelTag , HyphenFunctionTags , HyphenFunctionTag , HyphenNumTag , Hyphen , FunctionTag , WordTag , Num , Input_word , BOG , EOG , OpenBracket , CloseBracket = Str;
    --Text , BOG , EOG , Entity = Str;--
  lin

    --Derive_StartTree: Left -> SentenceTag -> Trees -> Right -> StartTree;--
    Derive_StartTree a b c d e f g h = a ++ b ++ c ++ d ++ e ++ f ++ g ++ h;

    Materialise_BOG = {bog_tokens};
    Materialise_EOG = {eog_tokens};
    Materialise_OpenBracket = {open_bracket_tokens};
    Materialise_CloseBracket = {close_bracket_tokens};

    -- Repeat:  Tree -> Trees -> Trees ; --
    Repeat a b = a ++ " " ++ b; -- (VP (VBN based) (PP-LOC-CLR (IN in) (NP (NNP New) (NNP York))--

    --Derive_Tree:  Left -> FullPhraseLevelTag -> Trees -> Right -> Tree;--
    Derive_Tree a b c d = a ++ b ++ " " ++ c ++ d; -- (NP-SBJ (NNP General) (NNP Motors) (NNP Corp.)) --


    --Derive_Trees:  Left -> FullPhraseLevelTag -> Trees -> Right -> Trees;--
    Derive_Trees a b c d = a ++ b ++ " " ++ c ++ d; -- (NP-SBJ (NNP General) (NNP Motors) (NNP Corp.)) --


    --Degenerate_Tree: Left -> WordTag -> Input_word -> Right -> Tree;--
    Degenerate_Tree a b c d = a ++ b ++ " " ++ c ++ d; -- (NNP Ford)--

    Degenerate_Trees: Left -> WordTag -> Input_word -> Right -> Trees;
    Degenerate_Trees a b c d = a ++ b ++ " " ++ c ++ d; -- (NNP Ford)--

    --Derive_FullTag: PhraseLevelTag -> HyphenFunctionTags -> HyphenNumTag -> FullPhraseLevelTag;--
    Derive_FullPhraseLevelTag a b c = a ++ b ++ c; -- NP-SBJ-3 --

    --Derive_HyphenFunctionTags: HyphenFunctionTag -> HyphenFunctionTags -> HyphenFunctionTags;--
    Derive_HyphenFunctionTags a b = a ++ b; -- -SBJ --

    --Empty_HyphenFunctionTags: HyphenFunctionTags;--
    Empty_HyphenFunctionTags = ""; -- --

    --Derive_HyphenNumTag: Hyphen -> Num -> HyphenNumTag;--
    Derive_HyphenNumTag a b = a ++ b; -- -3 --

    --Empty_HyphenNumTag: HyphenNumTag;--
    Empty_HyphenNumTag = ""; -- --


    --Derive_HyphenFunctionTag: Hyphen -> FunctionTag -> HyphenFunctionTag;--
    Derive_HyphenFunctionTag a b = a ++ b; -- -SBJ --

    --Empty_HyphenFunctionTag: HyphenFunctionTag;--
    Empty_HyphenFunctionTag = ""; -- --

    --Materialize_Hyphen: Hyphen;--
    Materialize_Hyphen = "-"; -- -

    --Materialize_SentenceTag: SentenceTag;--
    Materialize_SentenceTag = "S"; -- --

    --Materialize_Left: Left;--
    Materialize_Left = "(";

    --Materialize_Right: Right;--
    Materialize_Right = ")";

    -- the following should be automatically generated --
    Derive_PhraseLevelTag_S = {S}; -- "S" --
    Derive_PhraseLevelTag_SBAR = {SBAR}; -- "SBAR" --
    Derive_PhraseLevelTag_SBARQ = {SBARQ}; -- "SBARQ" --
    Derive_PhraseLevelTag_SINV = {SINV}; -- "SINV" --
    Derive_PhraseLevelTag_SQ = {SQ}; -- "SQ" --
    Derive_PhraseLevelTag_ADJP = {ADJP}; -- "ADJP" --
    Derive_PhraseLevelTag_ADVP = {ADVP}; -- "ADVP" --
    Derive_PhraseLevelTag_CONJP = {CONJP}; -- "CONJP" --
    Derive_PhraseLevelTag_FRAG = {FRAG}; -- "FRAG" --
    Derive_PhraseLevelTag_INTJ = {INTJ}; -- "INTJ" --
    Derive_PhraseLevelTag_LST = {LST}; -- "LST" --
    Derive_PhraseLevelTag_NAC = {NAC}; -- "NAC" --
    Derive_PhraseLevelTag_NP = {NP}; -- "NP" --
    Derive_PhraseLevelTag_NX = {NX}; -- "NX" --
    Derive_PhraseLevelTag_PP = {PP}; -- "PP" --
    Derive_PhraseLevelTag_PRN = {PRN}; -- "PRN" --
    Derive_PhraseLevelTag_PRT = {PRT}; -- "PRT" --
    Derive_PhraseLevelTag_QP = {QP}; -- "QP" --
    Derive_PhraseLevelTag_RRC = {RRC}; -- "RRC" --
    Derive_PhraseLevelTag_UCP = {UCP}; -- "UCP" --
    Derive_PhraseLevelTag_VP = {VP}; -- "VP" --
    Derive_PhraseLevelTag_WHADJP = {WHADJP}; -- "WHADJP" --
    Derive_PhraseLevelTag_WHADVP = {WHADVP}; -- "WHADVP" --
    Derive_PhraseLevelTag_WHNP = {WHNP}; -- "WHNP" --
    Derive_PhraseLevelTag_WHPP = {WHPP}; -- "WHPP" --
    Derive_PhraseLevelTag_X = {X}; -- "X" --

    Derive_FunctionTag_ADV = {ADV}; -- "ADV" --
    Derive_FunctionTag_NOM = {NOM}; -- "NOM" --
    Derive_FunctionTag_DTV = {DTV}; -- "DTV" --
    Derive_FunctionTag_LGS = {LGS}; -- "LGS" --
    Derive_FunctionTag_PRD = {PRD}; -- "PRD" --
    Derive_FunctionTag_PUT = {PUT}; -- "PUT" --
    Derive_FunctionTag_SBJ = {SBJ}; -- "SBJ" --
    Derive_FunctionTag_TPC = {TPC}; -- "TPC" --
    Derive_FunctionTag_VOC = {VOC}; -- "VOC" --
    Derive_FunctionTag_BNF = {BNF}; -- "BNF" --
    Derive_FunctionTag_DIR = {DIR}; -- "DIR" --
    Derive_FunctionTag_EXT = {EXT}; -- "EXT" --
    Derive_FunctionTag_LOC = {LOC}; -- "LOC" --
    Derive_FunctionTag_MNR = {MNR}; -- "MNR" --
    Derive_FunctionTag_PRP = {PRP}; -- "PRP" --
    Derive_FunctionTag_TMP = {TMP}; -- "TMP" --
    Derive_FunctionTag_CLR = {CLR}; -- "CLR" --
    Derive_FunctionTag_CLF = {CLF}; -- "CLF" --
    Derive_FunctionTag_HLN = {HLN}; -- "HLN" --
    Derive_FunctionTag_TTL = {TTL}; -- "TTL" --


    Derive_WordTag_ADD = {ADD}; -- "ADD" --
    Derive_WordTag_AFX = {AFX}; -- "AFX" --




    Derive_WordTag_CC = {CC}; -- "CC" --
    Derive_WordTag_CD = {CD}; -- "CD" --
    Derive_WordTag_DT = {DT}; -- "DT" --
    Derive_WordTag_EX = {EX}; -- "EX" --
    Derive_WordTag_FW = {FW}; -- "FW" --
    Derive_WordTag_IN = {IN}; -- "IN" --
    Derive_WordTag_JJ = {JJ}; -- "JJ" --
    Derive_WordTag_JJR = {JJR}; -- "JJR" --
    Derive_WordTag_JJS = {JJS}; -- "JJS" --
    Derive_WordTag_LS = {LS}; -- "LS" --
    Derive_WordTag_MD = {MD}; -- "MD" --
    Derive_WordTag_NN = {NN}; -- "NN" --
    Derive_WordTag_NNS = {NNS}; -- "NNS" --
    Derive_WordTag_NNP = {NNP}; -- "NNP" --
    Derive_WordTag_NNPS = {NNPS}; -- "NNPS" --
    Derive_WordTag_PDT = {PDT}; -- "PDT" --
    Derive_WordTag_POS = {POS}; -- "POS" --
    Derive_WordTag_PRP = {PRP}; -- "PRP" --
    Derive_WordTag_PRP_dollar = {PRP_dollar}; -- "PRP$" --
    Derive_WordTag_RB = {RB}; -- "RB" --
    Derive_WordTag_RBR = {RBR}; -- "RBR" --
    Derive_WordTag_RBS = {RBS}; -- "RBS" --
    Derive_WordTag_RP = {RP}; -- "RP" --
    Derive_WordTag_SYM = {SYM}; -- "SYM" --
    Derive_WordTag_TO = {TO}; -- "TO" --
    Derive_WordTag_UH = {UH}; -- "UH" --
    Derive_WordTag_VB = {VB}; -- "VB" --
    Derive_WordTag_VBD = {VBD}; -- "VBD" --
    Derive_WordTag_VBG = {VBG}; -- "VBG" --
    Derive_WordTag_VBN = {VBN}; -- "VBN" --
    Derive_WordTag_VBP = {VBP}; -- "VBP" --
    Derive_WordTag_VBZ = {VBZ}; -- "VBZ" --
    Derive_WordTag_WDT = {WDT}; -- "WDT" --
    Derive_WordTag_WP = {WP}; -- "WP" --
    Derive_WordTag_WP_dollar = {WP_dollar}; -- "WP$" --
    Derive_WordTag_WRB = {WRB}; -- "WRB" --

    Derive_WordTag_ADD = {ADD}; -- "ADD" --
    Derive_WordTag_NFP = {NFP}; -- "NFP" --
    Derive_WordTag_AFX = {AFX}; -- "AFX" --
    Derive_WordTag_HYPH = {HYPH}; -- "HYPH" --
    Derive_WordTag_NIL = {NIL}; -- "NIL" --
    Derive_WordTag_LS = {LS}; -- "LS" --
    Derive_WordTag_EOS = {EOS}; -- "EOS" --
    Derive_WordTag_GW = {GW}; -- "GW" --
    Derive_WordTag_BN = {BN}; -- "BN" --
    Derive_WordTag_BX = {BX}; -- "BX" --
    Derive_WordTag_BQ = {BQ}; -- "BQ" --
    Derive_WordTag_BM = {BM}; -- "BM" --
    Derive_WordTag_BF = {BF}; -- "BF" --
    Derive_WordTag_BZ = {BZ}; -- "BZ" --
    Derive_WordTag_CC = {CC}; -- "CC" --
    Derive_WordTag_CD = {CD}; -- "CD" --
    Derive_WordTag_DT = {DT}; -- "DT" --
    Derive_WordTag_EX = {EX}; -- "EX" --
    Derive_WordTag_FW = {FW}; -- "FW" --
    Derive_WordTag_IN = {IN}; -- "IN" --
    Derive_WordTag_JJ = {JJ}; -- "JJ" --
    Derive_WordTag_JJR = {JJR}; -- "JJR" --
    Derive_WordTag_JJS = {JJS}; -- "JJS" --
    Derive_WordTag_LS = {LS}; -- "LS" --
    Derive_WordTag_MD = {MD}; -- "MD" --
    Derive_WordTag_NN = {NN}; -- "NN" --
    Derive_WordTag_NNS = {NNS}; -- "NNS" --
    Derive_WordTag_NNP = {NNP}; -- "NNP" --
    Derive_WordTag_NNPS = {NNPS}; -- "NNPS" --
    Derive_WordTag_PDT = {PDT}; -- "PDT" --
    Derive_WordTag_POS = {POS}; -- "POS" --
    Derive_WordTag_PRP = {PRP}; -- "PRP" --
    Derive_WordTag_PRP_dollar = {PRP_dollar}; -- "PRP$" --

    Derive_WordTag_RB = {RB}; -- "RB" --
    Derive_WordTag_RBR = {RBR}; -- "RBR" --
    Derive_WordTag_RBS = {RBS}; -- "RBS" --
    Derive_WordTag_RP = {RP}; -- "RP" --
    Derive_WordTag_SYM = {SYM}; -- "SYM" --
    Derive_WordTag_TO = {TO}; -- "TO" --
    Derive_WordTag_UH = {UH}; -- "UH" --
    Derive_WordTag_VB = {VB}; -- "VB" --
    Derive_WordTag_VBD = {VBD}; -- "VBD" --
    Derive_WordTag_VBG = {VBG}; -- "VBG" --
    Derive_WordTag_VBN = {VBN}; -- "VBN" --
    Derive_WordTag_VBP = {VBP}; -- "VBP" --
    Derive_WordTag_VBZ = {VBZ}; -- "VBZ" --
    Derive_WordTag_WDT = {WDT}; -- "WDT" --
    Derive_WordTag_WP = {WP}; -- "WP" --
    Derive_WordTag_WP_dollar = {WP_dollar}; -- "WP$" --
    Derive_WordTag_WRB = {WRB}; -- "WRB" --


    Derive_Num1 = {num1}; -- "1" --
    Derive_Num2 = {num2}; -- "2" --
    Derive_Num3 = {num3}; -- "3" --
    Derive_Num4 = {num4}; -- "4" --
    Derive_Num5 = {num5}; -- "5" --
    Derive_Num6 = {num6}; -- "6" --
    Derive_Num7 = {num7}; -- "7" --
    Derive_Num8 = {num8}; -- "8" --
    Derive_Num9 = {num9}; -- "9" --
    Derive_Num10 = {num10}; -- "10" --
    Derive_Num11 = {num11}; -- "11" --
    Derive_Num12 = {num12}; -- "12" --
    Derive_Num13 = {num13}; -- "13" --
    Derive_Num14 = {num14}; -- "14" --
    Derive_Num15 = {num15}; -- "15" --
    Derive_Num16 = {num16}; -- "16" --


    -- the following should be automatically generated --
    Materialize_Input_word = "XX";
}}