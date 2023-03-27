concrete GenieMinimalAlphabetBart of GenieMinimalAlphabet = {
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

    A_lin = "a";
    B_lin = "b";
    C_lin = "c";
    D_lin = "d";
    E_lin = "e";
    F_lin = "f";
    G_lin = "g";
    H_lin = "h";
    I_lin = "i";
    J_lin = "j";
    K_lin = "k";
    L_lin = "l";
    M_lin = "m";
    N_lin = "n";
    O_lin = "o";
    P_lin = "p";
    Q_lin = "q";
    R_lin = "r";
    S_lin = "s";
    T_lin = "t";
    U_lin = "u";
    V_lin = "v";
    W_lin = "w";
    X_lin = "x";
    Y_lin = "y";
    Z_lin = "z";
}