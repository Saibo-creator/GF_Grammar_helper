concrete {crt_grammar_name} of {abs_grammar_name} = {{

  lincat
    Text , BOG , EOG , Mention , Entity , OpenBracket , CloseBracket , LeftContext , RightContext , StartMarker , EndMarker = Str;
  lin
    Start bog left_context start_marker mention open_bracket entity close_bracket end_marker right_context eog = bog ++ left_context ++ start_marker ++ mention ++ open_bracket ++ entity ++ close_bracket ++ end_marker ++ right_context ++ eog;
--    x_1 x_2 x_3 x_4 x_5 x_6 x_7 x_8 x_9 x_10 = x_1 ++ x_2 ++ x_3 ++ x_4 ++ x_5 ++ x_6 ++ x_7 ++ x_8 ++ x_9 ++ x_10;
    Materialise_BOG = {bog_tokens};
    Materialise_EOG = {eog_tokens};
    Materialise_OpenBracket = {open_bracket_tokens};
    Materialise_CloseBracket = {close_bracket_tokens};
    Materialise_LeftContext = {LeftContext_tokens};
    Materialise_RightContext = {RightContext_tokens};
    Materialise_StartMarker = {StartMarker_tokens};
    Materialise_EndMarker = {EndMarker_tokens};
    Materialise_Mention = {mention_tokens};

    -- the following should be automatically generated --
    {Materialize_Entities}
}}