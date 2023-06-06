abstract {abs_grammar_name} = {{
  flags coding = utf8 ;
  flags startcat = Text ;
  -- [s] John [r] lives in [o] New York [e] [s] John [r] likes [o] pizza [e] [s] Mary [r] lives in [o] London [e] --
  cat
    Text ; BOG ; EOG ; Triplet ; Triplets ; Subject ; Relation; Object ; TripletEndingMarker; SubjectMarker ; RelationMarker; objectMarker ; Rel ; Entity ;
  fun
    Start: BOG -> Triplets -> EOG -> Text ;
    Repeat:  Triplet -> Triplets -> Triplets ;
    Empty_triplet: Triplet;
    Empty_triplets: Triplets;
    Derive_triplet : Subject -> Relation -> Object -> TripletEndingMarker -> Triplet ;
    Derive_triplets : Subject -> Relation -> Object -> TripletEndingMarker -> Triplets ;
    Derive_subject: SubjectMarker -> Entity -> Subject;
    Derive_relation: RelationMarker -> Rel -> Relation;
    Derive_object: objectMarker -> Entity -> Object;

    Materialise_BOG: BOG;
    Materialise_EOG: EOG;
    Materialise_SubjectMarker: SubjectMarker;
    Materialise_RelationMarker: RelationMarker;
    Materialise_objectMarker: objectMarker;
    Materialise_tripletEndingMarker: TripletEndingMarker;

    -- the following should be automatically generated --
    {Materialize_Entities}: Entity; -- line to replace, "Germany, France, UK, US" --
    {Materialize_Relations}: Rel; -- line to replace, "Is, Has" --
}}