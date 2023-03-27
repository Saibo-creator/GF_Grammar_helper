module GenieBasic where

import PGF hiding (Tree)

----------------------------------------------------
-- automatic translation from GF to Haskell
----------------------------------------------------

class Gf a where
  gf :: a -> Expr
  fg :: Expr -> a

newtype GString = GString String deriving Show

instance Gf GString where
  gf (GString x) = mkStr x
  fg t =
    case unStr t of
      Just x  ->  GString x
      Nothing -> error ("no GString " ++ show t)

newtype GInt = GInt Int deriving Show

instance Gf GInt where
  gf (GInt x) = mkInt x
  fg t =
    case unInt t of
      Just x  ->  GInt x
      Nothing -> error ("no GInt " ++ show t)

newtype GFloat = GFloat Double deriving Show

instance Gf GFloat where
  gf (GFloat x) = mkFloat x
  fg t =
    case unFloat t of
      Just x  ->  GFloat x
      Nothing -> error ("no GFloat " ++ show t)

----------------------------------------------------
-- below this line machine-generated
----------------------------------------------------

data GEntity =
   GFrance 
 | GGermany 
 | GUK 
 | GUS 
  deriving Show

data GLeft = GLeft_bracket 
  deriving Show

data GObject = GBuild_object GLeft GEntity GRight 
  deriving Show

data GRel =
   GHas 
 | GIs 
  deriving Show

data GRelation = GBuild_relation GLeft GRel GRight 
  deriving Show

data GRight = GRight_bracket 
  deriving Show

data GSubject = GBuild_subject GLeft GEntity GRight 
  deriving Show

data GTriplet = GBuild_triplet GSubject GRelation GObject 
  deriving Show


instance Gf GEntity where
  gf GFrance = mkApp (mkCId "France") []
  gf GGermany = mkApp (mkCId "Germany") []
  gf GUK = mkApp (mkCId "UK") []
  gf GUS = mkApp (mkCId "US") []

  fg t =
    case unApp t of
      Just (i,[]) | i == mkCId "France" -> GFrance 
      Just (i,[]) | i == mkCId "Germany" -> GGermany 
      Just (i,[]) | i == mkCId "UK" -> GUK 
      Just (i,[]) | i == mkCId "US" -> GUS 


      _ -> error ("no Entity " ++ show t)

instance Gf GLeft where
  gf GLeft_bracket = mkApp (mkCId "Left_bracket") []

  fg t =
    case unApp t of
      Just (i,[]) | i == mkCId "Left_bracket" -> GLeft_bracket 


      _ -> error ("no Left " ++ show t)

instance Gf GObject where
  gf (GBuild_object x1 x2 x3) = mkApp (mkCId "Build_object") [gf x1, gf x2, gf x3]

  fg t =
    case unApp t of
      Just (i,[x1,x2,x3]) | i == mkCId "Build_object" -> GBuild_object (fg x1) (fg x2) (fg x3)


      _ -> error ("no Object " ++ show t)

instance Gf GRel where
  gf GHas = mkApp (mkCId "Has") []
  gf GIs = mkApp (mkCId "Is") []

  fg t =
    case unApp t of
      Just (i,[]) | i == mkCId "Has" -> GHas 
      Just (i,[]) | i == mkCId "Is" -> GIs 


      _ -> error ("no Rel " ++ show t)

instance Gf GRelation where
  gf (GBuild_relation x1 x2 x3) = mkApp (mkCId "Build_relation") [gf x1, gf x2, gf x3]

  fg t =
    case unApp t of
      Just (i,[x1,x2,x3]) | i == mkCId "Build_relation" -> GBuild_relation (fg x1) (fg x2) (fg x3)


      _ -> error ("no Relation " ++ show t)

instance Gf GRight where
  gf GRight_bracket = mkApp (mkCId "Right_bracket") []

  fg t =
    case unApp t of
      Just (i,[]) | i == mkCId "Right_bracket" -> GRight_bracket 


      _ -> error ("no Right " ++ show t)

instance Gf GSubject where
  gf (GBuild_subject x1 x2 x3) = mkApp (mkCId "Build_subject") [gf x1, gf x2, gf x3]

  fg t =
    case unApp t of
      Just (i,[x1,x2,x3]) | i == mkCId "Build_subject" -> GBuild_subject (fg x1) (fg x2) (fg x3)


      _ -> error ("no Subject " ++ show t)

instance Gf GTriplet where
  gf (GBuild_triplet x1 x2 x3) = mkApp (mkCId "Build_triplet") [gf x1, gf x2, gf x3]

  fg t =
    case unApp t of
      Just (i,[x1,x2,x3]) | i == mkCId "Build_triplet" -> GBuild_triplet (fg x1) (fg x2) (fg x3)


      _ -> error ("no Triplet " ++ show t)


