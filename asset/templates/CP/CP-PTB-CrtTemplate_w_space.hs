concrete {crt_grammar_name} of {abs_grammar_name} = {{
  lincat
    StartTree , Trees , Tree , SentenceTag , Left , Right , FullPhraseLevelTag , PhraseLevelTag , HyphenFunctionTags , HyphenFunctionTag , HyphenNumTag , Hyphen , FunctionTag , WordTag , Num , Input_word = Str;
  lin

    --Derive_StartTree: Left -> SentenceTag -> Trees -> Right -> StartTree;--
    Derive_StartTree a b c d = a ++ b ++ {Space} ++ c ++ d;

    -- Repeat:  Tree -> Trees -> Trees ; --
    Repeat a b = a ++ {Space} ++ b; -- (VP (VBN based) (PP-LOC-CLR (IN in) (NP (NNP New) (NNP York))--

    --Derive_Tree:  Left -> FullPhraseLevelTag -> Trees -> Right -> Tree;--
    Derive_Tree a b c d = a ++ b ++ {Space} ++ c ++ d; -- (NP-SBJ (NNP General) (NNP Motors) (NNP Corp.)) --


    --Derive_Trees:  Left -> FullPhraseLevelTag -> Trees -> Right -> Trees;--
    Derive_Trees a b c d = a ++ b ++ {Space} ++ c ++ d; -- (NP-SBJ (NNP General) (NNP Motors) (NNP Corp.)) --


    --Degenerate_Tree: Left -> WordTag -> Input_word -> Right -> Tree;--
    Degenerate_Tree a b c d = a ++ b ++ {Space} ++ c ++ d; -- (NNP Ford)--

    --Degenerate_Trees: Left -> WordTag -> Input_word -> Right -> Trees;--
    Degenerate_Trees a b c d = a ++ b ++ {Space} ++ c ++ d; -- (NNP Ford)--

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
    Degenerate_HyphenFunctionTag a b = a ++ b; -- -SBJ --

    --Degenerate_HyphenFunctionTags: Hyphen -> FunctionTag -> HyphenFunctionTags;--
    Degenerate_HyphenFunctionTags a b = a ++ b; -- -SBJ --

    --Empty_HyphenFunctionTag: HyphenFunctionTag;--
    Empty_HyphenFunctionTag = ""; -- --

    --Materialize_Hyphen: Hyphen;--
    Materialize_Hyphen = {Hyphen}; --"-"; --

    --Materialize_SentenceTag: SentenceTag;--
    Materialize_SentenceTag = {S}; --"S"; --

    --Materialize_Left: Left;--
    Materialize_Left = {Left_Paren}; --"("; --

    --Materialize_Right: Right;--
    Materialize_Right = {Right_Paren}; --")"; --

    Materialize_Input_word = {Input_Word}; --"XX"; --

    -- the following should be automatically generated --
    {constituency_linerization_rules}

}}