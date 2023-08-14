abstract {abs_grammar_name} = {{
  flags coding = utf8 ;
  flags startcat = StartTree ;
  cat
    StartTree ; Trees ; Tree; SentenceTag ; Left ; Right ; FullPhraseLevelTag ;  WordLevelTag ; Num ; Input_word ; BOG ; EOG ; OpenBracket ; CloseBracket ;
  fun
    Derive_StartTree: BOG -> OpenBracket -> Left -> FullPhraseLevelTag -> Trees -> Right -> CloseBracket -> EOG -> StartTree;
    Repeat:  Tree -> Trees -> Trees ;
    Materialise_BOG: BOG;
    Materialise_EOG: EOG;
    Materialise_OpenBracket: OpenBracket;
    Materialise_CloseBracket: CloseBracket;

    Derive_Tree:  Left -> FullPhraseLevelTag -> Trees -> Right -> Tree;
    Derive_Trees:  Left -> FullPhraseLevelTag -> Trees -> Right -> Trees;
    Degenerate_Tree: Left -> WordLevelTag -> Input_word -> Right -> Tree;
    Degenerate_Trees: Left -> WordLevelTag -> Input_word -> Right -> Trees;

    {Derive_FullPhraseLevelTags}
    {Derive_WordTags}
    {input_substring_materialise_rules}
--
--    Derive_FullPhraseLevelTag: PhraseLevelTag -> HyphenFunctionTags -> HyphenNumTag -> FullPhraseLevelTag;
--    Derive_HyphenFunctionTags: HyphenFunctionTag -> HyphenFunctionTags -> HyphenFunctionTags;
--    Empty_HyphenFunctionTags: HyphenFunctionTags;
--    Empty_HyphenNumTag: HyphenNumTag;
--
--    Empty_HyphenFunctionTag: HyphenFunctionTag;

--    Materialize_SentenceTag: SentenceTag;
    Materialize_Left: Left;
    Materialize_Right: Right;

    -- the following should be automatically generated --

    -- input substrings --

    -- tokens_0-1: Input_word; --
    -- tokens_0-2: Input_word; --
    -- tokens_0-3: Input_word; --
    -- tokens_0-4: Input_word; --
    --...--
    -- tokens_0-512: Input_word; --
    -- tokens_1-2: Input_word; --
    -- tokens_1-3: Input_word; --
}}

