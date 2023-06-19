concrete {crt_grammar_name} of {abs_grammar_name} = {{
  lincat
    Text , BOG , EOG , Mention , Entity , OpenBracket , CloseBracket , Canonical_phrase = Str;
  lin
    Start a b c d e f g = a ++ b ++ c ++ d ++ e ++ f ++ g;
    Materialise_BOG = {bog_tokens};
    Materialise_EOG = {eog_tokens};
    Materialise_OpenBracket = {open_bracket_tokens};
    Materialise_CloseBracket = {close_bracket_tokens};
    Materialise_Mention = {mention_tokens};
    Materialise_Canonical_phrase = {canonical_phrase_tokens};

    -- the following should be automatically generated --
    {Materialize_Entities}
}}