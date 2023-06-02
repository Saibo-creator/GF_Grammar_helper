abstract {abs_grammar_name} = {{
  flags coding = utf8 ;
  flags startcat = Text ;
  -- Leicestershire (UK Parliament constituency) --
  cat
    Text ; BOG ; EOG ; Entity ; OpenBracket ; CloseBracket ; StartMarker ; EndMarker ; {NumerateMentions} {NumeratedLeftContexts} {NumeratedRightContexts}; {NumerateUnits}

    --Mention1 ; LeftContext1 ; RightContext1 ;--
  fun
    Start: BOG ->  LeftContext0 -> {Units} -> EOG -> Text ; --Unit1 -> Unit2 -> Unit3--

    {Numerated_UnitDerivationRules}
    --Unit1: StartMarker -> Mention1 -> OpenBracket -> Entity -> CloseBracket -> EndMarker -> RightContext1;--

    --Unit2: StartMarker -> Mention2 -> OpenBracket -> Entity -> CloseBracket -> EndMarker -> RightContext2;--

    Materialise_BOG: BOG;
    Materialise_EOG: EOG;
    Materialise_OpenBracket: OpenBracket;
    Materialise_CloseBracket: CloseBracket;
    Materialise_StartMarker: StartMarker;
    Materialise_EndMarker: EndMarker;

    Materialise_LeftContext0: LeftContext0;

    {NumeratedRightContextDerivationRules}
--    Materialise_RightContext1_Derivation: RightContext1;
--    Materialise_RightContext2_Derivation: RightContext2;
--    Materialise_RightContext3_Derivation: RightContext3;

    {NumeratedMentionDerivationRules}
--    Materialise_Mention1_Derivation: Mention1;
--    Materialise_Mention2_Derivation: Mention2;
--    Materialise_Mention3_Derivation: Mention3;

    -- the following should be automatically generated --
    {Materialize_Entities}: Entity; -- line to replace, "Entity1, Entity2, Entity3, Entity4" --
}}