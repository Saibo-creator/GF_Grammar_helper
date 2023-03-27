abstract GenieMinimalAlphabet = {
  flags coding = utf8 ;
  flags startcat = Triplet ;
  cat
    Triplet ; Subject ; Object ; Relation ; Rel; Entity; Left; Right; A; B; C; D; E; F; G; H; I; J; K; L; M; N; O; P; Q; R; S; T; U; V; W; X; Y; Z;
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
    Germany: G -> E -> R -> M -> A -> N -> Y -> Entity;
    France: F -> R -> A -> N -> C -> E -> Entity;
    UK: U -> K -> Entity;
    US: U -> S -> Entity;

    Is: I -> S -> Rel;
    Has: H -> A -> S -> Rel;

    A_lin: A;
    B_lin: B;
    C_lin: C;
    D_lin: D;
    E_lin: E;
    F_lin: F;
    G_lin: G;
    H_lin: H;
    I_lin: I;
    J_lin: J;
    K_lin: K;
    L_lin: L;
    M_lin: M;
    N_lin: N;
    O_lin: O;
    P_lin: P;
    Q_lin: Q;
    R_lin: R;
    S_lin: S;
    T_lin: T;
    U_lin: U;
    V_lin: V;
    W_lin: W;
    X_lin: X;
    Y_lin: Y;
    Z_lin: Z;
}


-- 描述了自下而上的建立树的过程 --