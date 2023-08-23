# Information Extraction

## Knowledge Graph Constraints

- [EnglishWikipedia(Large)]
  - Description: With Wikidata (Vrandeˇ ci ́ c, 2012)(Dumps from 2019/08/01) filtering out all entities that do not have an English Wikipedia page associated. The filtering guarantees that all entity names are unique.
  - Entity: 5,891,959
  - Relation: 857
  - Reference: GenIE paper
  - Usage: `large_schema` in `GenIE` repo
- [WikiDataREBELIntersect(Medium)]
  - Description: Starts with the previous KG, only keep entities and relations that appear in the REBEL dataset.
  - Entity: 2.7M
  - Relation: 1088
  - Reference: SynthIE paper
  - Usage: `constrained_worlds/genie` in `SynthIE` repo
  - Comment: Strict Subset of `EnglishWikipedia(Large)`, Great for REBEL experiments
- [WikiNRE(Small)]
  - Description: Constructed by aligning hyperlinks to wikidata entities((Trisedya et al., 2019)
  - Entity: 278, 204
  - Relation: 157
  - Reference: GenIE paper
  - Comment: This is not really a KG, but a dataset for relation extraction. It is small, so can be used for debugging.
  - Usage: `small_schema` in `GenIE` repo
