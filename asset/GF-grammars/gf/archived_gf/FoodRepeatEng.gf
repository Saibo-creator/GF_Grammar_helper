concrete FoodRepeatEng of FoodRepeat = {
  lincat
    Comment, Sentence, Item, Kind, Quality = Str ;
  lin
    Repeat x y = x ++ ";" ++ y ;
    Pred x y = x ++ "is" ++ y ;
    Predd x y = x ++ "is" ++ y ;
    This kind = "this" ++ kind ;
    That kind = "that" ++ kind ;
    Mod quality kind = quality ++ kind ;
    Wine = "wine" ;
    Cheese = "cheese" ;
    Fish = "fish" ;
    Very quality = "very" ++ quality ;
    Fresh = "fresh" ;
    Warm = "warm" ;
    Italian = "Italian" ;
    Expensive = "expensive" ;
    Delicious = "delicious" ;
    Boring = "boring" ;
}

--相当于对parse tree 自下而上recursively的调用stringfy 函数