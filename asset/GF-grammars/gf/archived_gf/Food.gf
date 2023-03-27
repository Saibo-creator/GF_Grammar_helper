abstract Food = {
  flags startcat = Comment ;
  cat
    Comment ; Item ; Kind ; Quality ;
  fun
    Pred : Item -> Quality -> Comment ;
    This, That : Kind -> Item ;
    Mod : Quality -> Kind -> Kind ;
    Wine, Cheese, Fish : Kind ;
    Very : Quality -> Quality ;
    Fresh, Warm, Italian,Expensive, Delicious, Boring : Quality ;
}



-- 描述了自下而上的建立树的过程 -- 







{-
The step leading from BNF to GF is to separate the rules defining abstract syntax trees from the rules telling how trees are linearized. 
For example, the predication rule:

    Pred. Comment ::= Item "is" Quality
now becomes two rules:
    fun Pred : Item -> Quality -> Comment ;
    lin Pred item quality = item ++ "is" ++ quality ;
-}

{-
As customary in functional programming languages, arguments types and the value type are separated from each other by an arrow (->). 
This is ultimately justified by the technique of currying, which means that an n-place function is really a 1-place function that returns an n−1-place function.
A→B→C ≡≡ A→(B→C)
Currying has several advantages
-}