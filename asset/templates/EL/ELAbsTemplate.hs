abstract {abs_grammar_name} = {{
  flags coding = utf8 ;
  flags startcat = Text ;
  cat
    Text ; BOG ; EOG ; Entity ; OpenBracket ; CloseBracket ;
  fun
    Start: BOG -> OpenBracket -> Entity -> CloseBracket -> EOG -> Text ;
    Materialise_BOG: BOG;
    Materialise_EOG: EOG;
    Materialise_OpenBracket: OpenBracket;
    Materialise_CloseBracket: CloseBracket;

    -- the following should be automatically generated --
    {Materialize_Entities}: Entity;
}}