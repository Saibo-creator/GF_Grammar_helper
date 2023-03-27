concrete GenieMinimalBart of GenieMinimal = {
  lincat
    Triplet , Subject , Object , Relation , Rel, Entity, Left, Right = Str;
  lin
    Repeat x y = x ++ y;
    Empty = "EOT"; --[];--
    Build_triplet x y z = x ++ y ++ z ;
    Build_relation x y z = x ++ y ++ z ;
    Build_subject x y z = x ++ y ++ z ;
    Build_object x y z = x ++ y ++ z ;

    Left_bracket = "<" ;
    Right_bracket = ">" ;
    -- the following should be automatically generated --
    Germany = ["ger many"]; -- "ger"++"many" --
    France = ["fra nce"]; -- "fra"++"nce" --
    UK = ["u k"]; -- "u"++"k" --
    US = ["u s"]; -- "u"++"s" --
    Is = "is";
    Has = "has";
}