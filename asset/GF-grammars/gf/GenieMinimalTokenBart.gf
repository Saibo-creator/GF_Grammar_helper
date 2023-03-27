concrete GenieMinimalTokenBart of GenieMinimalToken = {
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
    Germany = Ger ++ Many;
    Ger = "ger";
    Many = "many";
    France = Fra ++ Nce;
    Fra = "fra";
    Nce = "nce";

    UK = U++K;
    U = "u";
    K = "k";
    US = U++S;
    S = "s";

    Is = "is";
    Has = "has";
}