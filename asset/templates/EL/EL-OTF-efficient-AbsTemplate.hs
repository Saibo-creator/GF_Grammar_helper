abstract {abs_grammar_name} = {{
  flags coding = utf8 ;
  flags startcat = Text ;
  cat
    Text ; BOG ; EOG ; OpenBracket ; CloseBracket ; StartMarker ; EndMarker ; LeftContext0 ; {NumeratedMentions} ; {NumeratedRightContexts}; {NumeratedEntities} ; {NumeratedUnits} ;

  fun
    Start: BOG ->  LeftContext0 -> {NumeratedUnitsAsInputVars} -> EOG -> Text ;

    {NumeratedUnitDerivationRules}

    Materialise_BOG: BOG;
    Materialise_EOG: EOG;
    Materialise_OpenBracket: OpenBracket;
    Materialise_CloseBracket: CloseBracket;
    Materialise_StartMarker: StartMarker;
    Materialise_EndMarker: EndMarker;
    Materialise_LeftContext0: LeftContext0;

    {NumeratedRightContextMaterialisationRules}

    {NumeratedMentionMaterialisationRules}

    {NumeratedEntitiesMaterialisationRules}
}}