concrete GenieMinimalAlphabetLiteralBart of GenieMinimalAlphabetLiteral = {
  lincat
    Triplet , Subject , Object , Relation , Rel, Entity, Left, Right, A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z = Str;
  lin
    Repeat x y = x ++ ";" ++ y;
    Empty = "EOT"; --[];--
    Build_triplet x y z = x ++ y ++ z ;
    Build_relation x y z = x ++ y ++ z ;
    Build_subject x y z = x ++ y ++ z ;
    Build_object x y z = x ++ y ++ z ;

    Left_bracket = "<" ;
    Right_bracket = ">" ;
    -- the following should be automatically generated --
    Germany g e r m a n y = g ++ e ++ r ++ m ++ a ++ n ++ y;
    France f r a n c e = f ++ r ++ a ++ n ++ c ++ e;
    UK u k = u ++ k;
    US u s = u ++ s;

    Is i s = i ++ s;
    Has h a s = h ++ a ++ s;
}