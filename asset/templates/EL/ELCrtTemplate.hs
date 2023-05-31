concrete {crt_grammar_name} of {abs_grammar_name} = {{
  -- Leicestershire (UK Parliament constituency) --
  lincat
    Text , BOG , EOG , Entity = Str;
  lin
    Start x y z = x ++ y ++ z;
    Materialise_BOG = {bog_tokens};
    Materialise_EOG = {eog_tokens};

    -- the following should be automatically generated --
    {entity_lin_str}
}}