concrete {crt_grammar_name} of {abs_grammar_name} = {{
  -- [s] John [r] lives in [o] New York [e] [s] John [r] likes [o] pizza [e] [s] Mary [r] lives in [o] London [e] --
  lincat
    Text , BOG , EOG , Triplet , Triplets , Doublet, Doublets, Subject , Relation , Object , TripletEndingMarker , SubjectMarker , RelationMarker , objectMarker , Rel , Entity = Str;
  lin
    Start x y z = x ++ y ++ z;
    Repeat x y = x ++ y;
    Empty_triplet = [];
    Empty_triplets = [];
    Derive_triplet x y z = x ++ y ++ z ;
    Derive_triplets x y z = x ++ y ++ z ;
    Repeat_Doublet x y = x ++ y;
    Derive_doublet x y = x ++ y ;
    Derive_doublets x y = x ++ y ;

    Derive_subject x y = x ++ y ;
    Derive_relation x y = x ++ y ;
    Derive_object x y = x ++ y ;

    Materialise_BOG = {bog_tokens};
    Materialise_EOG = {eog_tokens};
    Materialise_SubjectMarker = {SubjectMarker_tokens}; -- [s] --
    Materialise_RelationMarker = {RelationMarker_tokens}; -- [r] --
    Materialise_objectMarker = {objectMarker_tokens}; -- [o] --
    Materialise_tripletEndingMarker = {TripletEndingMarker_tokens}; -- [e] --

    -- the following should be automatically generated --
    {Materialize_Entities} --Germany = "ger"++"many"; France = "fra"++"nce"; UK = "u"++"k"; US = "u"++"s"; line to replace--
    {rel_lin_str} -- Is = "is"; Has = "has"; line to replace--
}}