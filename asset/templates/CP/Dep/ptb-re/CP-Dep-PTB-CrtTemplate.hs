concrete {crt_grammar_name} of {abs_grammar_name} = {{
  lincat
    S , {cat_B_2D} , {cat_C_2D} , {cat_E_2D} , {cat_W_1D} = Str;
    Left , Right , FullPhraseLevelTag , WordLevelTag  = Str;
  lin

    {Rule0_0D}
    {Rule1_2D}
    {Rule2_2D}
    {Rule3_2D}
    {Rule4_2D}
    {Rule5_1D}
    {Rule6_2D}
    {Rule7_2D}
    {Rule8_1D}
    {Rule9_0D}

    {RuleW_1D}


--

--    Derive_FullPhraseLevelTag a b c = a ++ b ++ c;
--    Derive_HyphenFunctionTags a b = a ++ b;
--    Empty_HyphenFunctionTags = "";
--    Derive_HyphenNumTag a b = a ++ b;
--    Empty_HyphenNumTag = "";
--
--
--
--    Derive_HyphenFunctionTag a b = a ++ b;
--    Empty_HyphenFunctionTag = "";
--
--
--    Materialize_Hyphen = "-";
    Materialize_Left = "(";
    Materialize_Right = ")";

--    Derive_PhraseLevelTag_S = "S";
--    Derive_PhraseLevelTag_SBAR = "SBAR";
--    Derive_PhraseLevelTag_SBARQ = "SBARQ";
--    Derive_PhraseLevelTag_SINV = "SINV";
--    Derive_PhraseLevelTag_SQ = "SQ";
--    Derive_PhraseLevelTag_ADJP = "ADJP";
--    Derive_PhraseLevelTag_ADVP = "ADVP";
--    Derive_PhraseLevelTag_CONJP = "CONJP";
--    Derive_PhraseLevelTag_FRAG = "FRAG";
--    Derive_PhraseLevelTag_INTJ = "INTJ";
--    Derive_PhraseLevelTag_LST = "LST";
--    Derive_PhraseLevelTag_NAC = "NAC";
--    Derive_PhraseLevelTag_NP = "NP";
--    Derive_PhraseLevelTag_NX = "NX";
--    Derive_PhraseLevelTag_PP = "PP";
--    Derive_PhraseLevelTag_PRN = "PRN";
--    Derive_PhraseLevelTag_PRT = "PRT";
--    Derive_PhraseLevelTag_QP = "QP";
--    Derive_PhraseLevelTag_RRC = "RRC";
--    Derive_PhraseLevelTag_UCP = "UCP";
--    Derive_PhraseLevelTag_VP = "VP";
--    Derive_PhraseLevelTag_WHADJP = "WHADJP";
--    Derive_PhraseLevelTag_WHADVP = "WHADVP";
--    Derive_PhraseLevelTag_WHNP = "WHNP";
--    Derive_PhraseLevelTag_WHPP = "WHPP";
--    Derive_PhraseLevelTag_X = "X";
--
--    Derive_FunctionTag_ADV = "ADV";
--    Derive_FunctionTag_NOM = "NOM";
--    Derive_FunctionTag_DTV = "DTV";
--    Derive_FunctionTag_LGS = "LGS";
--    Derive_FunctionTag_PRD = "PRD";
--    Derive_FunctionTag_PUT = "PUT";
--    Derive_FunctionTag_SBJ = "SBJ";
--    Derive_FunctionTag_TPC = "TPC";
--    Derive_FunctionTag_VOC = "VOC";
--    Derive_FunctionTag_BNF = "BNF";
--    Derive_FunctionTag_DIR = "DIR";
--    Derive_FunctionTag_EXT = "EXT";
--    Derive_FunctionTag_LOC = "LOC";
--    Derive_FunctionTag_MNR = "MNR";
--    Derive_FunctionTag_PRP = "PRP";
--    Derive_FunctionTag_TMP = "TMP";
--    Derive_FunctionTag_CLR = "CLR";
--    Derive_FunctionTag_CLF = "CLF";
--    Derive_FunctionTag_HLN = "HLN";
--    Derive_FunctionTag_TTL = "TTL";

    {Derive_FullPhraseLevelTags}
    {Derive_WordTags}

--    Derive_WordTag_ADD = "ADD";
--    Derive_WordTag_NFP = "NFP";
--    Derive_WordTag_AFX = "AFX";
--    Derive_WordTag_HYPH = "HYPH";
--    Derive_WordTag_NIL = "NIL";
--    Derive_WordTag_LS = "LS";
--    Derive_WordTag_EOS = "EOS";
--    Derive_WordTag_GW = "GW";
--    Derive_WordTag_BN = "BN";
--    Derive_WordTag_BX = "BX";
--    Derive_WordTag_BQ = "BQ";
--    Derive_WordTag_BM = "BM";
--    Derive_WordTag_BF = "BF";
--    Derive_WordTag_BZ = "BZ";
--
--    Derive_WordTag_CC = "CC";
--    Derive_WordTag_CD = "CD";
--    Derive_WordTag_DT = "DT";
--    Derive_WordTag_EX = "EX";
--    Derive_WordTag_FW = "FW";
--    Derive_WordTag_IN = "IN";
--    Derive_WordTag_JJ = "JJ";
--    Derive_WordTag_JJR = "JJR";
--    Derive_WordTag_JJS = "JJS";
--    Derive_WordTag_LS = "LS";
--    Derive_WordTag_MD = "MD";
--    Derive_WordTag_NN = "NN";
--    Derive_WordTag_NNS = "NNS";
--    Derive_WordTag_NNP = "NNP";
--    Derive_WordTag_NNPS = "NNPS";
--    Derive_WordTag_PDT = "PDT";
--    Derive_WordTag_POS = "POS";
--    Derive_WordTag_PRP = "PRP";
--    Derive_WordTag_PRP_DOLLAR = "PRP_DOLLAR";
--    Derive_WordTag_RB = "RB";
--    Derive_WordTag_RBR = "RBR";
--    Derive_WordTag_RBS = "RBS";
--    Derive_WordTag_RP = "RP";
--    Derive_WordTag_SYM = "SYM";
--    Derive_WordTag_TO = "TO";
--    Derive_WordTag_UH = "UH";
--    Derive_WordTag_VB = "VB";
--    Derive_WordTag_VBD = "VBD";
--    Derive_WordTag_VBG = "VBG";
--    Derive_WordTag_VBN = "VBN";
--    Derive_WordTag_VBP = "VBP";
--    Derive_WordTag_VBZ = "VBZ";
--    Derive_WordTag_WDT = "WDT";
--    Derive_WordTag_WP = "WP";
--    Derive_WordTag_WP_DOLLAR = "WP_DOLLAR";
--    Derive_WordTag_WRB = "WRB";



--    Derive_Num1 = "num1";
--    Derive_Num2 = "num2";
--    Derive_Num3 = "num3";
--    Derive_Num4 = "num4";
--    Derive_Num5 = "num5";
--    Derive_Num6 = "num6";
--    Derive_Num7 = "num7";
--    Derive_Num8 = "num8";
--    Derive_Num9 = "num9";
--    Derive_Num10 = "num10";
--    Derive_Num11 = "num11";
--    Derive_Num12 = "num12";
--    Derive_Num13 = "num13";
--    Derive_Num14 = "num14";
--    Derive_Num15 = "num15";
--    Derive_Num16 = "num16";


}}