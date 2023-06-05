abstract {abs_grammar_name} = {{
  flags coding = utf8 ;
  flags startcat = Text ;
  -- Leicestershire (UK Parliament constituency) --
  cat
    Text ; BOG ; EOG ; OpenBracket ; CloseBracket ; StartMarker ; EndMarker ; LeftContext0 ; {NumeratedMentions} ; {NumeratedRightContexts}; {NumeratedEntities} ; {NumeratedUnits} ;
--    RightContext1 ; RightContext2 ; RightContext3 ; RightContext4 ; RightContext5 ; RightContext6 ; RightContext7 ; RightContext8 ; RightContext9 ; RightContext10 ; RightContext12 ;
--    ; RightContext13 ; RightContext14 ; RightContext15 ; RightContext16
--    ; Mention1 ; Mention2 ; Mention3 ; Mention4 ; Mention5 ; Mention6 ; Mention7 ; Mention8 ; Mention9 ; Mention10 ; Mention11 ; Mention12 ; Mention13 ; Mention14 ; Mention15 ; Mention16 ;


    --Mention1 ; LeftContext1 ; RightContext1 ;--
  fun
    Start: BOG ->  LeftContext0 -> {NumeratedUnitsAsInputVars} -> EOG -> Text ;
--    Unit1 -> Unit2 -> Unit3 -> Unit4 -> Unit5 -> Unit6 -> Unit7 -> Unit8 -> Unit9 -> Unit10 -> Unit11 -> Unit12 -> Unit13 -> Unit14 -> Unit15 -> Unit16 -> EOG -> Text ;

    {NumeratedUnitDerivationRules}

--    Unit1Derivation: StartMarker -> Mention1 -> OpenBracket -> Entity -> CloseBracket -> EndMarker -> RightContext1 -> Unit1;
--    Unit2Derivation: StartMarker -> Mention1 -> OpenBracket -> Entity -> CloseBracket -> EndMarker -> RightContext2 -> Unit2;

    Materialise_BOG: BOG;
    Materialise_EOG: EOG;
    Materialise_OpenBracket: OpenBracket;
    Materialise_CloseBracket: CloseBracket;
    Materialise_StartMarker: StartMarker;
    Materialise_EndMarker: EndMarker;
    Materialise_LeftContext0: LeftContext0;

    {NumeratedRightContextMaterialisationRules}
--    Materialise_RightContext1_Materialisation: RightContext1;
--    Materialise_RightContext2_Materialisation: RightContext2;
--    Materialise_RightContext3_Materialisation: RightContext3;

    {NumeratedMentionMaterialisationRules}
--    Materialise_Mention1_Materialisation: Mention1;
--    Materialise_Mention2_Materialisation: Mention2;
--    Materialise_Mention3_Materialisation: Mention3;

    -- the following should be automatically generated --
    {NumeratedEntitiesMaterialisationRules} -- line to replace, "Entity1, Entity2, Entity3, Entity4" --
}}