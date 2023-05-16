abstract {abs_grammar_name} = {{
  flags coding = utf8 ;
  flags startcat = Text ;
  -- Leicestershire (UK Parliament constituency) --
  cat
    Text ; BOG ; EOG ; Entity ;
  fun
    Start: BOG -> Entity -> EOG -> Text ;
    Materialise_BOG: BOG;
    Materialise_EOG: EOG;

    -- the following should be automatically generated --
    {entities_str}: Entity; -- line to replace, "Germany, France, UK, US" --
}}