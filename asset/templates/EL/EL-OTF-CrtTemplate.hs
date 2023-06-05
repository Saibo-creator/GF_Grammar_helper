concrete {crt_grammar_name} of {abs_grammar_name} = {{
  lincat
    Text , BOG , EOG , Mention , Entity , OpenBracket , CloseBracket = Str;
  lin
    Start a b c d e f = a ++ b ++ c ++ d ++ e ++ f;
    Materialise_BOG = {bog_tokens};
    Materialise_EOG = {eog_tokens};
    Materialise_OpenBracket = {open_bracket_tokens};
    Materialise_CloseBracket = {close_bracket_tokens};
    Materialise_Mention = {mention_tokens};

    -- the following should be automatically generated --
    {Materialize_Entities}
}}