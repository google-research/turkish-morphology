# Lexicon Annotation Guideline

This guideline outlines the tagsets and the annotation scheme that are used to
manually annotate the lexicon. All lexicon annotations that are submitted to
`//analyzer/src/lexicon` should follow this guideline.

## Directory structure

Lexicon files are grouped into two:

* Base lexicon files that are provided by the Project Steward(s) in
base lexicon directory (`//analyzer/src/lexicon/base`).
* Contrib lexicon files that are submitted by the contributors to this library
and reviewed by the Project Steward(s) upon submission in
contrib lexicon directory (`//analyzer/src/lexicon/contrib`).

Base lexicon contains 66 files with annotations on 47,202 words. Lexicon entries
are grouped into different files according to their annotated coarse and fine
part-of-speech tag (e.g. `adjective_jj.tsv` contains the annotations for
base adjectival root forms; see [Annotating part-of-speech][1] for the
definition of coarse and fine part-of-speech).

## Structure of a lexicon file

Lexicon files are TSVs (tab separated values). They should be structured
according to the following conventions:

* Lexicon files should use '.tsv' file extension.
* Lexicon files should be named as `[coarse_pos_tag]_[fine_pos_tag].tsv`, where
`[coarse_pos_tag]` and `[fine_pos_tag]` stands for the annotated part-of-speech
of the lexicon entries that can be found in that file.
* Lexicon file that is named as `[coarse_pos_tag]_[fine_pos_tag].tsv` should
only contain annotations for lexicon entries that are annotated for
`[fine_pos_tag]`.
* Submitted lexicon files should end with an empty line (`\n`).
* Each lexicon file should contain a header in its first row.
* Headers should have 5 columns (`tag`, `root`, `morphophonemics`, `features`
and `is_compound` exactly in this order).
* Rows beneath the header should include annotated lexicon entries.
* Every lexicon entry annotation should have 5 columns (each of which should
contain the annotated value for the respective field in the header).

Definition of the annotated fields are as follows:

* `tag` (*string*): part-of-speech tag of the root form (see
[Annotating part-of-speech][1]).
* `root` (*string*): stem of the word (see
[Annotating root form][2]).
* `morphophonemics` (*string*): morphophonemic irregularities of the root form,
which determines the surface form of the root after affixation of suffix
morphemes (see [Annotating morphophonemic irregularities][3]).
* `features` (*string*): morphological feature tags, which are used for
marking optional morphosemantic or morphosyntactic tags to be used in building a
morphological analyzer for Turkish (see [Annotating features][4]).
* `is_compound` (*bool*): marks nominal root forms that end with a Turkish
compounding marker `+SH` (see [Annotating compound roots][5]).

## Annotating part-of-speech

Every lexicon entry should have the part-of-speech annotated in the `tag` field.

To annotate part-of-speech;

1. decide on the root form by referring to [Annotating root form][2].
2. refer to the table of annotation tags and their descriptions and use the
annotation tag that applies to the root form as its part-of-speech annotation.

### Coarse part-of-speech tagset

Coarse part-of-speech tagset is a broad classification of the lexical
categories. It is not used in lexicon annotations but provided here as a
reference syntactic categorization to help develop a Turkish morphotactic model
(since agglutination patterns for each coarse part-of-speech vary drastically).

Below listed 15 tags compose our coarse part-of-speech tagset.

| Coarse Tag   | Description  |
|:------------ |:------------ |
| ADJ          | Adjective    |
| ADP          | Adposition   |
| ADV          | Adverb       |
| AFFIX        | Affix        |
| CONJ         | Conjunct     |
| DET          | Determiner   |
| EXS          | Existential  |
| NOUN         | Noun         |
| NUM          | Number       |
| ONOM         | Onomatopoeia |
| PRON         | Pronoun      |
| PRT          | Particle     |
| PUNCT        | Punctuation  |
| VERB         | Verb         |
| X            | Other        |

### Fine part-of-speech tagset

Fine part-of-speech tagset defines the lexical categories that can occur in
morphological analyses that are output by a morphological analyzer
implementation for Turkish. It is not used in the lexicon annotations.

This tagset provides a finer distinction of syntactic subcategorization in
comparison to coarse part-of-speech tagset. Each fine part-of-speech category
can be mapped to one of the coarse part-of-speech categories. Therefore, there
is a one-to-many mapping from coarse part-of-speech tags to fine part-of-speech.

Below listed 47 tags compose our fine part-of-speech tagset.

Note that some tags are specified as **derived categories** (marked as *Yes*
under *Is Derived Category?* column). Morphologically derived categories can
only occur in a morphological analysis as a result of affixation of a
derivational morpheme, therefore no cross classified lexicon will contain
entries with those fine part-of-speech tags. Such morphological derivations and
inventory of derivational morphemes are defined as part of the morphotactic
model.

| Coarse Tag | Fine Tag  | Is Derived Category? | Description                                                        |
|:---------- |:--------- |:-------------------- |:------------------------------------------------------------------ |
| ADJ        | JJ        | No                   | Adjective                                                          |
| ADJ        | VJ        | Yes                  | Verb in participle form                                            |
|            |           |                      |                                                                    |
| ADP        | IN        | No                   | Postposition                                                       |
|            |           |                      |                                                                    |
| ADV        | CRB       | Yes                  | Converb                                                            |
| ADV        | RB        | No                   | Adverb                                                             |
| ADV        | WRB       | No                   | Interrogative adverb                                               |
|            |           |                      |                                                                    |
| AFFIX      | PFX       | No                   | Prefix                                                             |
|            |           |                      |                                                                    |
| CONJ       | CC        | No                   | Coordinating conjunction                                           |
|            |           |                      |                                                                    |
| DET        | DT        | No                   | Determiner                                                         |
| DET        | PDT       | No                   | Predeterminer                                                      |
| DET        | WDT       | No                   | Wh-determiner                                                      |
|            |           |                      |                                                                    |
| EXS        | EX        | No                   | Existential                                                        |
|            |           |                      |                                                                    |
| NOUN       | ADD       | No                   | Electronic address (e-mail or URL)                                 |
| NOUN       | NN        | No                   | Common noun                                                        |
| NOUN       | NNP       | No                   | Proper noun                                                        |
| NOUN       | VN        | Yes                  | Verbal noun (head of a noun clause)                                |
|            |           |                      |                                                                    |
| NUM        | CD        | No                   | Cardinal number                                                    |
|            |           |                      |                                                                    |
| ONOM       | DUP       | No                   | Onomatopoeic                                                       |
|            |           |                      |                                                                    |
| PRON       | PRD       | No                   | Demonstrative pronoun                                              |
| PRON       | PRF       | Yes                  | Morphologically derived pronoun                                    |
| PRON       | PRI       | No                   | Indefinite pronoun                                                 |
| PRON       | PRP       | No                   | Personal pronoun                                                   |
| PRON       | PRP$      | No                   | Possessive pronoun                                                 |
| PRON       | PRR       | No                   | Reflexive pronoun                                                  |
| PRON       | WP        | No                   | Wh-pronoun                                                         |
|            |           |                      |                                                                    |
| PRT        | EP        | No                   | Final particle                                                     |
| PRT        | OP        | No                   | Coordinative article                                               |
| PRT        | RPC       | No                   | Clitic particle                                                    |
| PRT        | RPNEG     | No                   | Negation particle                                                  |
| PRT        | RPQ       | No                   | Question particle                                                  |
|            |           |                      |                                                                    |
| PUNCT      | .         | No                   | Terminal punctuation such as .!?                                   |
| PUNCT      | ,         | No                   | Comma and comma-like punctuation                                   |
| PUNCT      | :         | No                   | Colon and semi-colon                                               |
| PUNCT      | (         | No                   | Left bracket punctuation                                           |
| PUNCT      | )         | No                   | Right bracket punctuation                                          |
| PUNCT      | \`\`      | No                   | Open quotation mark and similar punctuation                        |
| PUNCT      | '         | No                   | Close quotation mark and other similar punctuation                 |
| PUNCT      | -         | No                   | Hyphen, dashes, and similar punctuation                            |
|            |           |                      |                                                                    |
| VERB       | NOMP      | No                   | Nominal predicate                                                  |
| VERB       | VB        | No                   | Verb                                                               |
|            |           |                      |                                                                    |
| X          | FW        | No                   | Foreign word whose meaning is not known and cannot be inferred     |
| X          | GW        | No                   | Word parts separated due to bad tokenization                       |
| X          | LS        | No                   | List symbols                                                       |
| X          | NFP       | No                   | Non-final punctuation, including emoticons and multi-symbol tokens |
| X          | SYM       | No                   | Symbol                                                             |
| X          | UH        | No                   | Interjection or hesitation                                         |
| X          | XX        | No                   | Total garbage                                                      |

### Annotation tagset

Below listed 75 tags are used in lexicon annotations. Every lexicon entry should
have one of the part-of-speech tags listed under the *Annotation Tag* column in
its `tag` field.

In order to keep the lexicon size minimal we introduce a concept called **cross
classification of lexicon entries**.

It assumed that for every lexicon entry that is annotated with certain
annotation tags, the final lexicon should contain identical lexicon entries to
that annotated entry which only differ in part-of-speech (below table presents
the parts-of-speech which can be cross classified under the
*Cross Classifies As* column). Therefore, our lexicon is compressed. To obtain
the fully expanded lexicon a pre-processing stage is required in which new
lexicon entries are added for cross classification parts-of-speech (e.g. a
lexicon entry annotation which has the annotation tag `PDT` triggers creation of
two lexicon entries where one has the tag `NOMP` and the other has the tag
`PDT`, see [//analyzer/src/lexicon/parser.py][7]).

| Coarse Tag | Annotation Tag   | Cross Classifies As    | Description                                                                                                                                  |
|:---------- |:---------------- |:---------------------- |:-------------------------------------------------------------------------------------------------------------------------------------------- |
| ADJ        | JJ               | JJ, NN, NOMP, PRI, RB  | Adjective                                                                                                                                    |
| ADJ        | JJN              | JJ, NN, NOMP           | Adjective which can also be used as noun and nominal predicate                                                                               |
|            |                  |                        |                                                                                                                                              |
| ADP        | IN               | IN, NN, NOMP           | Postposition                                                                                                                                 |
|            |                  |                        |                                                                                                                                              |
| ADV        | RB               | RB                     | Adverb                                                                                                                                       |
| ADV        | RB-TEMP          | NN-TEMP, NOMP, RB      | Temporal adverb                                                                                                                              |
| ADV        | WRB              | NOMP, WRB              | Interrogative adverb                                                                                                                         |
|            |                  |                        |                                                                                                                                              |
| AFFIX      | PFX              | PFX                    | Prefixes                                                                                                                                     |
|            |                  |                        |                                                                                                                                              |
| CONJ       | CC               | CC                     | Coordinating conjunction                                                                                                                     |
|            |                  |                        |                                                                                                                                              |
| DET        | DT               | DT, NOMP, PRI          | Determiner                                                                                                                                   |
| DET        | PDT              | NOMP, PDT              | Predeterminer                                                                                                                                |
| DET        | WDT              | NOMP, PRI, WDT         | Wh-determiner                                                                                                                                |
|            |                  |                        |                                                                                                                                              |
| EXS        | EX               | EX, NOMP-CASE-BARE     | Existential                                                                                                                                  |
|            |                  |                        |                                                                                                                                              |
| NOUN       | ADD              | ADD, NOMP-WITH-APOS    | Electronic address (e-mail or URL)                                                                                                           |
| NOUN       | NN               | NN, NOMP               | Common noun                                                                                                                                  |
| NOUN       | NN-ABBR          | NN, NOMP-WITH-APOS     | Common noun abbreviation whose root might be separated from suffixes with an apostrophe                                                      |
| NOUN       | NN-ABBR-APOS     | NN, NOMP-APOS          | Common noun abbreviation whose root might be separated from suffixes with an apostrophe only when used as a nominal predicate                |
| NOUN       | NN-TEMP          | NN                     | Common noun that denotes temporality                                                                                                         |
| NOUN       | NNP              | NNP, NOMP-WITH-APOS    | Proper noun                                                                                                                                  |
| NOUN       | NNP-ABBR         | NNP, NOMP-WITH-APOS    | Proper noun abbreviation                                                                                                                     |
|            |                  |                        |                                                                                                                                              |
| NUM        | CD               | CD, NN, NOMP-WITH-APOS | Cardinal number                                                                                                                              |
| NUM        | CD-DIST          | NN, NOMP-WITH-APOS     | Distributive number                                                                                                                          |
| NUM        | CD-ORD           | NN, NOMP-WITH-APOS     | Ordinal number                                                                                                                               |
|            |                  |                        |                                                                                                                                              |
| ONOM       | DUP              | DUP                    | Onomatopoeic                                                                                                                                 |
|            |                  |                        |                                                                                                                                              |
| PRON       | PRD              | NOMP, PRD              | Demonstrative pronoun                                                                                                                        |
| PRON       | PRD-PNON         | NOMP-PNON, PRD         | Demonstrative pronoun whose root is marked for person-number and none possessiveness                                                         |
| PRON       | PRD-PNPOSS       | NOMP-PNPOSS, PRD       | Demonstrative pronoun whose root is marked for person-number and whose case markers are always realized as if it is marked for posessiveness |
| PRON       | PRI              | NOMP, PRI              | Indefinite pronoun                                                                                                                           |
| PRON       | PRP              | NOMP-PN, PRP           | Personal pronoun                                                                                                                             |
| PRON       | PRP-CASE         | NOMP-CASE-MARKED, PRP  | Personal pronoun whose root is marked for person-number, none possessiveness and case                                                        |
| PRON       | PRP-IRR          | NOMP-PNON, PRP         | Personal pronoun whose root is marked for person-number and none posessiveness, which cannot be inflected for dative case                    |
| PRON       | PRP$             | NOMP-PNON, PRP$        | Possessive pronoun                                                                                                                           |
| PRON       | PRR              | NOMP, PRR              | Reflexive pronoun                                                                                                                            |
| PRON       | WP               | NOMP, WP               | Wh-pronoun                                                                                                                                   |
|            |                  |                        |                                                                                                                                              |
| PRT        | EP               | EP                     | Final particle                                                                                                                               |
| PRT        | OP               | OP                     | Coordinative article                                                                                                                         |
| PRT        | RPC              | RPC                    | Clitic particle                                                                                                                              |
| PRT        | RPNEG            | NOMP-CASE-BARE, RPNEG  | Negation particle                                                                                                                            |
| PRT        | RPQ              | NOMP-CASE-BARE, RPQ    | Question particle                                                                                                                            |
|            |                  |                        |                                                                                                                                              |
| PUNCT      | PUNCT-6          | .                      | Terminal punctuation such as .!?                                                                                                             |
| PUNCT      | PUNCT-4          | ,                      | Comma and comma-like punctuation                                                                                                             |
| PUNCT      | PUNCT-7          | :                      | Colon and semi-colon                                                                                                                         |
| PUNCT      | PUNCT-2          | (                      | Left bracket punctuation                                                                                                                     |
| PUNCT      | PUNCT-3          | )                      | Right bracket punctuation                                                                                                                    |
| PUNCT      | PUNCT-8          | \`\`                   | Open quotation mark and similar punctuation                                                                                                  |
| PUNCT      | PUNCT-1          | '                      | Close quotation mark and other similar punctuation                                                                                           |
| PUNCT      | PUNCT-5          | -                      | Hyphen, dashes, and similar punctuation                                                                                                      |
|            |                  |                        |                                                                                                                                              |
| VERB       | NOMP             | NOMP                   | Nominal predicate                                                                                                                            |
| VERB       | NOMP-APOS        | NOMP                   | Nominal predicate whose root is always separated from suffixes with an apostrophe                                                            |
| VERB       | NOMP-CASE-BARE   | NOMP                   | Nominal predicate whose root is caseless but marked for person-number and none possessiveness                                                |
| VERB       | NOMP-CASE-MARKED | NOMP                   | Nominal predicate whose root is marked for person-number, none possessiveness and case                                                       |
| VERB       | NOMP-PN          | NOMP                   | Nominal predicate whose root is marked for person-number                                                                                     |
| VERB       | NOMP-PNON        | NOMP                   | Nominal predicate whose root is marked for person-number and none possessiveness                                                             |
| VERB       | NOMP-PNPOSS      | NOMP                   | Nominal predicate whose root is marked for person-number and whose case markers are always realized as if it is marked for posessiveness     |
| VERB       | NOMP-WITH-APOS   | NOMP                   | Nominal predicate whose root might be separated from suffixes with an apostrophe                                                             |
| VERB       | VB-HL-AR-DHR     | VB                     | Verb that takes `+Hl` as passive, `+Ar` as aorist tense and `+DHr` as causative marker                                                       |
| VERB       | VB-HL-AR-HR      | VB                     | Verb that takes `+Hl` as passive, `+Ar` as aorist tense and `+Hr` as causative marker                                                        |
| VERB       | VB-HL-AR-HT      | VB                     | Verb that takes `+Hl` as passive, `+Ar` as aorist tense and `+Ht` as causative marker                                                        |
| VERB       | VB-HL-AR-NO      | VB                     | Verb that takes `+Hl` as passive and `+Ar` as aorist tense marker, but does not take a causative marker                                      |
| VERB       | VB-HL-AR-T       | VB                     | Verb that takes `+Hl` as passive, `+Ar` as aorist tense and `+t` as causative marker                                                         |
| VERB       | VB-HL-HR-DHR     | VB                     | Verb that takes `+Hl` as passive, `+Hr` as aorist tense and `+DHr` as causative marker                                                       |
| VERB       | VB-HL-HR-NO      | VB                     | Verb that takes `+Hl` as passive and `+Hr` as aorist tense marker, but does not take a causative marker                                      |
| VERB       | VB-HL-HR-T       | VB                     | Verb that takes `+Hl` as passive, `+Hr` as aorist tense and `+t` as causative marker                                                         |
| VERB       | VB-HN-AR-DHR     | VB                     | Verb that takes `+Hn` as passive, `+Ar` as aorist tense and `+DHr` as causative marker                                                       |
| VERB       | VB-HN-HR-DHR     | VB                     | Verb that takes `+Hn` as passive, `+Hr` as aorist tense and `+DHr` as causative marker                                                       |
| VERB       | VB-HN-HR-NO      | VB                     | Verb that takes `+Hn` as passive and `+Hr` as aorist tense marker, but does not take a causative                                             |
| VERB       | VB-HN-HR-T       | VB                     | Verb that takes `+Hn` as passive, `+Hr` as aorist tense and `+t` as causative marker                                                         |
| VERB       | VB-ON-OR-DHR     | VB                     | Verb that takes `+Hn` as passive, `+r` as aorist tense and `+DHr` as causative marker                                                        |
| VERB       | VB-ON-OR-T       | VB                     | Verb that takes `+Hn` as passive, `+r` as aorist tense and `+Dt` as causative marker                                                         |
|            |                  |                        |                                                                                                                                              |
| X          | FW               | FW                     | Foreign word whose meaning is not known and cannot be inferred                                                                               |
| X          | GW               | GW                     | Word parts separated due to bad tokenization                                                                                                 |
| X          | LS               | LS                     | List symbols                                                                                                                                 |
| X          | NFP              | NFP                    | Non-final punctuation, including emotico nsand multi-symbol tokens                                                                           |
| X          | SYM              | SYM                    | Symbol                                                                                                                                       |
| X          | UH               | UH                     | Interjection or hesitation                                                                                                                   |
| X          | XX               | XX                     | Total garbage                                                                                                                                |

## Annotating root form

Every lexicon entry should have the root form annotated in the `root` field.

To annotate root forms;

1. decide on the part-of-speech of the root by referring to
[Annotating part-of-speech][1].
2. strip off all the suffixes (inflectional and derivational morphemes) from the
word form, given a morphotactic model that defines the inflections and
derivations for part-of-speech and the corresponding morpheme inventory.
3. remaining string is the root form.
4. if the root form ends with a compounding marker `+SH` leave it as a part of
the root form annotation (e.g. the word *ahçıbaşınınki* should have *ahçıbaşı*
as its root form annotation, not *ahçıbaş*).

## Annotating morphophonemic irregularities

Before you read this section it is strongly advised to refer to
[Oflazer, K. (1994). Two-level description of Turkish morphology. Literary and
linguistic computing, 9(2), 137-148][6] for an outline of the Turkish
morphophonemic processes.

Every lexicon entry should have the morphophonemic irregularities annotated in
the `morphophonemics` field.

To annotate morphophonemic irregularities;

1. go through the list of rules presented in below sections and decide on the
morphophonemic irregularity annotation string by referring to those that apply
to the root form.
2. if more than one of these rules apply to the root form, what all applying
annotation rules dictate should be incorporated in the final morphophonemic
annotation string.
3. if none of these rules apply to the root form, use `~` as the morphophonemic
irregularity annotation string.

### Voicing exceptions

The voicing exception applies to roots whose final voiceless consonant fails to
get voiced in spite of the affixation of a suffix that starts with a vowel. This
exception applies only to sounds that are `[-voiced][+plosive]`
(e.g. { ***p***, ***t***, ***k***, ***t***, ***ʃ*** }). Voiceless continuants
{ ***f***, ***s***, ***ʃ*** } never undergo voicing anyway.

#### Roots ending with `K` annotation mark up

Root final voiceless plosive ***k*** is always assumed to realize as ***ğ***
when a suffix starting with a vowel is affixed. Sometimes root final voiceless
plosive ***k*** realizes as ***g*** instead of ***ğ*** only if it is preceded by
***n***.

If the root ends with voiceless plosive ***k*** which is left unchanged (and not
realized as ***ğ*** or ***g***) after a suffix starting with a vowel is affixed,
then the root final velar stop ***k*** is annotated with the markup `K`.

For the sake of consistency, even there are no suffixes which start with a vowel
that can be affixed to the root in the affix inventory of the morphotactic model
for the annotated part-of-speech of the root, this rule still applies (e.g. as
seen in the adjectival examples below).

| Coarse Tag | Root       | Morphophonemic Annotation | Example      |
|:---------- |:---------- |:------------------------- |------------- |
| ADJ        | ak         | a`K`                      | ak           |
| ADJ        | tok        | to`K`                     | tok          |
| NOUN       | mercanköşk | mercanköş`K`              | mercanköşk-e |
| NOUN       | meşk       | meş`K`                    | meşk-i       |
| NOUN       | şark       | şar`K`                    | şark-ı       |
| NOUN       | türk       | tür`K`                    | türk-e       |
| VERB       | bük        | bü`K`                     | bük-er       |
| VERB       | kalk       | kal`K`                    | kalk-ar      |
| VERB       | sok        | so`K`                     | sok-ar       |

#### Roots ending with `~` annotation mark up

Root final voiceless plosive ***p*** (or ***t***) is always assumed to be left
unchanged after a suffix starting with a vowel is affixed.

If the root ends with the voiceless plosive ***p*** (or ***t***) which is
realized as voiced ***b***  (or resp. ***d***) when a suffix starting with a
vowel is affixed, then the root final voiceless plosive ***p*** (or ***t***)
should be annotated with a succeeding `~` annotation markup.

| Coarse Tag | Root      | Morphophonemic Annotation | Example     |
|:---------- |:--------- |:------------------------- |------------ |
| NOUN       | dolap     | dolap`~`                  | dolab-ın    |
| NOUN       | mikrop    | mikrop`~`                 | mikrob-u    |
| NOUN       | kanat     | kanat`~`                  | kanad-ının  |
| NOUN       | tehdit    | tehdit`~`                 | tehdid-i    |
| VERB       | bahset    | bahset`~`                 | bahsed-iyor |
| VERB       | git       | git`~`                    | gid-ecek    |

#### Roots ending with `Ç` annotation mark up

Root final voiceless plosive ***ç*** is always assumed to realize as voiced
***c*** when a suffix starting with a vowel is affixed.

If the root ends with the voiceless plosive ***ç*** which is left unchanged (and
not realized as ***c***) after a suffix starting with a vowel is affixed, then
the root final voiceless plosive ***ç*** is annotated with the markup `Ç`.

| Coarse Tag | Root      | Morphophonemic Annotation | Example    |
|:---------- |:--------- |:------------------------- |----------- |
| NOUN       | göç       | gö`Ç`                     | göç-e      |
| NOUN       | sandviç   | sandvi`Ç`                 | sandviç-in |
| NOUN       | suç       | su`Ç`                     | suç-u      |
| NUM        | üç        | ü`Ç`                      | üç-er      |
| VERB       | aç        | a`Ç`                      | aç-ıl      |
| VERB       | seç       | se`Ç`                     | seç-er     |

### Vowel harmony exceptions

#### Palatalization of final ***l***

The lateral ***l*** has allophones when it occurs in the root final position
after back vowels.

| Velar ***l*** (back) | Palatal ***l*** (front) |
|:-------------------- |:----------------------- |
| sol                  | sol (anahtarı)          |
| okul                 | usul                    |
| araba                | kalp                    |
| bor                  | golf                    |

When roots that have a palatalized root final ***l*** are followed by a suffix
that starts with a vowel, the surface form of the suffixes are resolved as if
the last syllable of the root has a front vowel.

##### Roots ending with `%` annotation in the last vowel position

Certain roots that have the back rounded vowel ***o*** as its last vowel
followed by a ***l*** cause the first back vowel of the affixed suffix to be
realized as a front vowel.

The last vowel of those roots should be annotated with the markup `%`.

| Coarse Tag | Root      | Morphophonemic Annotation | Example     |
|:---------- |:--------- |:------------------------- |------------ |
| NOUN       | mentol    | ment`%`l                  | mentol-lü   |
| NOUN       | metropol  | metrop`%`l                | metropol-de |
| NOUN       | monokl    | monok`%`l                 | monokol-e   |

##### Roots ending with `{` annotation in the last vowel position

Certain roots that have the back unrounded vowel ***a*** as its last vowel
followed by a ***l*** cause the first back vowel of the affixed suffix to be
realized as a front vowel.

The last vowel of those roots should be annotated with the markup `{`.

| Coarse Tag | Root        | Morphophonemic Annotation | Example        |
|:---------- |:----------- |:------------------------- |--------------- |
| ADJ        | biyomedikal | biyomedik`{`l             | biyomedikal-de |
| NOUN       | ideal       | ide`{`l                   | ideal-i        |
| NOUN       | ihtimal     | ihtim`{`l                 | ihtimal-iyle   |

In addition, if the root ends with a cluster that contains a back vowel and
{ ***r***, ***t***, ***b***, ***d*** }, same phenomena could be observed. The
last vowel of such roots should also be annotated with the markup `{`.

| Coarse Tag | Root      | Morphophonemic Annotation | Example    |
|:---------- |:--------- |:------------------------- |----------- |
| NOUN       | dikkat    | dikk`{`t                  | dikkat-i   |
| NOUN       | harf      | hr`{`f                    | harf-e     |
| NOUN       | hat       | h`{`t`~"`                 | had-dinin  |
| NOUN       | saat      | sa`{`t                    | saat-e     |

##### Roots ending with `}` annotation in the last vowel position

Certain roots that have the back rounded vowel ***u*** as its last vowel
followed by a ***l*** cause the first back vowel of the affixed suffix to be
realized as a front vowel.

The last vowel of those roots should be annotated with the markup `}`.

| Coarse Tag | Root      | Morphophonemic Annotation | Example    |
|:---------- |:--------- |:------------------------- |----------- |
| ADJ        | mesul     | mes`}`l                   | mesul-ü    |
| NOUN       | ampul     | amp`}`l                   | ampul-e    |
| NOUN       | duhul     | duh`}`l                   | duhul-de   |

##### Roots ending with `[` annotation in the last vowel position

Certain roots that have the long ***â*** as its last vowel followed by a
***l*** cause the first back vowel of the affixed suffix to be realized as a
front vowel.

The last vowel of those roots should be annotated with the markup `[`.

| Coarse Tag | Root      | Morphophonemic Annotation | Example    |
|:---------- |:--------- |:------------------------- |----------- |
| NOUN       | eşkâl     | eşk`[`l                   | eşkâl-i    |
| NOUN       | hâl       | h`[`l                     | hâl-den    |
| NOUN       | işkâl     | işk`[`l                   | işkâl-inin |

#### Vowel closing

For certain verbal roots, root final front unrounded open vowel ***e*** is
realized as close ***i*** when a suffix starting with a vowel is affixed.

The final front unrounded vowel ***e*** of those roots should be annotated with
the `E` annotation markup.

| Coarse Tag | Root      | Morphophonemic Annotation | Example    |
|:---------- |:--------- |:------------------------- |----------- |
| VERB       | de        | d`E`                      | d-i-yecek  |
| VERB       | ye        | y`E`                      | y-i-yor    |

### Epenthesis

Last vowel of certain root forms are dropped when a suffix that starts with a
vowel or a consonant that drops gets affixed.

The final vowel of those roots should be annotated with a succeeding `?`
annotation markup.

| Coarse Tag | Root      | Morphophonemic Annotation | Example    |
|:---------- |:--------- |:------------------------- |----------- |
| NOUN       | böğür     | böğü`?`r                  | böğr-üme   |
| NOUN       | burun     | buru`?`n                  | burn-um    |
| NOUN       | isim      | isi`?`m                   | ism-e      |
| VERB       | çağır     | çağı`?`r                  | çağr-ıldı  |

### Gemination

For some words, root final consonant { ***b***, ***c***, ***d***, ***f***,
***k***, ***l***, ***m***, ***n***, ***r***, ***t***, ***z*** } is duplicated
when a suffix starting with a vowel is affixed.

The final consonant of those roots should be annotated with a succeeding `"`
annotation markup.

| Coarse Tag | Root      | Morphophonemic Annotation | Example    |
|:---------- |:--------- |:------------------------- |----------- |
| ADJ        | muhil     | muhil`"`                  | muhil-l-i  |
| ADJ        | muhip     | muhip`~"`                 | muhib-b-in |
| NOUN       | af        | af`"`                     | af-f-ın    |
| NOUN       | hak       | hak`"`                    | hak-k-a    |

### Roots ending with `-su`

Certain nominal root forms that end with `su` alter the initial consonant of
some suffixes (e.g. 3rd person possessive and genitive case inflection
morphemes) when they are affixed.

Root final `su` of those root forms should be annotated with a succeeding `^`
annotation markup.

| Coarse Tag | Root      | Morphophonemic Annotation | Example    |
|:---------- |:--------- |:------------------------- |----------- |
| NOUN       | akarsu    | akarsu`^`                 | akarsu-yun |
| NOUN       | yuzsu     | yuzsu`^`                  | yuzsu-yu   |
| NOUN       | su        | su`^`                     | su-yu      |

### Foreign words and code switching

In case of code switching, foreign words could be used in Turkish sentences,
while preserving their surface form and getting inflected according to the
part-of-speech that they hold within the context.

Foreign word stems should be annotated by enclosing the last syllable of their
Turkish pronunciation enclosed in `*` annotation markup.

| Coarse Tag | Root      | Morphophonemic Annotation | Example     |
|:---------- |:--------- |:------------------------- |------------ |
| NOUN       | ABD       | ABD`*e*`                  | ABD-de      |
| NOUN       | single    | single`*ıl*`              | single-ının |

## Annotating features

Certain lexicon entry annotations must be annotated with morphosyntactic and
morphosemantic feature tags to represent the features that are intrinsically
carried by the root itself without affixation of any inflectional or
derivational morpheme.

Every lexicon entry should have features annotated in the `features` field.
Every feature should be annotated in the form of
`+[feature_category=feature_tag]`.

To annotate features;

1. check whether annotated part-of-speech of the lexicon entry matches one of
the part-of-speech listed in the tables for required and optional features (note
that set of part-of-speech tags that require features annotation in both lists
are disjoint).
2. if so, annotate the lexicon entry with corresponding feature tags that apply
for the root.
3. if annotated part-of-speech of the lexicon entry does not match any of the
part-of-speech listed in the tables for required and optional features, use `~`
as the features annotation string.

Note that if a lexicon entry is required to be annotated with more than one
feature, all applicable features should be annotated in sequence, in the form of
`+[feature_category_1=feature_tag_1]+[feature_category_2=feature_tag_2]` (e.g.
lexicon entries that are annotated with `PRP-CASE` part-of-speech tag should
take three feature tags in sequence, where the first feature is chosen from the
set of features tags { `A1sg`, `A2sg`, `A3sg`, `A1pl`, `A2pl`, `A3pl` } and the
second chosen from { `Pnon` }, and so on).

Below listed 31 feature tags compose our features tagset.

| Feature Category | Feature Tag | Description                                            |
|:---------------- |:----------- |:------------------------------------------------------ |
| PersonNumber     | A1sg        | 1st person singular                                    |
| PersonNumber     | A2sg        | 2nd person singular                                    |
| PersonNumber     | A3sg        | 3rd person singular                                    |
| PersonNumber     | A1pl        | 1st person plural                                      |
| PersonNumber     | A2pl        | 2nd person plural                                      |
| PersonNumber     | A3pl        | 3rd person plural                                      |
| Case             | Abl         | Ablative case marked                                   |
| Case             | Acc         | Accusative case marked                                 |
| Case             | Dat         | Dative case marked                                     |
| Case             | Gen         | Genitive case marked                                   |
| Case             | Ins         | Instrumental case marked                               |
| Case             | Loc         | Locative case marked                                   |
| ComplementType   | CAbl        | (Postposition has) ablative case marked complement     |
| ComplementType   | CAcc        | (Postposition has) accusative case marked complement   |
| ComplementType   | CBare       | (Postposition has) caseless complement                 |
| ComplementType   | CDat        | (Postposition has) dative case marked complement       |
| ComplementType   | CFin        | (Postposition has) finite complement                   |
| ComplementType   | CGen        | (Postposition has) genitive case marked complement     |
| ComplementType   | CIns        | (Postposition has) instrumental case marked complement |
| ComplementType   | CNum        | (Postposition has) numeric complement                  |
| ConjunctionType  | Adv         | Adverbial conjunction                                  |
| ConjunctionType  | Coor        | Coordinating conjunction                               |
| ConjunctionType  | Par         | Parallel conjunction                                   |
| ConjunctionType  | Sub         | Subordinating conjunction                              |
| DeterminerType   | Def         | Definitive (determiner)                                |
| DeterminerType   | Dem         | Demonstrative (determiner)                             |
| DeterminerType   | Dir         | Directional (determiner)                               |
| DeterminerType   | Ind         | Indefinite (determiner)                                |
| Emphasis         | True        | Emphasis                                               |
| Possessive       | Pnon        | None possessive                                        |
| Temporal         | True        | Temporal                                               |

### Required features

All lexicon entries that are annotated with one of the below listed
part-of-speech tags are required to be annotated with the corresponding feature
tag(s).

| Coarse Tag | Annotation Tag   | Required Features                                                                                              |
|:---------- |:---------------- |:-------------------------------------------------------------------------------------------------------------- |
| ADP        | IN               | +\[ComplementType=CAbl\|CAcc\|CBare\|CDat\|CFin\|CGen\|CIns\|CNum\]                                                |
|            |                  |                                                                                                                |
| ADV        | RB-TEMP          | +\[Temporal=True\]                                                                                             |
|            |                  |                                                                                                                |
| CONJ       | CC               | +\[ConjunctionType=Adv\|Coor\|Par\|Sub\]                                                                       |
|            |                  |                                                                                                                |
| DET        | DT               | +\[DeterminerType=Def\|Dem\|Dir\|Ind\]                                                                         |
|            |                  |                                                                                                                |
| NOUN       | NN-TEMP          | +\[Temporal=True\]                                                                                             |
|            |                  |                                                                                                                |
| PRON       | PRD-PNON         | +\[PersonNumber=A1sg\|A2sg\|A3sg\|A1pl\|A2pl\|A3pl\]+\[Possessive=Pnon\]                                       |
| PRON       | PRD-PNPOSS       | +\[PersonNumber=A1sg\|A2sg\|A3sg\|A1pl\|A2pl\|A3pl\]                                                           |
| PRON       | PRP              | +\[PersonNumber=A1sg\|A2sg\|A3sg\|A1pl\|A2pl\|A3pl\]                                                           |
| PRON       | PRP-CASE         | +\[PersonNumber=A1sg\|A2sg\|A3sg\|A1pl\|A2pl\|A3pl\]+\[Possessive=Pnon\]+\[Case=Acc\|Abl\|Dat\|Gen\|Ins\|Loc\] |
| PRON       | PRP-IRR          | +\[PersonNumber=A1sg\|A2sg\|A3sg\|A1pl\|A2pl\|A3pl\]+\[Possessive=Pnon\]                                       |
| PRON       | PRP-PRP$         | +\[PersonNumber=A1sg\|A2sg\|A3sg\|A1pl\|A2pl\|A3pl\]+\[Possessive=Pnon\]                                       |
|            |                  |                                                                                                                |
| VERB       | NOMP-CASE-BARE   | +\[PersonNumber=A3sg\]+\[Possessive=Pnon\]+\[Bare\]                                                            |
| VERB       | NOMP-CASE-MARKED | +\[PersonNumber=A1sg\|A2sg\|A3sg\|A1pl\|A2pl\|A3pl\]+\[Possessive=Pnon\]+\[Case=Acc\|Abl\|Dat\|Gen\|Ins\|Loc\] |
| VERB       | NOMP-PN          | +\[PersonNumber=A1sg\|A2sg\|A3sg\|A1pl\|A2pl\|A3pl\]                                                           |
| VERB       | NOMP-PNON        | +\[PersonNumber=A1sg\|A2sg\|A3sg\|A1pl\|A2pl\|A3pl\]+\[Possessive=Pnon\]                                       |
| VERB       | NOMP-PNPOSS      | +\[PersonNumber=A1sg\|A2sg\|A3sg\|A1pl\|A2pl\|A3pl\]                                                           |

### Optional features

All lexicon entries that are annotated with one of the below listed
part-of-speech tags might be annotated with the corresponding feature tag(s),
if and only if the feature tag applies to the root.

| Coarse Tag | Annotation Tag  | Optional Features                 |
|:---------- |:--------------- |:--------------------------------- |
| ADJ        | JJ              | +\[Emphasis=True\]                |
| ADJ        | JJN             | +\[Emphasis=True\]                |
|            |                 |                                   |
| ADV        | RB              | +\[Emphasis=True\|Temporal=True\] |

## Annotating compound roots

Certain Turkish root forms end with a compounding marker `+SH`, which is
ambiguous with a 3rd person possessive marker (e.g. common noun: *atbalığı*,
proper noun: *Kırklareli*).

Defining the morphotactics for those cases are particularly challenging. For
example, if the word is a common noun which is inflected for person-number, the
person-number morpheme occurs before the compounding marker which is essentially
part of the root form. While implementing a morphological analyzer, this
phenomena violates the assumption that all suffixes are sequentially affixed to
the root.

Every lexicon entry should have this phenomena annotated in the `is_compound`
field.

To annotate roots that end with a compounding marker;

1. `is_compound` field should be annotated as `TRUE` if the root form ends with
a compounding marker (otherwise, `FALSE`).
2. the morphophonemic irregularity annotation string in the `morphophonemics`
field should be the root form without the final compounding marker (e.g.
the word *atbalığı* should have *atbalık* as its morphophonemics annotation).
3. if any of the morphophonemics processes that are described in the
[Annotating morphophonemic irregularities][3] applies to morphophonemic
annotation string yielded by (2), they should also be represented in the
morphophonemics annotations (e.g. *adamkökü* should have *adamkö*`K` as its
morphophonemics annotation, not *adamkök*).
4. lexicon entries for root forms that do not end with a compounding marker
should follow the rules defined in
[Annotating morphophonemic irregularities][3].

[1]: #annotating-part-of-speech
[2]: #annotating-root-form
[3]: #annotating-morphophonemic-irregularities
[4]: #annotating-features
[5]: #annotating-compound-roots
[6]: https://s3.amazonaws.com/academia.edu.documents/35587556/morphspecs-fixed.pdf?AWSAccessKeyId=AKIAIWOWYYGZ2Y53UL3A&Expires=1537291706&Signature=AjFntxShQrQiaXdp%2B3%2ByneCbJxg%3D&response-content-disposition=inline%3B%20filename%3DAn_Outline_of_Turkish_Morphology.pdf
[7]: ./parser.py
