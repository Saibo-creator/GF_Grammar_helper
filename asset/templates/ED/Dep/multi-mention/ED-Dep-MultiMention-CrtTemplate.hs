concrete {crt_grammar_name} of {abs_grammar_name} = {{
  -- Leicestershire (UK Parliament constituency) --
  lincat
--      Text ; BOG ; EOG ; OpenBracket ; CloseBracket ; StartMarker ; EndMarker ; LeftContext0 ; {NumeratedMentions} ; {NumeratedRightContexts}; {NumeratedEntities} ; {NumeratedUnits} ;
    Text , BOG , EOG , OpenBracket , CloseBracket , StartMarker , EndMarker , LeftContext0 , {NumeratedMentions} , {NumeratedRightContexts} , {NumeratedEntities} , {NumeratedUnits} = Str;
  lin
    Start bog left_context0 {NumeratedUnitsAsInputVars} eog = bog ++ left_context0 ++ {NumeratedUnitsAsInputVarsConcat} ++ eog;
--    x_1 x_2 x_3 x_4 x_5 x_6 x_7 x_8 x_9 x_10 = x_1 ++ x_2 ++ x_3 ++ x_4 ++ x_5 ++ x_6 ++ x_7 ++ x_8 ++ x_9 ++ x_10;
    Materialise_BOG = {bog_tokens};
    Materialise_EOG = {eog_tokens};
    Materialise_OpenBracket = {open_bracket_tokens};
    Materialise_CloseBracket = {close_bracket_tokens};
    Materialise_LeftContext0 = {left_context0_tokens};
    Materialise_StartMarker = {start_marker_tokens};
    Materialise_EndMarker = {end_marker_tokens};

    {NumeratedUnitDerivationRules}
--    Unit1Derivation: start_marker mention1 open_bracket entity1 close_bracket end_marker right_context1 = start_marker ++ mention1 ++ open_bracket ++ entity1 ++ close_bracket ++ end_marker ++ right_context1;


    {NumeratedRightContextMaterialisationRules}


    {NumeratedMentionMaterialisationRules}


    {Materialize_Entities}

}}