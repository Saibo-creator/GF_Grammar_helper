abstract {abs_grammar_name} = {{
  flags coding = utf8 ;
  flags startcat = Text ;
  cat
    Text ; BOG ; EOG ; Mention; Entity ; OpenBracket ; CloseBracket ; Canonical_phrase ;
  fun
    Start: BOG -> Mention -> Canonical_phrase -> OpenBracket -> Entity -> CloseBracket -> EOG -> Text ;
    Materialise_BOG: BOG;
    Materialise_EOG: EOG;
    Materialise_OpenBracket: OpenBracket;
    Materialise_CloseBracket: CloseBracket;
    Materialise_Mention: Mention;
    Materialise_Canonical_phrase: Canonical_phrase;

    -- the following should be automatically generated --
    {Materialize_Entities}: Entity; -- line to replace, "Entity1, Entity2, Entity3, Entity4" --
}}