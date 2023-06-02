# Caveats

## Some tokenizers don't have a `bos_token` and `eos_token` attribute. t5-flan

In this case, how should we handle this ? Maybe set the `bos_token` and `eos_token` manually ?

Because we will need them in the grammar.
```haskell
concrete {crt_grammar_name} of {abs_grammar_name} = {{
  -- [s] John [r] lives in [o] New York [e] [s] John [r] likes [o] pizza [e] [s] Mary [r] lives in [o] London [e] --
  lincat
    Text , BOT , EOT , Triplet , Triplets , Subject , Relation , Object , TripletEndingMarker , SubjectMarker , RelationMarker , objectMarker , Rel , Entity = Str;
  lin
    Start x y z = x ++ y ++ z;
    Repeat x y = x ++ y;
    Empty = {eos_token};  --[];--
    Build_triplet x y z w = x ++ y ++ z ++ w ;
    Build_triplets x y z w = x ++ y ++ z ++ w ;
    Build_relation x y = x ++ y ;
    Build_subject x y = x ++ y ;
    Build_object x y = x ++ y ;

    Materialise_BOT = {bos_token};
    Materialise_EOT = {eos_token};
    Materialise_SubjectMarker = {SubjectMarker_tokens}; -- [s] --
    Materialise_RelationMarker = {RelationMarker_tokens}; -- [r] --
    Materialise_objectMarker = {objectMarker_tokens}; -- [o] --
    Materialise_tripletEndingMarker = {TripletEndingMarker_tokens}; -- [e] --

    -- the following should be automatically generated --
    {Materialize_Entities} --Germany = "ger"++"many"; France = "fra"++"nce"; UK = "u"++"k"; US = "u"++"s"; line to replace--
    {rel_lin_str} -- Is = "is"; Has = "has"; line to replace--
}}
```