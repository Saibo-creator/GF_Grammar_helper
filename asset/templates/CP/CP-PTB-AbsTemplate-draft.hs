abstract {abs_grammar_name} = {{
  flags coding = utf8 ;
  flags startcat = StartTree ;
  cat
    StartTree ; Trees ; Tree; SentenceTag ; Left ; Right ; FullPhraseLevelTag ; PhraseLevelTag ; HyphenFunctionTags ; HyphenFunctionTag ; HyphenNumTag ; Hyphen ; FunctionTag ; WordTag ; Num ; Input_word ; BOG ; EOG ; OpenBracket ; CloseBracket ;
  fun
    Derive_StartTree: BOG -> OpenBracket -> Left -> SentenceTag -> Trees -> Right -> CloseBracket -> EOG -> StartTree;
    Repeat:  Tree -> Trees -> Trees ;

    Materialise_BOG: BOG;
    Materialise_EOG: EOG;
    Materialise_OpenBracket: OpenBracket;
    Materialise_CloseBracket: CloseBracket;

    Derive_Tree:  Left -> FullPhraseLevelTag -> Trees -> Right -> Tree;
    Derive_Trees:  Left -> FullPhraseLevelTag -> Trees -> Right -> Trees;
    Degenerate_Tree: Left -> WordTag -> Input_word -> Right -> Tree;
    Degenerate_Trees: Left -> WordTag -> Input_word -> Right -> Trees;

    Derive_FullPhraseLevelTag: PhraseLevelTag -> HyphenFunctionTags -> HyphenNumTag -> FullPhraseLevelTag;
    Derive_HyphenFunctionTags: HyphenFunctionTag -> HyphenFunctionTags -> HyphenFunctionTags;
    Empty_HyphenFunctionTags: HyphenFunctionTags;
    Derive_HyphenNumTag: Hyphen -> Num -> HyphenNumTag;
    Empty_HyphenNumTag: HyphenNumTag;


    Derive_HyphenFunctionTag: Hyphen -> FunctionTag -> HyphenFunctionTag;
    Empty_HyphenFunctionTag: HyphenFunctionTag;

    Materialize_Hyphen: Hyphen;
    Materialize_SentenceTag: SentenceTag;
    Materialize_Left: Left;
    Materialize_Right: Right;

    -- the following should be automatically generated --
    Derive_PhraseLevelTag_S, Derive_PhraseLevelTag_SBAR, Derive_PhraseLevelTag_SBARQ, Derive_PhraseLevelTag_SINV, Derive_PhraseLevelTag_SQ, Derive_PhraseLevelTag_ADJP, Derive_PhraseLevelTag_ADVP, Derive_PhraseLevelTag_CONJP, Derive_PhraseLevelTag_FRAG, Derive_PhraseLevelTag_INTJ, Derive_PhraseLevelTag_LST, Derive_PhraseLevelTag_NAC, Derive_PhraseLevelTag_NP, Derive_PhraseLevelTag_NX, Derive_PhraseLevelTag_PP, Derive_PhraseLevelTag_PRN, Derive_PhraseLevelTag_PRT, Derive_PhraseLevelTag_QP, Derive_PhraseLevelTag_RRC, Derive_PhraseLevelTag_UCP, Derive_PhraseLevelTag_VP, Derive_PhraseLevelTag_WHADJP, Derive_PhraseLevelTag_WHADVP, Derive_PhraseLevelTag_WHNP, Derive_PhraseLevelTag_WHPP, Derive_PhraseLevelTag_X: PhraseLevelTag;

    Derive_FunctionTag_ADV, Derive_FunctionTag_NOM, Derive_FunctionTag_DTV, Derive_FunctionTag_LGS, Derive_FunctionTag_PRD, Derive_FunctionTag_PUT, Derive_FunctionTag_SBJ, Derive_FunctionTag_TPC, Derive_FunctionTag_VOC, Derive_FunctionTag_BNF, Derive_FunctionTag_DIR, Derive_FunctionTag_EXT, Derive_FunctionTag_LOC, Derive_FunctionTag_MNR, Derive_FunctionTag_PRP, Derive_FunctionTag_TMP, Derive_FunctionTag_CLR, Derive_FunctionTag_CLF, Derive_FunctionTag_HLN, Derive_FunctionTag_TTL: FunctionTag;

    Derive_WordTag_CC, Derive_WordTag_CD, Derive_WordTag_DT, Derive_WordTag_EX, Derive_WordTag_FW, Derive_WordTag_IN, Derive_WordTag_JJ, Derive_WordTag_JJR, Derive_WordTag_JJS, Derive_WordTag_LS, Derive_WordTag_MD, Derive_WordTag_NN, Derive_WordTag_NNS, Derive_WordTag_NNP, Derive_WordTag_NNPS, Derive_WordTag_PDT, Derive_WordTag_POS, Derive_WordTag_PRP, Derive_WordTag_PRP$, Derive_WordTag_RB, Derive_WordTag_RBR, Derive_WordTag_RBS, Derive_WordTag_RP, Derive_WordTag_SYM, Derive_WordTag_TO, Derive_WordTag_UH, Derive_WordTag_VB, Derive_WordTag_VBD, Derive_WordTag_VBG, Derive_WordTag_VBN, Derive_WordTag_VBP, Derive_WordTag_VBZ, Derive_WordTag_WDT, Derive_WordTag_WP, Derive_WordTag_WP$, Derive_WordTag_WRB, Derive_WordTag_ADD, Derive_WordTag_NFP, Derive_WordTag_AFX, Derive_WordTag_HYPH, Derive_WordTag_NIL, Derive_WordTag_LS, Derive_WordTag_EOS, Derive_WordTag_GW, Derive_WordTag_BN, Derive_WordTag_BX, Derive_WordTag_BQ, Derive_WordTag_BM, Derive_WordTag_BF, Derive_WordTag_BZ, Derive_WordTag_CC, Derive_WordTag_CD, Derive_WordTag_DT, Derive_WordTag_EX, Derive_WordTag_FW, Derive_WordTag_IN, Derive_WordTag_JJ, Derive_WordTag_JJR, Derive_WordTag_JJS, Derive_WordTag_LS, Derive_WordTag_MD, Derive_WordTag_NN, Derive_WordTag_NNS, Derive_WordTag_NNP, Derive_WordTag_NNPS, Derive_WordTag_PDT, Derive_WordTag_POS, Derive_WordTag_PRP, Derive_WordTag_PRP$, Derive_WordTag_RB, Derive_WordTag_RBR, Derive_WordTag_RBS, Derive_WordTag_RP, Derive_WordTag_SYM, Derive_WordTag_TO, Derive_WordTag_UH, Derive_WordTag_VB, Derive_WordTag_VBD, Derive_WordTag_VBG, Derive_WordTag_VBN, Derive_WordTag_VBP, Derive_WordTag_VBZ, Derive_WordTag_WDT, Derive_WordTag_WP, Derive_WordTag_WP$, Derive_WordTag_WRB: WordTag;

    Derive_Num1, Derive_Num2, Derive_Num3, Derive_Num4, Derive_Num5, Derive_Num6, Derive_Num7, Derive_Num8, Derive_Num9, Derive_Num10, Derive_Num11, Derive_Num12, Derive_Num13, Derive_Num14, Derive_Num15, Derive_Num16 : Num;

    Materialize_Input_word: Input_word;

    -- tokens_0-1: Input_word; --
    -- tokens_0-2: Input_word; --
    -- tokens_0-3: Input_word; --
    -- tokens_0-4: Input_word; --
    --...--
    -- tokens_0-512: Input_word; --
    -- tokens_1-2: Input_word; --
    -- tokens_1-3: Input_word; --
}}

