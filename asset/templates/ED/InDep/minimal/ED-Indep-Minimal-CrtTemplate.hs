concrete {crt_grammar_name} of {abs_grammar_name} = {{
  lincat
    Text , BOG , EOG , Entity , OpenBracket , CloseBracket = Str;
  lin
    Start x y z = x ++ y ++ z;
    Materialise_BOG = {bog_tokens};
    Materialise_EOG = {eog_tokens};
    Materialise_OpenBracket = {open_bracket_tokens};
    Materialise_CloseBracket = {close_bracket_tokens};

    -- the following should be automatically generated --
    {Materialize_Entities}
}}