abstract {abs_grammar_name} = {{
  flags coding = utf8 ;
  flags startcat = Text ;
  -- [s] John [r] lives in [o] New York [e] [s] John [r] likes [o] pizza [e] [s] Mary [r] lives in [o] London [e] --
  cat
    Text ; BOG ; EOG ; Triplet ; Triplets ; Subject ; Relation; Object ; Triplet_ending_marker; Subject_marker ; Relation_marker; Object_marker ; Rel ; Entity ;
  fun
    Start: BOG -> Triplets -> EOG -> Text ;
    Repeat:  Triplet -> Triplets -> Triplets ;
    Empty_triplet: Triplet;
    Empty_triplets: Triplets;
    Derive_triplet : Subject -> Relation -> Object -> Triplet_ending_marker -> Triplet ;
    Derive_triplets : Subject -> Relation -> Object -> Triplet_ending_marker -> Triplets ;
    Derive_subject: Subject_marker -> Entity -> Subject;
    Derive_relation: Relation_marker -> Rel -> Relation;
    Derive_object: Object_marker -> Entity -> Object;

    Materialise_BOG: BOG;
    Materialise_EOG: EOG;
    Materialise_subject_marker: Subject_marker;
    Materialise_relation_marker: Relation_marker;
    Materialise_object_marker: Object_marker;
    Materialise_triplet_ending_marker: Triplet_ending_marker;

    -- the following should be automatically generated --
    {entities_str}: Entity; -- line to replace, "Germany, France, UK, US" --
    {relations_str}: Rel; -- line to replace, "Is, Has" --
}}