abstract {abs_grammar_name} = {{
  flags coding = utf8 ;
  flags startcat = Text ;

  cat
    Text ; BOG ; EOG ; Mention; Entity ; OpenBracket ; CloseBracket ; LeftContext ; RightContext ; StartMarker ; EndMarker ;
  fun
    Start: BOG -> LeftContext -> StartMarker -> Mention -> OpenBracket -> Entity -> CloseBracket -> EndMarker -> RightContext -> EOG -> Text ;

    Materialise_BOG: BOG;
    Materialise_EOG: EOG;
    Materialise_OpenBracket: OpenBracket;
    Materialise_CloseBracket: CloseBracket;
    Materialise_Mention: Mention;
    Materialise_LeftContext: LeftContext;
    Materialise_RightContext: RightContext;
    Materialise_StartMarker: StartMarker;
    Materialise_EndMarker: EndMarker;

    -- the following should be automatically generated --
    {Materialize_Entities}: Entity; -- line to replace, "Entity1, Entity2, Entity3, Entity4" --
}}