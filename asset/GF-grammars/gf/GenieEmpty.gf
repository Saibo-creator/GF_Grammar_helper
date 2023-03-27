abstract GenieEmpty = {
  flags coding = utf8 ;
  flags startcat = Triplet ;
  cat
    Triplet ; Subject ; Object ; Relation ; Rel; Entity;Left;Right; 
  fun
    Repeat:  Triplet -> Triplet -> Triplet ;
    Empty: Triplet;
    Build_triplet : Subject -> Relation -> Object -> Triplet ;
    Build_relation: Left -> Rel -> Right -> Relation;
    Build_subject: Left -> Entity -> Right -> Subject;
    Build_object: Left -> Entity -> Right -> Object;
    Left_bracket: Left;
    Right_bracket: Right;
    -- the following should be automatically generated --
    Germany, France, UK, US: Entity;
    Is, Has: Rel;

} -- 描述了自下而上的建立树的过程 -- 